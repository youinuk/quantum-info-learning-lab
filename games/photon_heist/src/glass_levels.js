const GLASS_LEVELS = [
  {
    id: "G0-1",
    title: { ko: "정면 입사", en: "Straight In" },
    intro: {
      ko: "레이저가 유리 면에 수직으로 들어간다. 방향이 꺾이는지 관찰한다.",
      en: "The laser enters the glass face straight on. Watch whether the direction changes."
    },
    source: { x: 0.08, y: 0.5, angle: 0 },
    glass: { cx: 0.5, cy: 0.5, width: 0.28, height: 0.58, index: 1.5, initialAngle: 0 },
    solutionAngle: 0,
    rotatable: false,
    targetRotations: 0,
    hints: [
      { ko: "입사각이 0도이면 굴절각도 0도다.", en: "At 0 deg incidence, the refraction angle is also 0 deg." },
      { ko: "n1 sin 0도 = n2 sin 0도라서 양쪽 모두 0이다.", en: "n1 sin 0 deg = n2 sin 0 deg, so both sides are zero." },
      { ko: "속도는 줄어들지만 진행 방향은 그대로다.", en: "The light slows down, but its direction stays the same." }
    ],
    note: {
      ko: "스넬 법칙: n1 sin(theta1) = n2 sin(theta2). 정면으로 들어가면 theta1=0도, theta2=0도라서 방향이 변하지 않는다.",
      en: "Snell's law: n1 sin(theta1) = n2 sin(theta2). With theta1=0 deg, theta2 is also 0 deg, so the beam does not bend."
    }
  },
  {
    id: "G0-2",
    title: { ko: "굴절 조준", en: "Refraction Aim" },
    intro: {
      ko: "레이저를 기울여 굴절된 경로가 센서를 지나가게 만든다.",
      en: "Tilt the laser so the refracted path passes through the sensor."
    },
    source: { x: 0.08, y: 0.62, angle: 0 },
    glass: { cx: 0.5, cy: 0.5, width: 0.28, height: 0.56, index: 1.5, initialAngle: 0 },
    solutionAngle: -20,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    targetRotations: 4,
    hints: [
      { ko: "-5도 버튼으로 레이저를 위쪽으로 기울여 본다.", en: "Use the -5 deg button to tilt the laser upward." },
      { ko: "공기에서 유리로 들어갈 때 빛은 법선 쪽으로 꺾인다.", en: "When light enters glass from air, it bends toward the normal." },
      { ko: "레이저를 -20도 근처로 맞추면 센서를 지난다.", en: "Near -20 deg, the beam passes through the sensor." }
    ],
    note: {
      ko: "공기(n=1)에서 유리(n=1.5)로 들어가면 굴절각이 입사각보다 작아진다. 평행한 유리판을 지나면 나오는 빛은 처음 방향과 평행하지만 옆으로 조금 이동한다.",
      en: "From air (n=1) into glass (n=1.5), the refraction angle is smaller than the incidence angle. After a parallel glass slab, the exiting beam is parallel to the original beam but shifted sideways."
    },
    challenge: { noHint: true }
  },
  {
    id: "G0-3",
    title: { ko: "기울어진 보안 유리", en: "Tilted Security Glass" },
    intro: {
      ko: "유리판이 -20도로 고정되어 있다. 레이저를 반대 방향으로 조정해 센서를 맞힌다.",
      en: "The glass pane is fixed at -20 deg. Adjust the laser in the opposite direction to hit the sensor."
    },
    source: { x: 0.08, y: 0.38, angle: 0 },
    glass: { cx: 0.5, cy: 0.5, width: 0.28, height: 0.58, index: 1.5, initialAngle: -20 },
    solutionAngle: 20,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    targetRotations: 4,
    hints: [
      { ko: "+5도 버튼으로 레이저를 아래쪽으로 기울인다.", en: "Use +5 deg to tilt the laser downward." },
      { ko: "고정된 유리 면의 법선을 기준으로 입사각을 생각한다.", en: "Judge the incidence angle from the normal of the fixed glass face." },
      { ko: "+20도 근처에서 출사 광선이 센서를 지난다.", en: "Near +20 deg, the exiting beam passes through the sensor." }
    ],
    note: {
      ko: "평행한 두 면을 가진 유리판에서는 들어갈 때와 나올 때 빛이 반대 방향으로 꺾인다. 나오는 빛은 처음 빛과 평행하지만 조금 옆으로 이동한다.",
      en: "In a parallel-sided glass pane, light bends one way when entering and the opposite way when leaving. The exiting beam is parallel to the starting beam but slightly displaced."
    },
    challenge: { noHint: true }
  },
  {
    id: "G0-4",
    title: { ko: "경보 구역 피하기", en: "Avoid the Alarm Zone" },
    intro: {
      ko: "센서는 5도 눈금 사이에 있다. 5도 조정과 1도 미세 조정으로 세 발 안에 맞힌다.",
      en: "The sensor sits between 5 deg marks. Use coarse and fine adjustment to hit it within three shots."
    },
    source: { x: 0.08, y: 0.45, angle: 0 },
    glass: { cx: 0.52, cy: 0.48, width: 0.38, height: 0.5, index: 1.5, initialAngle: 0 },
    solutionAngle: -7,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    fineStepDeg: 1,
    targetRotations: 3,
    commitMode: true,
    targetShots: 1,
    shotBudget: 3,
    sensorRadius: 0.01,
    sensorT: 0.9,
    shardAngle: -5,
    shardT: 0.4,
    shardRadius: 0.018,
    dangerZones: [{ x1: 0, y1: 0.76, x2: 1, y2: 1 }],
    hints: [
      { ko: "먼저 -5도 근처로 조정해 정보 조각 경로를 확인한다.", en: "Start near -5 deg to inspect the data-shard route." },
      { ko: "센서는 -5도와 -10도 사이에 있다. 미세 조정으로 1도씩 보정한다.", en: "The sensor is between -5 deg and -10 deg. Fine-tune one degree at a time." },
      { ko: "-7도 근처에서 경보 없이 센서에 도달한다.", en: "Near -7 deg, the beam reaches the sensor without triggering the alarm." }
    ],
    note: {
      ko: "큰 눈금으로 목표 근처까지 이동하고 작은 눈금으로 마무리하면 빠르고 정확하게 조정할 수 있다.",
      en: "Use coarse steps to get close, then fine steps to finish accurately."
    },
    challenge: { collectShard: true, maxRotations: 3, maxShots: 2 }
  },
  {
    id: "G1-1",
    title: { ko: "물의 굴절", en: "Water Refraction" },
    intro: {
      ko: "경로를 보기 전에 먼저 예측한다. 같은 입사각에서 물과 유리 중 어느 쪽이 더 많이 꺾일까?",
      en: "Predict before revealing the path. At the same incidence angle, which bends light more: water or glass?"
    },
    source: { x: 0.08, y: 0.5, angle: -30 },
    glass: { cx: 0.5, cy: 0.5, width: 0.3, height: 0.62, index: 1.33, initialAngle: 0 },
    solutionAngle: 0,
    rotatable: false,
    targetRotations: 0,
    prediction: {
      question: {
        ko: "같은 30도 입사에서 어느 매질이 빛을 법선 쪽으로 더 많이 꺾을까?",
        en: "At the same 30 deg incidence, which medium bends light more toward the normal?"
      },
      options: [
        { id: "water", label: { ko: "물 n=1.33", en: "Water n=1.33" } },
        { id: "glass", label: { ko: "유리 n=1.50", en: "Glass n=1.50" } }
      ],
      correct: "glass",
      feedback: {
        ko: "굴절률이 큰 매질일수록 법선 쪽으로 더 많이 꺾인다. 다시 선택해 본다.",
        en: "A higher refractive index bends light farther toward the normal. Try again."
      }
    },
    hints: [
      { ko: "30도 입사에서 물은 약 22도, 유리는 약 19도다.", en: "At 30 deg incidence, water gives about 22 deg and glass about 19 deg." },
      { ko: "굴절률이 클수록 굴절각은 작아지고 법선 쪽으로 더 많이 꺾인다.", en: "A larger refractive index makes the refraction angle smaller, bending the light more toward the normal." },
      { ko: "물 n=1.33, 유리 n=1.5, 다이아몬드 n=2.4 순서로 더 많이 꺾인다.", en: "Water n=1.33, glass n=1.5, diamond n=2.4: larger n bends more." }
    ],
    note: {
      ko: "굴절률 n = c/v이다. n이 클수록 빛은 더 느리게 가고 법선 쪽으로 더 많이 꺾인다.",
      en: "The refractive index is n = c/v. A larger n means light moves slower in that material and bends more toward the normal."
    },
    challenge: { maxPredictions: 1 }
  },
  {
    id: "G1-2",
    title: { ko: "다시 공기로", en: "Back Into Air" },
    intro: {
      ko: "광원이 유리 안에 있다. 유리에서 공기로 나올 때 어느 방향으로 꺾이는지 예측한다.",
      en: "The source is inside glass. Predict how light bends when it exits into air."
    },
    source: { x: 0.42, y: 0.5, angle: -25 },
    glass: { cx: 0.52, cy: 0.5, width: 0.25, height: 0.65, index: 1.5, initialAngle: 0 },
    solutionAngle: 0,
    rotatable: false,
    targetRotations: 0,
    prediction: {
      question: {
        ko: "유리에서 공기로 나오는 빛은 법선을 기준으로 어떻게 꺾일까?",
        en: "When light leaves glass for air, how does it bend relative to the normal?"
      },
      options: [
        { id: "toward", label: { ko: "법선 쪽으로", en: "Toward the normal" } },
        { id: "away", label: { ko: "법선에서 멀리", en: "Away from the normal" } }
      ],
      correct: "away",
      feedback: {
        ko: "큰 굴절률에서 작은 굴절률로 나갈 때는 법선에서 멀어진다. 다시 선택해 본다.",
        en: "When light goes from higher n to lower n, it bends away from the normal. Try again."
      }
    },
    hints: [
      { ko: "유리(n=1.5)에서 공기(n=1)로 나오면 법선에서 멀어지는 방향으로 꺾인다.", en: "From glass (n=1.5) to air (n=1), the beam bends away from the normal." },
      { ko: "25도 입사라면 굴절각은 약 39도다.", en: "At 25 deg incidence, the refraction angle is about 39 deg." },
      { ko: "밀한 매질에서 성긴 매질로 나올 때는 법선에서 멀어진다.", en: "From a denser medium to a rarer medium, light bends away from the normal." }
    ],
    note: {
      ko: "스넬 법칙은 양방향으로 적용된다. 유리에서 공기로 나올 때 각도가 너무 커지면 빛이 빠져나가지 못하고 전반사가 일어난다.",
      en: "Snell's law works in both directions. When leaving glass for air, a large angle can prevent escape and cause total internal reflection."
    },
    challenge: { maxPredictions: 1 }
  },
  {
    id: "G1-3",
    title: { ko: "임계각 찾기", en: "Find the Critical Angle" },
    intro: {
      ko: "유리 안에서 출발한다. 각도를 키우면 어느 순간 빛이 밖으로 나가지 못한다.",
      en: "Start inside glass. As the angle grows, there is a point where the beam cannot leave."
    },
    source: { x: 0.42, y: 0.5, angle: 0 },
    glass: { cx: 0.52, cy: 0.5, width: 0.25, height: 0.65, index: 1.5, initialAngle: 0 },
    solutionAngle: -40,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    targetRotations: 8,
    commitMode: true,
    targetShots: 1,
    shotBudget: 3,
    hints: [
      { ko: "각도를 키우다 보면 빛이 유리 밖으로 나가지 못하는 순간이 나온다.", en: "Increase the angle until the beam no longer escapes the glass." },
      { ko: "유리(n=1.5)의 임계각은 약 41.8도다.", en: "For glass (n=1.5), the critical angle is about 41.8 deg." },
      { ko: "40도에서는 아직 나가지만 45도에서는 전반사가 일어난다.", en: "At 40 deg the beam still exits, but at 45 deg total internal reflection occurs." }
    ],
    note: {
      ko: "임계각 theta_c = arcsin(n2/n1). 입사각이 임계각보다 크면 굴절 대신 전반사가 일어난다. 광섬유가 이 원리를 이용한다.",
      en: "Critical angle theta_c = arcsin(n2/n1). Above it, refraction is replaced by total internal reflection. Fiber-optic cables use this idea."
    },
    challenge: { noHint: true, maxShots: 1 }
  },
  {
    id: "G1-4",
    title: { ko: "전반사 금고", en: "TIR Vault" },
    intro: {
      ko: "오른쪽 출구는 경보 구역이다. 전반사를 이용해 위쪽으로 빛을 돌린다.",
      en: "The right-side exit is an alarm zone. Use total internal reflection to turn the beam upward."
    },
    source: { x: 0.42, y: 0.5, angle: 0 },
    glass: { cx: 0.52, cy: 0.5, width: 0.25, height: 0.65, index: 1.5, initialAngle: 0 },
    solutionAngle: -50,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    targetRotations: 10,
    commitMode: true,
    targetShots: 1,
    shotBudget: 3,
    sensorRadius: 0.022,
    dangerZones: [{ x1: 0.66, y1: 0, x2: 1, y2: 1 }],
    hints: [
      { ko: "오른쪽 면으로 빠져나가면 경보가 울린다.", en: "Exiting through the right face triggers the alarm." },
      { ko: "임계각을 넘기면 오른쪽 면에서 전반사가 일어나 위쪽으로 꺾인다.", en: "Above the critical angle, total internal reflection happens at the right face and redirects the beam upward." },
      { ko: "40도 근처에서 전반사된 빛이 위쪽 센서에 도달한다.", en: "Near 40 deg, the reflected beam reaches the upper sensor." }
    ],
    note: {
      ko: "전반사된 빛은 거울 반사처럼 입사각과 반사각이 같다. 광섬유 안의 빛도 전반사를 반복하며 이동한다.",
      en: "A totally internally reflected beam follows the same angle rule as mirror reflection. Light in fiber optics also travels by repeated total internal reflection."
    },
    challenge: { noHint: true, maxRotations: 10, maxShots: 1 }
  },
  {
    id: "G2-1",
    title: { ko: "유리 너머 반사", en: "Reflection Beyond Glass" },
    intro: {
      ko: "유리에서 굴절된 빛을 고정 거울에 맞혀 위쪽 금고로 보낸다.",
      en: "Send the refracted beam through glass, hit the fixed mirror, and guide it to the upper vault."
    },
    source: { x: 0.08, y: 0.7, angle: 0 },
    glass: { cx: 0.5, cy: 0.56, width: 0.26, height: 0.62, index: 1.5, initialAngle: 0 },
    mirrors: [{ cx: 0.78, cy: 0.48, length: 0.22, angle: -55 }],
    solutionAngle: -20,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    targetRotations: 4,
    commitMode: true,
    targetShots: 1,
    shotBudget: 3,
    sensorRadius: 0.024,
    sensorT: 0.66,
    dangerZones: [{ x1: 0.9, y1: 0, x2: 1, y2: 1 }],
    hints: [
      { ko: "레이저를 위쪽으로 기울여 유리 뒤 거울의 중앙을 노린다.", en: "Tilt the laser upward and aim at the mirror behind the glass." },
      { ko: "평행한 유리판을 지난 빛은 원래 방향과 평행하지만 옆으로 이동한다.", en: "After a parallel glass slab, the beam remains parallel to its original direction but shifts sideways." },
      { ko: "-20도 근처에서 거울을 맞히고 반사광이 위쪽 센서로 향한다.", en: "Near -20 deg, the beam hits the mirror and reflects toward the upper sensor." }
    ],
    note: {
      ko: "복합 경로는 규칙을 순서대로 적용한다. 공기에서 유리로 굴절, 유리에서 공기로 굴절, 거울에서 반사 순서다.",
      en: "Apply the rules in order: refraction into glass, refraction out of glass, then mirror reflection."
    },
    challenge: { noHint: true, maxRotations: 4, maxShots: 1 }
  },
  {
    id: "G2-2",
    title: { ko: "순서 잠금장치", en: "Sequence Lock" },
    intro: {
      ko: "두 경로를 순서대로 실행한다. 먼저 정보 조각을 얻고, 다음에 잠금 센서를 연다.",
      en: "Run two paths in order. First collect the data shard, then open the locked sensor."
    },
    source: { x: 0.08, y: 0.6, angle: 0 },
    glass: { cx: 0.55, cy: 0.52, width: 0.22, height: 0.56, index: 1.5, initialAngle: 0 },
    mirrors: [
      { cx: 0.28, cy: 0.673, length: 0.17, angle: 0, label: "A" },
      { cx: 0.78, cy: 0.374, length: 0.2, angle: -55, label: "B" }
    ],
    solutionAngle: -20,
    shardAngle: 20,
    shardT: 0.55,
    shardRadius: 0.02,
    requiresShard: true,
    rotatable: true,
    rotateMode: "laser",
    stepDeg: 5,
    firstSolutionRotations: 4,
    targetRotations: 12,
    commitMode: true,
    targetShots: 2,
    shotBudget: 3,
    sensorRadius: 0.024,
    sensorT: 0.64,
    hints: [
      { ko: "첫 발은 +20도로 A 거울을 맞혀 정보 조각을 얻는다.", en: "For the first shot, use +20 deg to hit mirror A and collect the data shard." },
      { ko: "조각을 얻은 뒤에는 -20도 근처로 크게 전환한다.", en: "After collecting the shard, swing near -20 deg." },
      { ko: "두 번째 경로는 유리와 B 거울 순서다. B가 빛을 잠금 센서로 보낸다.", en: "The second path goes through glass and mirror B. Mirror B sends the beam to the locked sensor." }
    ],
    note: {
      ko: "같은 장치라도 통과하는 순서가 달라지면 경로가 달라진다. 반사에서 정보를 얻고, 굴절과 반사를 이용해 탈출한다.",
      en: "The same devices can produce different paths when the order changes. Here, reflection collects information, then refraction and reflection create the escape route."
    },
    challenge: { noHint: true, maxRotations: 12, maxShots: 2 }
  }
];
