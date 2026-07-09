const state = {
  lang: window.PhotonHeistBridge?.getLanguage() || "ko",
  levelIndex: 0,
  level: LEVELS[0],
  grid: [],
  laser: null,
  selected: null,
  rotations: 0,
  shots: 0,
  committed: false,
  shotHistory: [],
  keyCollected: false,
  objectiveIndex: 0,
  hintIndex: 0,
  usedHint: false,
  ray: null,
  cleared: false,
  alarm: false,
  lastStars: 0,
  soundEnabled: loadSoundPreference(),
  progress: loadProgress(),
  rotatedMirrors: new Set(),
  alarmsTriggered: 0
};

const el = {
  gameTitle: document.getElementById("gameTitle"),
  chapterLabel: document.getElementById("chapterLabel"),
  languageLabel: document.getElementById("languageLabel"),
  languageSelect: document.getElementById("languageSelect"),
  soundBtn: document.getElementById("soundBtn"),
  stageSelectBtn: document.getElementById("stageSelectBtn"),
  hubLink: document.getElementById("hubLink"),
  glassRouteLink: document.getElementById("glassRouteLink"),
  stageId: document.getElementById("stageId"),
  stageTitle: document.getElementById("stageTitle"),
  stageIntro: document.getElementById("stageIntro"),
  stars: document.getElementById("stars"),
  currentStarsLabel: document.getElementById("currentStarsLabel"),
  campaignProgress: document.getElementById("campaignProgress"),
  board: document.getElementById("board"),
  statusBox: document.getElementById("statusBox"),
  statusTitle: document.getElementById("statusTitle"),
  statusText: document.getElementById("statusText"),
  rotationsLabel: document.getElementById("rotationsLabel"),
  rotationsValue: document.getElementById("rotationsValue"),
  targetLabel: document.getElementById("targetLabel"),
  targetValue: document.getElementById("targetValue"),
  hintUsedLabel: document.getElementById("hintUsedLabel"),
  hintUsedValue: document.getElementById("hintUsedValue"),
  shotControl: document.getElementById("mirrorShotControl"),
  shotsLabel: document.getElementById("mirrorShotsLabel"),
  shotsValue: document.getElementById("mirrorShotsValue"),
  fireBtn: document.getElementById("fireMirrorBtn"),
  objectiveTracker: document.getElementById("objectiveTracker"),
  objectiveTrackerLabel: document.getElementById("objectiveTrackerLabel"),
  objectiveSteps: document.getElementById("objectiveSteps"),
  rotateBtn: document.getElementById("rotateBtn"),
  resetBtn: document.getElementById("resetBtn"),
  hintBtn: document.getElementById("hintBtn"),
  prevBtn: document.getElementById("prevBtn"),
  nextBtn: document.getElementById("nextBtn"),
  noteTitle: document.getElementById("noteTitle"),
  noteText: document.getElementById("noteText"),
  effectLayer: document.getElementById("effectLayer"),
  stageModal: document.getElementById("stageModal"),
  stageModalEyebrow: document.getElementById("stageModalEyebrow"),
  stageModalTitle: document.getElementById("stageModalTitle"),
  progressSummary: document.getElementById("progressSummary"),
  stageSelectGrid: document.getElementById("stageSelectGrid"),
  closeStageModalBtn: document.getElementById("closeStageModalBtn"),
  resetProgressBtn: document.getElementById("resetProgressBtn"),
  challengeStrip: document.getElementById("challengeStrip"),
  challengeLabel: document.getElementById("challengeLabel"),
  challengeText: document.getElementById("challengeText"),
  challengeStatus: document.getElementById("challengeStatus"),
  chapterModal: document.getElementById("chapterModal"),
  chapterCompleteEyebrow: document.getElementById("chapterCompleteEyebrow"),
  chapterCompleteTitle: document.getElementById("chapterCompleteTitle"),
  chapterCompleteText: document.getElementById("chapterCompleteText"),
  chapterStarsLabel: document.getElementById("chapterStarsLabel"),
  chapterStarsValue: document.getElementById("chapterStarsValue"),
  chapterChallengesLabel: document.getElementById("chapterChallengesLabel"),
  chapterChallengesValue: document.getElementById("chapterChallengesValue"),
  chapterMapBtn: document.getElementById("chapterMapBtn"),
  closeChapterBtn: document.getElementById("closeChapterBtn")
};

