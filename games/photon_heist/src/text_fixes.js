(function () {
  "use strict";

  function applyMap(target, values) {
    if (!target || !values) return;
    Object.keys(values).forEach(function (key) {
      target[key] = values[key];
    });
  }

  function patchHubText() {
    if (typeof HUB_TEXT === "undefined") return;
    applyMap(HUB_TEXT.ko, {
      eyebrow: "PHOTON HEIST · 작전 본부",
      title: "빛의 규칙을 훔쳐라",
      intro: "고전 광학에서 시작해 양자정보 작전까지 이어지는 캠페인이다.",
      language: "언어",
      completed: "완료 작전",
      stars: "획득 별",
      next: "다음 목표",
      route: "캠페인 경로",
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
    });
    applyMap(HUB_TEXT.en, {
      eyebrow: "PHOTON HEIST · OPERATIONS HQ",
      route: "CAMPAIGN ROUTE"
    });
  }

  window.applyPhotonHeistTextFixes = patchHubText;
  window.applyPhotonHeistGlassTextFixes = function () {};
  patchHubText();
})();
