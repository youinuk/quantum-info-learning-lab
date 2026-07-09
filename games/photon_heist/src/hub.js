const HUB_TEXT = {
  ko: {
    eyebrow: "PHOTON HEIST · 작전 본부",
    title: "빛의 규칙을 훔쳐라",
    intro: "고전 광학에서 시작해 양자정보 작전까지 이어지는 캠페인이다.",
    language: "언어",
    completed: "완료 작전",
    stars: "획득 별",
    next: "다음 목표",
    route: "CAMPAIGN ROUTE",
    chapters: "챕터 선택",
    unlockRule: "필수 작전을 클리어하면 다음 챕터가 열린다. 별은 숙련 기록이며 진행을 막지 않는다.",
    enter: "작전 시작",
    continue: "계속하기",
    replay: "다시 플레이",
    locked: "잠김",
    planned: "개발 예정",
    complete: "필수 작전 완료",
    requirement: "잠금 조건",
    requiredClear: "필수 작전 클리어",
    noMission: "현재 구현된 작전을 모두 완료했다"
  },
  en: {
    eyebrow: "PHOTON HEIST · OPERATIONS HQ",
    title: "Steal the Rules of Light",
    intro: "A campaign from classical optics to quantum information.",
    language: "Language",
    completed: "Missions cleared",
    stars: "Stars earned",
    next: "Next objective",
    route: "CAMPAIGN ROUTE",
    chapters: "Select Chapter",
    unlockRule: "Clear required missions to unlock the next chapter. Stars record mastery and never block progress.",
    enter: "Start operation",
    continue: "Continue",
    replay: "Replay chapter",
    locked: "Locked",
    planned: "In development",
    complete: "Required mission cleared",
    requirement: "Unlock condition",
    requiredClear: "Clear required mission",
    noMission: "All currently available operations are complete"
  }
};

window.applyPhotonHeistTextFixes?.();

const hubState = {
  lang: loadHubLanguage(),
  progress: new Map()
};

const hubEl = {
  eyebrow: document.getElementById("hubEyebrow"),
  title: document.getElementById("hubTitle"),
  intro: document.getElementById("hubIntro"),
  languageLabel: document.getElementById("hubLanguageLabel"),
  languageSelect: document.getElementById("hubLanguageSelect"),
  completedLabel: document.getElementById("hubCompletedLabel"),
  completed: document.getElementById("hubCompleted"),
  starsLabel: document.getElementById("hubStarsLabel"),
  stars: document.getElementById("hubStars"),
  nextLabel: document.getElementById("hubNextLabel"),
  next: document.getElementById("hubNext"),
  campaignEyebrow: document.getElementById("campaignEyebrow"),
  campaignTitle: document.getElementById("campaignTitle"),
  unlockRule: document.getElementById("unlockRule"),
  chapterGrid: document.getElementById("chapterGrid")
};

function ht(key) { return HUB_TEXT[hubState.lang][key]; }

function hubUrl(path) {
  return window.PhotonHeistBridge?.withLanguage(path, hubState.lang) || path;
}

function loadHubLanguage() {
  if (window.PhotonHeistBridge) return window.PhotonHeistBridge.getLanguage();
  try { return localStorage.getItem("photonHeistHubLanguage") === "en" ? "en" : "ko"; }
  catch (_) { return "ko"; }
}

function readProgress(chapter) {
  if (!chapter.progressKey) return { bestStars: {}, challenges: {}, unlockedIndex: 0 };
  try {
    const parsed = JSON.parse(localStorage.getItem(chapter.progressKey));
    return parsed && typeof parsed === "object"
      ? { bestStars: parsed.bestStars || {}, challenges: parsed.challenges || {}, unlockedIndex: parsed.unlockedIndex || 0 }
      : { bestStars: {}, challenges: {}, unlockedIndex: 0 };
  } catch (_) {
    return { bestStars: {}, challenges: {}, unlockedIndex: 0 };
  }
}

function chapterStats(chapter) {
  const progress = hubState.progress.get(chapter.id) || readProgress(chapter);
  const stars = Object.values(progress.bestStars).reduce((sum, value) => sum + (Number(value) || 0), 0);
  const completed = Object.values(progress.bestStars).filter(value => Number(value) > 0).length;
  const requiredComplete = (chapter.requiredStageIds || []).every(id => Number(progress.bestStars[id]) > 0);
  return { progress, stars, completed, requiredComplete };
}

function hasOwnProgress(chapter) {
  return chapterStats(chapter).completed > 0;
}

function prerequisiteMet(chapter) {
  if (!chapter.prerequisite) return true;
  const previous = PHOTON_CHAPTERS.find(item => item.id === chapter.prerequisite.chapterId);
  if (!previous) return false;
  const progress = chapterStats(previous).progress;
  return chapter.prerequisite.requiredStageIds.every(id => Number(progress.bestStars[id]) > 0);
}

function chapterUnlocked(chapter) {
  return !chapter.prerequisite || prerequisiteMet(chapter) || hasOwnProgress(chapter);
}

function requirementText(chapter) {
  if (!chapter.prerequisite) return ht("requiredClear");
  const previous = PHOTON_CHAPTERS.find(item => item.id === chapter.prerequisite.chapterId);
  const previousTitle = previous ? previous.title[hubState.lang] : chapter.prerequisite.chapterId;
  return `${previousTitle} ${chapter.prerequisite.requiredStageIds.join(", ")} ${hubState.lang === "ko" ? "클리어" : "clear"}`;
}