let audioContext = null;
let effectTimer = null;
let modalReturnFocus = null;
let chapterTimer = null;
let chapterReturnFocus = null;

function t(key) {
  return TEXT[state.lang][key];
}

function gameUrl(path) {
  return window.PhotonHeistBridge?.withLanguage(path, state.lang) || path;
}

function setLanguage(lang) {
  state.lang = lang === "en" ? "en" : "ko";
  window.PhotonHeistBridge?.saveLanguage(state.lang);
  document.documentElement.lang = state.lang;
  renderAll();
  window.PhotonHeistBridge?.reportHeight();
}

function loadLevel(index) {
  clearBoardEffects();
  if (chapterTimer) window.clearTimeout(chapterTimer);
  chapterTimer = null;
  state.levelIndex = Math.max(0, Math.min(LEVELS.length - 1, index));
  state.level = LEVELS[state.levelIndex];
  state.grid = makeGridFromLevel(state.level);
  state.laser = { ...state.level.laser };
  state.selected = null;
  state.rotations = 0;
  state.shots = 0;
  state.committed = false;
  state.shotHistory = [];
  state.keyCollected = false;
  state.objectiveIndex = 0;
  state.hintIndex = 0;
  state.usedHint = false;
  state.cleared = false;
  state.alarm = false;
  state.lastStars = 0;
  state.rotatedMirrors = new Set();
  state.alarmsTriggered = 0;
  evaluate();
  renderAll();
  if (state.cleared) {
    effectTimer = window.setTimeout(() => celebrateSuccess(false), 120);
  }
}

function selectMirror(x, y) {
  state.selected = { x, y, type: "mirror" };
  renderAll();
  tinyBeep(520, 0.035);
}

function selectLaser(x, y) {
  state.selected = { x, y, type: "laser" };
  renderAll();
  tinyBeep(520, 0.035);
}

function rotateSelected() {
  if (!state.selected) {
    showMessage("standby", t("standbyTitle"), t("selectMirror"));
    tinyBeep(180, 0.05);
    return;
  }
  const { x, y } = state.selected;
  const cell = state.grid[y][x];
  const isMirror = cell === "/" || cell === "\\" || (cell === "m" && state.level.stowableMirrors);
  const isRotatableLaser = cell === "L" && state.level.rotatableLaser;
  if (!isMirror && !isRotatableLaser) return;
  const wasCleared = state.cleared;
  const previousAlarm = [...state.ray.alarmSensors][0] || null;
  if (isMirror) {
    state.grid[y][x] = state.level.stowableMirrors
      ? ({ m: "/", "/": "\\", "\\": "m" }[cell])
      : (cell === "/" ? "\\" : "/");
    state.rotatedMirrors.add(`${x},${y}`);
  } else {
    const directions = ["R", "D", "L", "U"];
    state.laser.dir = directions[(directions.indexOf(state.laser.dir) + 1) % directions.length];
  }
  state.rotations += 1;
  if (state.level.commitMode) state.committed = false;
  evaluate();
  const currentAlarm = [...state.ray.alarmSensors][0] || null;
  if (state.alarm && currentAlarm !== previousAlarm) state.alarmsTriggered += 1;
  renderAll(true);
  if (state.cleared && !wasCleared) {
    celebrateSuccess(true);
    scheduleChapterComplete();
  } else if (state.alarm && currentAlarm !== previousAlarm) {
    triggerAlarmEffect();
    playAlarmSound();
  } else {
    tinyBeep(760, 0.045);
  }
}

function fireMirrorLaser() {
  const budget = state.level.shotBudget;
  if (!state.level.commitMode || state.cleared || (budget && state.shots >= budget)) return;
  const previousAlarm = [...state.ray.alarmSensors][0] || null;
  state.committed = true;
  state.shots += 1;
  evaluate();
  const sequence = state.level.objectiveSequence || (state.level.sequentialKey ? ["K", "S"] : ["S"]);
  const expected = sequence[state.objectiveIndex];
  const objectiveHit = expected === "K"
    ? state.ray.keySensors.size
    : expected === "Q"
      ? state.ray.secondaryKeySensors.size
      : state.ray.activeSensors.size;
  if (expected !== "S" && objectiveHit && !state.alarm) {
    state.shotHistory.push(state.ray.path.map(step => ({ ...step })));
    state.grid = state.grid.map(row => row.map(cell => cell === expected ? "." : cell));
    state.objectiveIndex += 1;
    state.keyCollected = state.objectiveIndex > 0;
    state.committed = false;
    evaluate();
    renderAll(true);
    tinyBeep(1040, 0.12);
    return;
  }
  if (!state.cleared) {
    state.shotHistory.push(state.ray.path.map(step => ({ ...step })));
  }
  const currentAlarm = [...state.ray.alarmSensors][0] || null;
  if (state.alarm && currentAlarm !== previousAlarm) state.alarmsTriggered += 1;
  renderAll(true);
  if (state.cleared) {
    celebrateSuccess(true);
    scheduleChapterComplete();
  } else if (state.alarm) {
    triggerAlarmEffect();
    playAlarmSound();
  } else {
    tinyBeep(860, 0.08);
  }
}

