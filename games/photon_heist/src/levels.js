const LEVELS = [
  {
    id: "0-1",
    title: { ko: "첫 번째 빛", en: "First Beam" },
    intro: {
      ko: "아무것도 건드리지 말고 빛이 어디로 가는지 관찰한다.",
      en: "Do not touch anything yet. Watch where the beam goes."
    },
    grid: [
      "........",
      "........",
      ".L....S.",
      "........",
      "........",
      "........",
      "........",
      "........"
    ],
    laser: { x: 1, y: 2, dir: "R" },
    targetRotations: 0,
    challenge: { ko: "빛의 직진을 확인하고 별 3개 받기", en: "Observe straight travel and earn three stars", maxRotations: 0, noHint: true },
    hints: {
      ko: ["빛은 막히지 않으면 곧게 나아간다.", "센서는 레이저의 오른쪽에 있다.", "이번 스테이지는 조작하지 않아도 성공한다."],
      en: ["Light travels straight when nothing blocks it.", "The sensor is to the right of the laser.", "You do not need to change anything in this stage."]
    },
    successNote: {
      ko: "빛은 아무것도 만나지 않으면 곧게 나아간다. 이것을 빛의 직진이라고 한다.",
      en: "Light travels in a straight line when nothing blocks it."
    }
  },
  {
    id: "0-2",
    title: { ko: "첫 번째 거울", en: "First Mirror" },
    intro: {
      ko: "거울을 한 번 돌려 빛을 위쪽 센서로 보낸다.",
      en: "Rotate the mirror once and send the beam to the upper sensor."
    },
    grid: [
      "........",
      "....S...",
      "........",
      "........",
      "........",
      ".L..\\...",
      "........",
      "........"
    ],
    laser: { x: 1, y: 5, dir: "R" },
    targetRotations: 1,
    challenge: { ko: "힌트 없이 거울을 정확히 한 번만 회전", en: "Rotate exactly once without a hint", maxRotations: 1, noHint: true, maxMirrorsTouched: 1 },
    hints: {
      ko: ["레이저는 오른쪽으로 출발한다.", "45도 거울은 오른쪽으로 오던 빛을 위로 보낸다.", "거울을 선택한 뒤 90도 회전을 누른다."],
      en: ["The laser starts to the right.", "A 45 degree mirror sends the right-moving beam upward.", "Select the mirror and press Rotate 90 degrees."]
    },
    successNote: {
      ko: "거울은 빛의 방향을 바꾼다. 빛이 거울에서 튕겨 나가는 현상을 반사라고 한다.",
      en: "A mirror changes the direction of light. This bouncing of light is called reflection."
    }
  },
  {
    id: "1-1",
    title: { ko: "막힌 길", en: "Blocked Path" },
    intro: {
      ko: "두 거울을 모두 사용해 벽 사이로 빛을 우회시킨다.",
      en: "Use both 45 degree and 135 degree mirrors to route the beam between two walls."
    },
    grid: [
      "........",
      "........",
      ".S./.#..",
      "........",
      "........",
      ".L.\\....",
      "...#....",
      "........"
    ],
    laser: { x: 1, y: 5, dir: "R" },
    targetRotations: 2,
    challenge: { ko: "힌트 없이 두 거울만 건드려 우회", en: "Detour by touching only two mirrors without hints", maxRotations: 2, noHint: true, maxMirrorsTouched: 2 },
    hints: {
      ko: ["아래쪽 거울이 빛을 위쪽 통로로 보낸다.", "아래 거울은 45도, 위 거울은 135도가 되도록 맞춘다.", "두 거울을 각각 한 번씩 회전한다."],
      en: ["The lower mirror sends the beam into the upper corridor.", "Set the lower mirror to 45 degrees and the upper mirror to 135 degrees.", "Rotate each mirror once."]
    },
    successNote: {
      ko: "벽은 빛을 통과시키지 않는다. 거울을 조합하면 막힌 길을 돌아갈 수 있다.",
      en: "Light cannot pass through walls, but mirrors at different angles can redirect it around obstacles."
    }
  },
  {
    id: "1-2",
    title: { ko: "빨간 경보", en: "Red Alert" },
    intro: {
      ko: "빨간 가짜 센서를 피하고 초록 목표 센서로 빛을 보낸다.",
      en: "Avoid the red fake sensor and send the beam to the green target."
    },
    grid: [
      "........",
      "....S...",
      "........",
      "........",
      "........",
      ".L..\\...",
      "....X...",
      "........"
    ],
    laser: { x: 1, y: 5, dir: "R" },
    targetRotations: 1,
    challenge: { ko: "한 번의 회전으로 빨간 경보 피하기", en: "Disable the red alarm with one rotation", maxRotations: 1, maxMirrorsTouched: 1 },
    hints: {
      ko: ["현재 빛은 빨간 X 센서로 향한다.", "빛을 아래가 아니라 위로 보내야 한다.", "거울을 45도로 바꾼다."],
      en: ["The current beam points toward the red X sensor.", "Send the beam upward instead of downward.", "Change the mirror to 45 degrees."]
    },
    successNote: {
      ko: "같은 출발점에서도 거울 각도에 따라 안전한 경로와 위험한 경로가 갈린다.",
      en: "A mirror angle can turn the same starting beam into either a safe route or a dangerous one."
    }
  },
  {
    id: "1-3",
    title: { ko: "수직 출발", en: "Vertical Launch" },
    intro: {
      ko: "이번에는 레이저가 위로 출발한다. 방향을 바꿔 아래쪽 센서로 보낸다.",
      en: "This laser starts upward. Redirect it back to the lower sensor."
    },
    grid: [
      "........",
      "........",
      "........",
      "........",
      "..\\.../.",
      "........",
      "..S...L.",
      "........"
    ],
    laser: { x: 6, y: 6, dir: "U" },
    targetRotations: 2,
    challenge: { ko: "두 거울만 사용해 수직 경로 완성", en: "Complete the vertical route using only two mirrors", maxRotations: 2, maxMirrorsTouched: 2 },
    hints: {
      ko: ["오른쪽 거울은 위로 오던 빛을 왼쪽으로 보낸다.", "왼쪽 거울은 왼쪽으로 오던 빛을 아래로 보낸다.", "두 거울을 모두 한 번씩 돌린다."],
      en: ["The right mirror must send the upward beam left.", "The left mirror must send the left-moving beam down.", "Rotate both mirrors once."]
    },
    successNote: {
      ko: "반사 법칙은 레이저의 출발 방향이 달라도 같다. 빛이 거울에 들어오는 방향이 기준이다.",
      en: "Reflection works the same for every starting direction. Follow how the beam enters each mirror."
    }
  },
  {
    id: "2-1",
    title: { ko: "세 번 꺾기", en: "Three Turns" },
    intro: {
      ko: "두 거울을 이용해 빛을 세 번 꺾어 목표 센서에 도달시킨다.",
      en: "Connect three mirrors and bend the beam around to the target."
    },
    grid: [
      "........",
      "........",
      "././....",
      "........",
      "........",
      ".S......",
      ".L.\\....",
      "........"
    ],
    laser: { x: 1, y: 6, dir: "R" },
    targetRotations: 2,
    challenge: { ko: "힌트 없이 두 번만 회전해 세 번 반사", en: "Make three reflections in two turns without hints", maxRotations: 2, noHint: true, maxMirrorsTouched: 2 },
    hints: {
      ko: ["아래 거울에서 먼저 빛을 위로 보낸다.", "오른쪽 위 거울은 빛을 왼쪽으로 보내야 한다.", "아래 거울과 오른쪽 위 거울만 한 번씩 돌린다."],
      en: ["First send the beam upward at the lower mirror.", "The upper-right mirror must send it left.", "Rotate only the lower and upper-right mirrors once."]
    },
    successNote: {
      ko: "반사는 여러 번 이어질 수 있다. 각 거울에서 들어오는 방향을 차례로 따라가면 긴 경로도 예측할 수 있다.",
      en: "Reflections can happen in sequence. Trace the incoming direction at each mirror to predict a long route."
    }
  },
  {
    id: "2-2",
    title: { ko: "접이식 거울 통로", en: "Retractable Mirror Passage" },
    intro: {
      ko: "거울은 숨김, 45도, 135도 상태로 바뀐다. 필요한 거울만 올린다.",
      en: "Mirrors cycle below the beam, 45 degrees, then 135 degrees. Raise only the four you need."
    },
    grid: [
      "X.X.X...",
      "........",
      "....m...",
      "X.mmm..X",
      ".m....#X",
      "..m..m.S",
      "mL.mm...",
      ".m..X..."
    ],
    laser: { x: 1, y: 6, dir: "U" },
    rotatableLaser: true,
    stowableMirrors: true,
    commitMode: true,
    shotBudget: 3,
    targetShots: 1,
    targetRotations: 7,
    challenge: { ko: "미끼를 건드리지 않고 필요한 거울만 사용해 한 발에 성공", en: "Deploy only four path mirrors and clear in one shot", maxRotations: 7, maxShots: 1, noHint: true, maxMirrorsTouched: 4 },
    hints: {
      ko: ["목표에서 거꾸로 경로를 추적해 본다.", "정답 경로는 오른쪽, 위, 왼쪽, 아래, 오른쪽 순서다.", "출발점부터 필요한 각도는 45도, 135도, 45도, 135도다."],
      en: ["Point the laser right, then trace backward from the target.", "The route travels right, up, left, down, then right.", "Required angles from the emitter are 45 degrees, 135 degrees, 45 degrees, and 135 degrees."]
    },
    successNote: {
      ko: "거울 방향뿐 아니라 어떤 거울을 실제 광로에 넣을지도 선택이다. 숨긴 거울은 빛이 통과한다.",
      en: "You chose both mirror angles and which mirrors to raise into the beam. Light passes above mirrors lowered beneath the beam plane."
    }
  },
  {
    id: "2-3",
    title: { ko: "거울 네트워크", en: "Mirror Network" },
    intro: {
      ko: "첫 금고와 다음 금고가 이어진다. 다섯 거울을 연결하는 경로를 계획한다.",
      en: "Each first candidate leads to more candidates on its row or column. Plan a route through five mirrors."
    },
    grid: [
      "......X.",
      "X...mmmX",
      "X..m...X",
      ".X......",
      ".m.L.mmX",
      ".XXm.XX.",
      "...XmmmX",
      ".X..X.S."
    ],
    laser: { x: 3, y: 4, dir: "U" },
    rotatableLaser: true,
    stowableMirrors: true,
    commitMode: true,
    shotBudget: 3,
    targetShots: 1,
    targetRotations: 9,
    challenge: { ko: "미끼를 건드리지 않고 다섯 거울로 한 발에 연결", en: "Connect five path mirrors in one shot without touching decoys", maxRotations: 9, maxShots: 1, noHint: true, maxMirrorsTouched: 5 },
    hints: {
      ko: ["목표에서 거꾸로 추적하면 마지막 거울 위치가 보인다.", "경로는 오른쪽, 위, 왼쪽, 아래, 오른쪽, 위, 아래로 이어진다.", "필요한 각도는 45도, 135도, 45도, 135도, 135도다."],
      en: ["Trace backward from the target: the last mirror must sit directly above it.", "The route goes right, up, left, down, right, then down.", "Required angles from the emitter are 45 degrees, 135 degrees, 45 degrees, 135 degrees, and 135 degrees."]
    },
    successNote: {
      ko: "거울을 하나씩 따로 보지 말고 네트워크로 보면 가능한 경로와 막힌 경로를 체계적으로 구분할 수 있다.",
      en: "Treating candidates as a row-and-column network lets you eliminate impossible branches systematically."
    }
  },
  {
    id: "3-1",
    title: { ko: "보안 키 작전", en: "Key Heist" },
    intro: {
      ko: "첫 발로 노란 보안 키를 얻고, 두 번째 발로 탈출 센서를 맞힌다.",
      en: "Hit the yellow security key first, then reconfigure the network and reach the green exit sensor."
    },
    grid: [
      "X....X.X",
      ".K..mm.X",
      "X..m...X",
      ".X...m..",
      "Xm.L.m.X",
      ".XXmX...",
      "X..mXm.S",
      "X..X.X.."
    ],
    laser: { x: 3, y: 4, dir: "U" },
    rotatableLaser: true,
    stowableMirrors: true,
    commitMode: true,
    sequentialKey: true,
    objectiveSequence: ["K", "S"],
    shotBudget: 3,
    targetShots: 2,
    targetRotations: 7,
    challenge: { ko: "힌트 없이 정확히 두 발로 키 확보와 탈출 성공", en: "Steal the key and escape in exactly two shots without hints", maxRotations: 7, maxShots: 2, noHint: true, maxMirrorsTouched: 3 },
    hints: {
      ko: ["키와 탈출 센서는 오른쪽의 첫 거울에서 경로가 갈린다.", "키를 얻을 때는 첫 거울을 45도로 두어 위쪽 경로를 만든다.", "키를 얻은 뒤 첫 거울을 135도로 바꾸고 아래쪽 거울도 135도로 맞춘다."],
      en: ["Both routes branch from the first candidate to the laser's right.", "Raise the first mirror to 45 degrees to reach the key route.", "After the key, change it to 135 degrees and raise the lower mirror to 135 degrees."]
    },
    successNote: {
      ko: "같은 거울망도 상태를 바꾸면 서로 다른 목표를 순서대로 연결할 수 있다.",
      en: "One mirror network can connect different objectives in sequence. The first successful route becomes evidence for the second plan."
    }
  },
  {
    id: "3-2",
    title: { ko: "삼중 잠금 금고", en: "Triple-Lock Vault" },
    intro: {
      ko: "중앙 거울을 45도, 135도, 숨김 상태로 바꾸며 두 보안 키와 최종 센서를 순서대로 맞힌다.",
      en: "Cycle the central mirror through 45 degrees, 135 degrees, then stowed to hit two keys and the final sensor in order."
    },
    grid: [
      "X...X...",
      ".K.mm..X",
      "..m.m..X",
      ".X..m...",
      "m.Lmm..S",
      "..m.m..X",
      ".Q.mm..X",
      "X...X..."
    ],
    laser: { x: 2, y: 4, dir: "U" },
    rotatableLaser: true,
    stowableMirrors: true,
    commitMode: true,
    objectiveSequence: ["K", "Q", "S"],
    shotBudget: 3,
    targetShots: 3,
    targetRotations: 7,
    challenge: { ko: "힌트와 실수 없이 정확히 세 발로 삼중 잠금 해제", en: "Open all three locks in exactly three shots without hints or misses", maxRotations: 7, maxShots: 3, noHint: true, maxMirrorsTouched: 3, maxAlarms: 0 },
    hints: {
      ko: ["오른쪽으로 쏘고 중앙 거울 하나를 세 단계 모두 사용한다.", "노란 키는 중앙 45도와 위쪽 거울 135도다.", "청록 키는 중앙 135도와 아래쪽 거울 45도다. 마지막에는 중앙 거울을 숨긴다."],
      en: ["Point the laser right and use all three states of the central mirror.", "Yellow key: central 45 degrees, upper end mirror 135 degrees.", "Cyan key: central 135 degrees, lower end mirror 45 degrees. Finally stow the central mirror."]
    },
    successNote: {
      ko: "같은 거울도 45도, 135도, 숨김 상태에서 서로 다른 광로를 만든다. 세 상태를 순서대로 제어해 삼중 잠금을 열었다.",
      en: "The same mirror creates different routes at 45 degrees, 135 degrees, and stowed. Sequencing all three states opened the triple lock."
    }
  }
];
