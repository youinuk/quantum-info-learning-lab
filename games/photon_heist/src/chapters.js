const PHOTON_CHAPTERS = [
  {
    id: "mirror",
    order: 1,
    icon: "M",
    accent: "#ff6680",
    file: "index.html",
    progressKey: "photonHeistProgressV1",
    stageCount: 10,
    requiredStageIds: ["3-2"],
    title: { ko: "거울 작전", en: "Mirror Mission" },
    concept: { ko: "직진 · 반사", en: "Straight paths · Reflection" },
    description: {
      ko: "거울 각도를 바꾸어 빛의 경로를 설계하고 보안망을 통과한다.",
      en: "Design reflected light paths and evade security grids."
    }
  },
  {
    id: "glass",
    order: 2,
    icon: "G",
    accent: "#78d9ff",
    file: "glass.html",
    progressKey: "photonHeistGlassProgressV1",
    stageCount: 10,
    requiredStageIds: ["G2-2"],
    prerequisite: { chapterId: "mirror", requiredStageIds: ["3-2"] },
    title: { ko: "유리 작전", en: "Glass Route" },
    concept: { ko: "굴절 · 전반사 · 복합 경로", en: "Refraction · TIR · Mixed paths" },
    description: {
      ko: "발사 전에 경로를 예측하고 유리와 거울을 순서대로 이용한다.",
      en: "Predict before firing and combine glass with mirrors in sequence."
    }
  },
  {
    id: "focus",
    order: 3,
    icon: "F",
    accent: "#a78bfa",
    stageCount: 8,
    available: false,
    prerequisite: { chapterId: "glass", requiredStageIds: ["G2-2"] },
    title: { ko: "초점 작전", en: "Focus Job" },
    concept: { ko: "볼록·오목 렌즈 · 초점", en: "Convex/concave lenses · Focus" },
    description: { ko: "여러 광선을 모으거나 퍼뜨려 정확한 상을 만든다.", en: "Converge or spread ray bundles to form an image." }
  },
  {
    id: "spectrum",
    order: 4,
    icon: "S",
    accent: "#fb7185",
    stageCount: 8,
    available: false,
    title: { ko: "스펙트럼 금고", en: "Spectrum Vault" },
    concept: { ko: "프리즘 · 파장 · 색 분리", en: "Prisms · Wavelength · Dispersion" },
    description: { ko: "색마다 다른 굴절 경로를 이용해 금고를 연다.", en: "Exploit wavelength-dependent paths to open the vault." }
  },
  {
    id: "polarization",
    order: 5,
    icon: "P",
    accent: "#fbbf24",
    stageCount: 8,
    available: false,
    title: { ko: "편광 암호", en: "Polarization Cipher" },
    concept: { ko: "편광 · 필터 각도 · 측정 기준", en: "Polarization · Filters · Bases" },
    description: { ko: "빛의 진동 방향을 선택해 숨겨진 신호를 복원한다.", en: "Select vibration directions to recover hidden signals." }
  },
  {
    id: "wave",
    order: 6,
    icon: "W",
    accent: "#34d399",
    stageCount: 10,
    available: false,
    title: { ko: "파동 프로토콜", en: "Wave Protocol" },
    concept: { ko: "간섭 · 위상 · 회절", en: "Interference · Phase · Diffraction" },
    description: { ko: "빛을 겹치고 퍼뜨려 밝고 어두운 암호 무늬를 만든다.", en: "Overlap and diffract light into coded bright and dark patterns." }
  },
  {
    id: "photon",
    order: 7,
    icon: "Q",
    accent: "#60a5fa",
    stageCount: 10,
    available: false,
    title: { ko: "광자 작전", en: "Photon Operations" },
    concept: { ko: "광자 · 확률 · 반복 측정", en: "Photons · Probability · Repeated measurement" },
    description: { ko: "한 번의 검출과 반복 실험으로 확률 정보를 읽는다.", en: "Read probabilistic information through single detections and trials." }
  },
  {
    id: "quantum",
    order: 8,
    icon: "QI",
    accent: "#f472b6",
    stageCount: 10,
    available: false,
    title: { ko: "양자 하이스트", en: "Quantum Heist" },
    concept: { ko: "큐비트 · 중첩 · 측정 · BB84", en: "Qubits · Superposition · Measurement · BB84" },
    description: { ko: "앞에서 익힌 광학 장치를 양자정보 작전으로 다시 해석한다.", en: "Reinterpret earlier optical devices as quantum-information operations." }
  }
];