function useHint() {
  const hints = state.level.hints[state.lang];
  if (state.hintIndex >= hints.length) {
    showMessage("standby", `${t("hintPrefix")}`, t("noMoreHints"));
    return;
  }
  state.usedHint = true;
  const message = hints[state.hintIndex];
  state.hintIndex += 1;
  showMessage("standby", `${t("hintPrefix")} ${state.hintIndex}`, message);
  renderStats();
  tinyBeep(420, 0.06);
}

function resetLevel() {
  loadLevel(state.levelIndex);
}

function calculateStars() {
  if (!state.cleared) return 0;
  let stars = 1;
  const efficientShots = !state.level.commitMode || state.shots <= (state.level.targetShots || 1);
  if (state.rotations <= state.level.targetRotations && efficientShots) stars += 1;
  if (!state.usedHint) stars += 1;
  return stars;
}

function evaluate() {
  state.ray = castRay(state.grid, state.laser);
  const resolved = !state.level.commitMode || state.committed;
  state.alarm = resolved && state.ray.alarmSensors.size > 0;
  const sequence = state.level.objectiveSequence || (state.level.sequentialKey ? ["K", "S"] : ["S"]);
  const objectiveReady = sequence[state.objectiveIndex] === "S";
  state.cleared = resolved && objectiveReady && state.ray.activeSensors.size > 0 && !state.alarm;
  state.lastStars = calculateStars();
  if (state.cleared) recordLevelCompletion();
}

function showMessage(kind, title, text) {
  el.statusBox.classList.remove("success", "alarm");
  if (kind === "success") el.statusBox.classList.add("success");
  if (kind === "alarm") el.statusBox.classList.add("alarm");
  el.statusTitle.textContent = title;
  el.statusText.textContent = text;
}

function renderHeader() {
  el.gameTitle.textContent = t("gameTitle");
  el.chapterLabel.textContent = t("chapter");
  el.languageLabel.textContent = t("language");
  el.stageId.textContent = `Stage ${state.level.id}`;
  el.stageTitle.textContent = state.level.title[state.lang];
  el.stageIntro.textContent = state.level.intro[state.lang];
  const adjustKey = !state.level.stowableMirrors
    ? "rotate"
    : state.selected?.type === "laser"
      ? "cycleLaser"
      : state.selected?.type === "mirror"
        ? "cycleMirror"
        : "cycleDevice";
  el.rotateBtn.textContent = t(adjustKey);
  el.resetBtn.textContent = t("reset");
  el.hintBtn.textContent = t("hint");
  el.prevBtn.textContent = t("prev");
  el.nextBtn.textContent = t("next");
  el.stageSelectBtn.textContent = t("stageSelect");
  el.shotsLabel.textContent = t("shots");
  el.fireBtn.textContent = t("fire");
  el.hubLink.textContent = t("hub");
  el.glassRouteLink.textContent = t("glassRoute");
  el.hubLink.href = gameUrl("hub.html");
  el.glassRouteLink.href = gameUrl("glass.html");
  el.soundBtn.textContent = state.soundEnabled ? t("soundOn") : t("soundOff");
  el.soundBtn.setAttribute("aria-label", t("soundLabel"));
  el.soundBtn.setAttribute("aria-pressed", String(state.soundEnabled));
  el.stageModalEyebrow.textContent = t("missionMap");
  el.stageModalTitle.textContent = t("stageSelectTitle");
  el.closeStageModalBtn.setAttribute("aria-label", t("close"));
  el.resetProgressBtn.textContent = t("resetProgress");
  el.challengeLabel.textContent = t("challenge");
  el.chapterCompleteEyebrow.textContent = t("chapterCompleteEyebrow");
  el.chapterCompleteTitle.textContent = t("chapterCompleteTitle");
  el.chapterCompleteText.textContent = t("chapterCompleteText");
  el.chapterStarsLabel.textContent = t("totalStars");
  el.chapterChallengesLabel.textContent = t("challenges");
  el.chapterMapBtn.textContent = t("chapterMap");
  el.closeChapterBtn.textContent = t("continuePlaying");
}