function makeChapterCard(chapter) {
  const stats = chapterStats(chapter);
  const available = chapter.available !== false && Boolean(chapter.file);
  const unlocked = available && chapterUnlocked(chapter);
  const percent = chapter.stageCount ? Math.min(100, stats.completed / chapter.stageCount * 100) : 0;
  const card = document.createElement("article");
  card.className = `chapter-card${unlocked ? " unlocked" : " locked"}${stats.requiredComplete ? " complete" : ""}`;
  card.style.setProperty("--chapter-accent", chapter.accent);

  const top = document.createElement("div");
  top.className = "chapter-card-top";
  const number = document.createElement("span");
  number.className = "chapter-number";
  number.textContent = `0${chapter.order}`.slice(-2);
  const icon = document.createElement("span");
  icon.className = "chapter-icon";
  icon.textContent = chapter.icon;
  top.append(number, icon);

  const title = document.createElement("h3");
  title.textContent = chapter.title[hubState.lang];
  const concept = document.createElement("strong");
  concept.className = "chapter-concept";
  concept.textContent = chapter.concept[hubState.lang];
  const description = document.createElement("p");
  description.textContent = chapter.description[hubState.lang];

  const progress = document.createElement("div");
  progress.className = "chapter-progress";
  const progressText = document.createElement("div");
  progressText.innerHTML = `<span>${stats.completed}/${chapter.stageCount}</span><span>*${stats.stars}/${chapter.stageCount * 3}</span>`;
  const track = document.createElement("div");
  track.className = "chapter-progress-track";
  const fill = document.createElement("span");
  fill.style.width = `${percent}%`;
  track.appendChild(fill);
  progress.append(progressText, track);

  const footer = document.createElement("div");
  footer.className = "chapter-card-footer";
  const status = document.createElement("span");
  status.className = "chapter-status";
  if (!available) status.textContent = ht("planned");
  else if (!unlocked) status.textContent = `LOCK ${requirementText(chapter)}`;
  else if (stats.requiredComplete) status.textContent = `OK ${ht("complete")}`;
  else status.textContent = stats.completed ? `${stats.completed}/${chapter.stageCount}` : ht("enter");

  if (unlocked) {
    const link = document.createElement("a");
    link.className = "chapter-enter";
    link.href = hubUrl(chapter.file);
    link.textContent = stats.requiredComplete ? ht("replay") : stats.completed ? ht("continue") : ht("enter");
    footer.append(status, link);
  } else {
    const button = document.createElement("button");
    button.disabled = true;
    button.textContent = available ? ht("locked") : ht("planned");
    footer.append(status, button);
  }

  card.append(top, title, concept, description, progress, footer);
  return card;
}

function renderHub() {
  document.documentElement.lang = hubState.lang;
  hubEl.languageSelect.value = hubState.lang;
  hubEl.eyebrow.textContent = ht("eyebrow");
  hubEl.title.textContent = ht("title");
  hubEl.intro.textContent = ht("intro");
  hubEl.languageLabel.textContent = ht("language");
  hubEl.completedLabel.textContent = ht("completed");
  hubEl.starsLabel.textContent = ht("stars");
  hubEl.nextLabel.textContent = ht("next");
  hubEl.campaignEyebrow.textContent = ht("route");
  hubEl.campaignTitle.textContent = ht("chapters");
  hubEl.unlockRule.textContent = ht("unlockRule");

  PHOTON_CHAPTERS.forEach(chapter => hubState.progress.set(chapter.id, readProgress(chapter)));
  const playable = PHOTON_CHAPTERS.filter(chapter => chapter.available !== false && chapter.progressKey);
  const totals = playable.reduce((sum, chapter) => {
    const stats = chapterStats(chapter);
    sum.completed += stats.completed;
    sum.stars += stats.stars;
    sum.stages += chapter.stageCount;
    return sum;
  }, { completed: 0, stars: 0, stages: 0 });
  hubEl.completed.textContent = `${totals.completed} / ${totals.stages}`;
  hubEl.stars.textContent = `${totals.stars} / ${totals.stages * 3}`;

  const nextChapter = playable.find(chapter => chapterUnlocked(chapter) && !chapterStats(chapter).requiredComplete);
  hubEl.next.textContent = nextChapter ? nextChapter.title[hubState.lang] : ht("noMission");
  hubEl.chapterGrid.replaceChildren(...PHOTON_CHAPTERS.map(makeChapterCard));
}

hubEl.languageSelect.addEventListener("change", event => {
  hubState.lang = event.target.value === "en" ? "en" : "ko";
  window.PhotonHeistBridge?.saveLanguage(hubState.lang);
  try { localStorage.setItem("photonHeistHubLanguage", hubState.lang); } catch (_) {}
  renderHub();
  window.PhotonHeistBridge?.reportHeight();
});

window.addEventListener("photonheist:language", event => {
  hubState.lang = event.detail.lang;
  renderHub();
  window.PhotonHeistBridge?.reportHeight();
});

window.addEventListener("storage", renderHub);
renderHub();