function renderChallenge() {
  const complete = Boolean(state.progress.challenges[state.level.id]);
  el.challengeText.textContent = state.level.challenge[state.lang];
  el.challengeStatus.textContent = complete ? t("challengeComplete") : t("challengeRetry");
  el.challengeStrip.classList.toggle("complete", complete);
  el.challengeStrip.querySelector(".challenge-icon").textContent = complete ? "OK" : "!";
}

function renderStats() {
  const totals = progressTotals();
  el.rotationsLabel.textContent = t(state.level.stowableMirrors ? "actions" : "rotations");
  el.rotationsValue.textContent = state.rotations;
  el.targetLabel.textContent = t("target");
  el.targetValue.textContent = state.level.targetRotations;
  el.hintUsedLabel.textContent = t("hintUsed");
  el.hintUsedValue.textContent = state.hintIndex;
  el.shotsValue.textContent = `${state.shots} / ${state.level.shotBudget || "∞"}`;
  el.stars.textContent = renderStars(state.lastStars);
  el.stars.setAttribute("aria-label", `${t("starsLabel")}: ${state.lastStars}/3`);
  el.currentStarsLabel.textContent = t("currentMissionStars");
  el.campaignProgress.textContent = `${t("campaignTotal")} *${totals.stars}/${LEVELS.length * 3} - ${totals.challenges}/${LEVELS.length}`;
}

function renderStatus() {
  const sequence = state.level.objectiveSequence || (state.level.sequentialKey ? ["K", "S"] : ["S"]);
  const expected = sequence[state.objectiveIndex];
  const wrongObjectiveHit = state.committed && !state.cleared && (
    (state.ray.keySensors.size && expected !== "K")
    || (state.ray.secondaryKeySensors.size && expected !== "Q")
    || (state.ray.activeSensors.size && expected !== "S")
  );
  if (state.cleared) {
    const clearTitleKey = state.lastStars === 3 ? "perfectClearTitle" : state.lastStars === 2 ? "solidClearTitle" : "basicClearTitle";
    const resultParts = state.lang === "ko"
      ? [`조작 ${state.rotations}/${state.level.targetRotations}`]
      : [`Actions ${state.rotations}/${state.level.targetRotations}`];
    if (state.level.commitMode) {
      resultParts.push(state.lang === "ko"
        ? `발사 ${state.shots}/${state.level.targetShots || state.level.shotBudget}`
        : `Shots ${state.shots}/${state.level.targetShots || state.level.shotBudget}`);
    }
    resultParts.push(state.lang === "ko"
      ? (state.usedHint ? `힌트 ${state.hintIndex}개` : "힌트 없음")
      : (state.usedHint ? `Hints ${state.hintIndex}` : "No hints"));
    showMessage("success", t(clearTitleKey), resultParts.join(" - "));
    el.noteText.textContent = state.level.successNote[state.lang];
  } else if (state.alarm) {
    showMessage("alarm", t("alarmTitle"), t("alarmText"));
    el.noteText.textContent = t("noteDefault");
  } else if (wrongObjectiveHit) {
    const remainingShots = (state.level.shotBudget || Infinity) - state.shots;
    const remainingObjectives = sequence.length - state.objectiveIndex;
    const cannotFinish = remainingShots < remainingObjectives;
    showMessage("standby", t(cannotFinish ? "sequenceFailedTitle" : "wrongObjectiveTitle"), t(cannotFinish ? "sequenceFailedText" : "wrongObjectiveText"));
    el.noteText.textContent = t("noteDefault");
  } else if (state.ray.loop && (!state.level.commitMode || state.committed)) {
    showMessage("alarm", t("loopTitle"), t("loopText"));
    el.noteText.textContent = t("noteDefault");
  } else if ((state.level.sequentialKey || state.level.objectiveSequence) && state.objectiveIndex > 0 && !state.committed) {
    const threeStage = (state.level.objectiveSequence || []).length === 3;
    const titleKey = threeStage ? (state.objectiveIndex === 1 ? "firstKeyTitle" : "secondKeyTitle") : "keyAcquiredTitle";
    const textKey = threeStage ? (state.objectiveIndex === 1 ? "firstKeyText" : "secondKeyText") : "keyAcquiredText";
    showMessage("standby", t(titleKey), t(textKey));
    el.noteText.textContent = t("noteDefault");
  } else if (state.level.commitMode && !state.committed) {
    const exhausted = state.level.shotBudget && state.shots >= state.level.shotBudget;
    showMessage("standby", t(exhausted ? "shotsExhaustedTitle" : "planningTitle"), t(exhausted ? "shotsExhaustedText" : "planningText"));
    el.noteText.textContent = t("noteDefault");
  } else if (state.level.commitMode) {
    showMessage("standby", t("shotResultTitle"), t("shotResultText"));
    el.noteText.textContent = t("noteDefault");
  } else {
    showMessage("standby", t("blockedTitle"), t("blockedText"));
    el.noteText.textContent = t("noteDefault");
  }
  el.noteTitle.textContent = t("noteTitle");
}

function renderObjectiveTracker() {
  const sequence = state.level.objectiveSequence || (state.level.sequentialKey ? ["K", "S"] : []);
  el.objectiveTracker.hidden = sequence.length < 2;
  if (sequence.length < 2) return;
  el.objectiveTrackerLabel.textContent = t("objectiveSequence");
  el.objectiveSteps.innerHTML = "";
  const labels = { K: t("yellowKey"), Q: t("cyanKey"), S: t("exitObjective") };
  const icons = { K: "K", Q: "Q", S: "S" };
  sequence.forEach((objective, index) => {
    const status = index < state.objectiveIndex ? "complete" : index === state.objectiveIndex ? "current" : "pending";
    const step = document.createElement("div");
    step.className = `objective-step ${status} objective-${objective.toLowerCase()}`;
    step.setAttribute("aria-label", `${labels[objective]}: ${t(status === "complete" ? "objectiveDone" : status === "current" ? "objectiveCurrent" : "objectivePending")}`);
    step.innerHTML = `<span class="objective-symbol" aria-hidden="true">${status === "complete" ? "OK" : icons[objective]}</span><span>${labels[objective]}</span>`;
    el.objectiveSteps.appendChild(step);
    if (index < sequence.length - 1) {
      const arrow = document.createElement("span");
      arrow.className = "objective-arrow";
      arrow.setAttribute("aria-hidden", "true");
      arrow.textContent = ">";
      el.objectiveSteps.appendChild(arrow);
    }
  });
}

function renderButtons() {
  el.shotControl.hidden = !state.level.commitMode;
  const budgetSpent = state.level.shotBudget && state.shots >= state.level.shotBudget;
  el.fireBtn.disabled = !state.level.commitMode || state.cleared || Boolean(budgetSpent);
  el.prevBtn.disabled = state.levelIndex === 0;
  const nextAccessible = canAccessLevel(state.levelIndex + 1);
  el.nextBtn.disabled = state.levelIndex === LEVELS.length - 1 || !nextAccessible;
  el.nextBtn.classList.toggle("ready", state.cleared && state.levelIndex < LEVELS.length - 1 && nextAccessible);
}

function renderAll(animate = false) {
  renderHeader();
  renderStats();
  renderChallenge();
  renderStatus();
  renderObjectiveTracker();
  renderButtons();
  renderBoard(el.board, {
    ...state,
    actions: {
      selectMirror,
      selectLaser
    }
  });
  if (!el.stageModal.hidden) renderStageSelector();
  if (animate) {
    el.board.classList.remove("pulse");
    void el.board.offsetWidth;
    el.board.classList.add("pulse");
  }
}

function loadSoundPreference() {
  try {
    return localStorage.getItem("photonHeistSound") !== "off";
  } catch (_) {
    return true;
  }
}

function defaultProgress() {
  return { version: 2, bestStars: {}, bestRotations: {}, bestShots: {}, challenges: {}, unlockedIndex: 0 };
}

function loadProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem("photonHeistProgressV1"));
    if (!saved || typeof saved !== "object") return defaultProgress();
    const bestStars = {};
    const bestRotations = {};
    const bestShots = {};
    const challenges = {};
    LEVELS.forEach(level => {
      const stars = Number(saved.bestStars?.[level.id] || 0);
      const rotations = Number(saved.bestRotations?.[level.id]);
      const shots = Number(saved.bestShots?.[level.id]);
      if (stars >= 1 && stars <= 3) bestStars[level.id] = Math.floor(stars);
      if (Number.isFinite(rotations) && rotations >= 0) bestRotations[level.id] = Math.floor(rotations);
      if (Number.isFinite(shots) && shots >= 1) bestShots[level.id] = Math.floor(shots);
      if (saved.challenges?.[level.id] === true) challenges[level.id] = true;
    });
    return {
      version: 2,
      bestStars,
      bestRotations,
      bestShots,
      challenges,
      unlockedIndex: Math.max(0, Math.min(LEVELS.length - 1, Number(saved.unlockedIndex) || 0))
    };
  } catch (_) {
    return defaultProgress();
  }
}

function saveProgress() {
  try {
    localStorage.setItem("photonHeistProgressV1", JSON.stringify(state.progress));
  } catch (_) {
    // Progress saving is optional when storage is unavailable.
  }
}

function canAccessLevel(index) {
  return index >= 0 && index < LEVELS.length && index <= state.progress.unlockedIndex;
}

function recordLevelCompletion() {
  const id = state.level.id;
  const previousBest = state.progress.bestStars[id] || 0;
  const nextUnlocked = Math.min(LEVELS.length - 1, state.levelIndex + 1);
  let changed = false;

  if (state.lastStars > previousBest) {
    state.progress.bestStars[id] = state.lastStars;
    changed = true;
  }
  const previousRotations = state.progress.bestRotations[id];
  if (previousRotations === undefined || state.rotations < previousRotations) {
    state.progress.bestRotations[id] = state.rotations;
    changed = true;
  }
  if (state.level.commitMode) {
    const previousShots = state.progress.bestShots[id];
    if (previousShots === undefined || state.shots < previousShots) {
      state.progress.bestShots[id] = state.shots;
      changed = true;
    }
  }
  if (nextUnlocked > state.progress.unlockedIndex) {
    state.progress.unlockedIndex = nextUnlocked;
    changed = true;
  }
  if (challengeAchieved() && !state.progress.challenges[id]) {
    state.progress.challenges[id] = true;
    changed = true;
  }
  if (changed) saveProgress();
}

function challengeAchieved() {
  const challenge = state.level.challenge;
  if (!state.cleared || !challenge) return false;
  if (challenge.maxRotations !== undefined && state.rotations > challenge.maxRotations) return false;
  if (challenge.noHint && state.usedHint) return false;
  if (challenge.maxMirrorsTouched !== undefined && state.rotatedMirrors.size > challenge.maxMirrorsTouched) return false;
  if (challenge.maxAlarms !== undefined && state.alarmsTriggered > challenge.maxAlarms) return false;
  if (challenge.maxShots !== undefined && state.shots > challenge.maxShots) return false;
  return true;
}

function progressTotals() {
  const stars = LEVELS.reduce((total, level) => total + (state.progress.bestStars[level.id] || 0), 0);
  const completed = LEVELS.filter(level => (state.progress.bestStars[level.id] || 0) > 0).length;
  const challenges = LEVELS.filter(level => state.progress.challenges[level.id]).length;
  return { stars, completed, challenges };
}

function makeStageCard(level, index) {
  const unlocked = canAccessLevel(index);
  const best = state.progress.bestStars[level.id] || 0;
  const challengeDone = Boolean(state.progress.challenges[level.id]);
  const bestRotations = state.progress.bestRotations[level.id];
  const bestShots = state.progress.bestShots[level.id];
  const button = document.createElement("button");
  button.type = "button";
  button.className = "stage-select-item";
  button.classList.toggle("locked", !unlocked);
  button.classList.toggle("complete", best > 0);
  button.classList.toggle("current", index === state.levelIndex);
  button.disabled = !unlocked;

  const top = document.createElement("span");
  top.className = "stage-select-item-top";
  const stageId = document.createElement("span");
  stageId.textContent = `Stage ${level.id}`;
  const stateIcon = document.createElement("span");
  stateIcon.textContent = unlocked ? `${best > 0 ? "*" : ""}${challengeDone ? " OK" : ""}` : "LOCK";
  top.append(stageId, stateIcon);

  const title = document.createElement("strong");
  title.textContent = level.title[state.lang];
  const stars = document.createElement("span");
  stars.className = "stage-best-stars";
  stars.textContent = renderStars(best);
  const performance = document.createElement("span");
  performance.className = "stage-best-performance";
  if (best > 0 && bestRotations !== undefined) {
    const parts = state.lang === "ko" ? [`Best ${bestRotations} actions`] : [`Best ${bestRotations} actions`];
    if (level.commitMode && bestShots !== undefined) parts.push(state.lang === "ko" ? `${bestShots} shots` : `${bestShots} shots`);
    performance.textContent = parts.join(" - ");
  }
  const status = document.createElement("small");
  const statusParts = [];
  if (!unlocked) statusParts.push(t("locked"));
  if (index === state.levelIndex && unlocked) statusParts.push(t("currentStage"));
  if (best > 0 && index !== state.levelIndex) statusParts.push(t("replayStage"));
  if (challengeDone) statusParts.push(`${t("challenge")} OK`);
  status.textContent = statusParts.join(" - ");

  button.append(top, title, stars, performance, status);
  if (unlocked) {
    button.addEventListener("click", () => {
      closeStageModal();
      loadLevel(index);
    });
  }
  return button;
}

function renderStageSelector() {
  const { stars, completed, challenges } = progressTotals();
  el.progressSummary.textContent = state.lang === "ko"
    ? `${completed}/${LEVELS.length} ${t("completed")} · ${t("totalStars")} ${stars}/${LEVELS.length * 3} · ${t("challenges")} ${challenges}/${LEVELS.length}`
    : `${completed}/${LEVELS.length} ${t("completed")} · ${stars}/${LEVELS.length * 3} ${t("totalStars")} · ${challenges}/${LEVELS.length} ${t("challenges")}`;
  el.stageSelectGrid.replaceChildren(...LEVELS.map(makeStageCard));
}

function openStageModal() {
  modalReturnFocus = document.activeElement;
  renderStageSelector();
  el.stageModal.hidden = false;
  document.body.classList.add("modal-open");
  el.closeStageModalBtn.focus();
}

function closeStageModal() {
  el.stageModal.hidden = true;
  document.body.classList.remove("modal-open");
  if (modalReturnFocus instanceof HTMLElement) modalReturnFocus.focus();
  modalReturnFocus = null;
}

function resetProgress() {
  if (!window.confirm(t("resetProgressConfirm"))) return;
  state.progress = defaultProgress();
  saveProgress();
  closeStageModal();
  loadLevel(0);
}

function scheduleChapterComplete() {
  if (state.levelIndex !== LEVELS.length - 1 || !state.cleared) return;
  if (chapterTimer) window.clearTimeout(chapterTimer);
  chapterTimer = window.setTimeout(showChapterComplete, 1650);
}

function showChapterComplete() {
  chapterTimer = null;
  const { stars, challenges } = progressTotals();
  chapterReturnFocus = document.activeElement;
  el.chapterStarsValue.textContent = `${stars}/${LEVELS.length * 3}`;
  el.chapterChallengesValue.textContent = `${challenges}/${LEVELS.length}`;
  el.chapterModal.hidden = false;
  document.body.classList.add("modal-open");
  el.chapterMapBtn.focus();
}

function closeChapterModal() {
  el.chapterModal.hidden = true;
  if (el.stageModal.hidden) document.body.classList.remove("modal-open");
  if (chapterReturnFocus instanceof HTMLElement) chapterReturnFocus.focus();
  chapterReturnFocus = null;
}

function openMapFromChapter() {
  closeChapterModal();
  openStageModal();
}

function setSoundEnabled(enabled) {
  state.soundEnabled = enabled;
  try {
    localStorage.setItem("photonHeistSound", enabled ? "on" : "off");
  } catch (_) {
    // The game also works when storage is unavailable.
  }
  renderHeader();
  if (enabled) tinyBeep(660, 0.07);
}

function getAudioContext() {
  if (!state.soundEnabled) return null;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if (!AudioContext) return null;
  if (!audioContext) audioContext = new AudioContext();
  if (audioContext.state === "suspended") audioContext.resume();
  return audioContext;
}

function playTone(freq, start = 0, duration = 0.08, type = "sine", volume = 0.035) {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const beginsAt = ctx.currentTime + start;
    const endsAt = beginsAt + duration;
    osc.type = type;
    osc.frequency.setValueAtTime(freq, beginsAt);
    gain.gain.setValueAtTime(0.0001, beginsAt);
    gain.gain.exponentialRampToValueAtTime(volume, beginsAt + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, endsAt);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(beginsAt);
    osc.stop(endsAt + 0.02);
  } catch (_) {
    // Audio feedback is optional and never blocks the puzzle.
  }
}

function tinyBeep(freq = 600, duration = 0.04) {
  playTone(freq, 0, duration, "sine", 0.028);
}

function playSuccessSound() {
  playTone(523.25, 0, 0.18, "sine", 0.04);
  playTone(659.25, 0.09, 0.2, "sine", 0.045);
  playTone(783.99, 0.18, 0.22, "triangle", 0.05);
  playTone(1046.5, 0.32, 0.35, "triangle", 0.055);
}

function playAlarmSound() {
  playTone(220, 0, 0.16, "sawtooth", 0.035);
  playTone(164.81, 0.14, 0.22, "sawtooth", 0.04);
}

function clearBoardEffects() {
  if (effectTimer) window.clearTimeout(effectTimer);
  effectTimer = null;
  el.effectLayer.replaceChildren();
  el.board.classList.remove("success-burst", "alarm-shake");
}

function makeEffectBanner(kind, text) {
  const banner = document.createElement("strong");
  banner.className = `effect-banner ${kind}`;
  banner.textContent = text;
  return banner;
}

function celebrateSuccess(withSound = true) {
  clearBoardEffects();
  el.board.classList.add("success-burst");
  el.effectLayer.appendChild(makeEffectBanner("success", t("successBurst")));

  for (let i = 0; i < 18; i += 1) {
    const particle = document.createElement("span");
    particle.className = "success-particle";
    particle.style.setProperty("--particle-angle", `${i * 20}deg`);
    particle.style.setProperty("--particle-distance", `${92 + (i % 4) * 18}px`);
    particle.style.setProperty("--particle-delay", `${(i % 3) * 35}ms`);
    el.effectLayer.appendChild(particle);
  }

  if (withSound) playSuccessSound();
  effectTimer = window.setTimeout(clearBoardEffects, 1500);
}

function triggerAlarmEffect() {
  clearBoardEffects();
  el.board.classList.add("alarm-shake");
  el.effectLayer.appendChild(makeEffectBanner("alarm", t("alarmBurst")));
  effectTimer = window.setTimeout(clearBoardEffects, 850);
}

el.languageSelect.addEventListener("change", event => setLanguage(event.target.value));
window.addEventListener("photonheist:language", event => setLanguage(event.detail.lang));
el.soundBtn.addEventListener("click", () => setSoundEnabled(!state.soundEnabled));
el.stageSelectBtn.addEventListener("click", openStageModal);
el.closeStageModalBtn.addEventListener("click", closeStageModal);
el.resetProgressBtn.addEventListener("click", resetProgress);
el.chapterMapBtn.addEventListener("click", openMapFromChapter);
el.closeChapterBtn.addEventListener("click", closeChapterModal);
el.chapterModal.addEventListener("click", event => {
  if (event.target === el.chapterModal) closeChapterModal();
});
el.stageModal.addEventListener("click", event => {
  if (event.target === el.stageModal) closeStageModal();
});
el.rotateBtn.addEventListener("click", rotateSelected);
el.fireBtn.addEventListener("click", fireMirrorLaser);
el.resetBtn.addEventListener("click", resetLevel);
el.hintBtn.addEventListener("click", useHint);
el.prevBtn.addEventListener("click", () => loadLevel(state.levelIndex - 1));
el.nextBtn.addEventListener("click", () => loadLevel(state.levelIndex + 1));

document.addEventListener("keydown", event => {
  if (event.key === "Escape" && !el.chapterModal.hidden) {
    closeChapterModal();
    return;
  }
  if (event.key === "Escape" && !el.stageModal.hidden) {
    closeStageModal();
    return;
  }
  if (!el.stageModal.hidden || !el.chapterModal.hidden) return;
  if (event.key.toLowerCase() === "r") rotateSelected();
  if ((event.key === "Enter" || event.key === " ") && state.level.commitMode) {
    event.preventDefault();
    fireMirrorLaser();
  }
  if (event.key === "ArrowRight" && canAccessLevel(state.levelIndex + 1)) loadLevel(state.levelIndex + 1);
  if (event.key === "ArrowLeft" && state.levelIndex > 0) loadLevel(state.levelIndex - 1);
});

loadLevel(0);
