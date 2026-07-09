function makeGridFromLevel(level) {
  return level.grid.map(row => row.split(""));
}

const SVG_NS = "http://www.w3.org/2000/svg";

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  return element;
}

function makeSvg(className) {
  return svgElement("svg", { class: className, viewBox: "0 0 100 100", "aria-hidden": "true" });
}

function directionPoint(dir, entering = false) {
  return {
    R: entering ? [0, 50] : [100, 50],
    L: entering ? [100, 50] : [0, 50],
    D: entering ? [50, 0] : [50, 100],
    U: entering ? [50, 100] : [50, 0]
  }[dir];
}

function makeBeamSvg(steps, sourceDir = null, ghost = false) {
  const svg = makeSvg(`beam-layer${ghost ? " ghost-beam-layer" : ""}`);
  if (sourceDir) {
    const [endX, endY] = directionPoint(sourceDir);
    svg.appendChild(svgElement("path", { d: `M 50 50 L ${endX} ${endY}`, class: "beam-line" }));
  }
  steps.forEach(step => {
    const [startX, startY] = directionPoint(step.dirIn, true);
    let path = `M ${startX} ${startY} L 50 50`;
    if (step.dirOut) {
      const [endX, endY] = directionPoint(step.dirOut);
      path += ` L ${endX} ${endY}`;
    }
    svg.appendChild(svgElement("path", { d: path, class: "beam-line" }));
  });
  return svg;
}

function makeMirrorIcon(mirror) {
  const svg = makeSvg("object-icon mirror-icon");
  const y1 = mirror === "/" ? 82 : 18;
  const y2 = mirror === "/" ? 18 : 82;
  svg.appendChild(svgElement("line", { x1: 18, y1, x2: 82, y2, class: "mirror-shadow" }));
  svg.appendChild(svgElement("line", { x1: 18, y1, x2: 82, y2, class: "mirror-glass" }));
  svg.appendChild(svgElement("circle", { cx: 18, cy: y1, r: 5, class: "mirror-mount" }));
  svg.appendChild(svgElement("circle", { cx: 82, cy: y2, r: 5, class: "mirror-mount" }));
  return svg;
}

function makeStowedMirrorIcon() {
  const svg = makeSvg("object-icon mirror-icon stowed-mirror-icon");
  svg.appendChild(svgElement("path", { d: "M 22 34 V 24 H 34 M 66 24 H 78 V 34 M 78 66 V 76 H 66 M 34 76 H 22 V 66", class: "mirror-slot" }));
  svg.appendChild(svgElement("path", { d: "M 50 31 V 63 M 39 52 L 50 63 L 61 52", class: "mirror-slot-detail" }));
  return svg;
}

function makeLaserIcon(dir) {
  const svg = makeSvg(`object-icon laser-icon dir-${dir}`);
  svg.appendChild(svgElement("rect", { x: 18, y: 32, width: 52, height: 36, rx: 11, class: "laser-body" }));
  svg.appendChild(svgElement("path", { d: "M 26 40 H 57 M 26 50 H 51", class: "laser-detail" }));
  svg.appendChild(svgElement("path", { d: "M 70 38 L 84 44 V 56 L 70 62 Z", class: "laser-nozzle" }));
  svg.appendChild(svgElement("circle", { cx: 84, cy: 50, r: 5, class: "laser-aperture" }));
  return svg;
}

function makeSensorIcon(fake = false) {
  const svg = makeSvg(`object-icon sensor-icon ${fake ? "fake" : "goal"}`);
  svg.appendChild(svgElement("circle", { cx: 50, cy: 50, r: 31, class: "sensor-ring" }));
  svg.appendChild(svgElement("circle", { cx: 50, cy: 50, r: 20, class: "sensor-core" }));
  svg.appendChild(svgElement("path", {
    d: fake ? "M 40 40 L 60 60 M 60 40 L 40 60" : "M 37 50 L 46 59 L 64 39",
    class: "sensor-mark"
  }));
  return svg;
}

function makeKeySensorIcon(secondary = false) {
  const svg = makeSvg(`object-icon sensor-icon key-sensor-icon${secondary ? " secondary-key-icon" : ""}`);
  svg.appendChild(svgElement("circle", { cx: 50, cy: 50, r: 31, class: "sensor-ring" }));
  svg.appendChild(svgElement("circle", { cx: 42, cy: 47, r: 11, class: "key-head" }));
  svg.appendChild(svgElement("path", { d: "M 51 54 L 69 72 M 61 64 L 67 58 M 66 69 L 72 63", class: "key-mark" }));
  return svg;
}

function makeWallIcon() {
  const svg = makeSvg("object-icon wall-icon");
  svg.appendChild(svgElement("path", {
    d: "M 15 24 H 85 V 76 H 15 Z M 15 41 H 85 M 15 59 H 85 M 38 24 V 41 M 66 24 V 41 M 28 41 V 59 M 57 41 V 59 M 40 59 V 76 M 69 59 V 76",
    class: "wall-bricks"
  }));
  return svg;
}

function objectLabel(cell, lang, angle = "", rotatableLaser = false) {
  const labels = lang === "ko"
    ? {
        L: "레이저 발생기",
        laserRotatable: "회전 가능한 레이저 발생기",
        S: "초록 탈출 센서",
        K: "노란 보안 키 센서",
        Q: "청록 보안 키 센서",
        X: "빨간 가짜 센서",
        "#": "벽",
        mirror: "회전 가능한 거울",
        m: "아래로 내려간 거울, 빛 통과"
      }
    : {
        L: "Laser emitter",
        laserRotatable: "Rotatable laser emitter",
        S: "Green exit sensor",
        K: "Yellow security-key sensor",
        Q: "Cyan security-key sensor",
        X: "Red fake sensor",
        "#": "Wall",
        mirror: "Rotatable mirror",
        m: "Mirror lowered below the beam, pass-through"
      };
  if (cell === "/" || cell === "\\") return `${labels.mirror}, ${angle}`;
  if (cell === "m") return labels.m;
  if (cell === "L" && rotatableLaser) return labels.laserRotatable;
  return labels[cell] || "";
}

function renderBoard(boardEl, state) {
  const { grid, level, laser, selected, ray } = state;
  const actions = state.actions || {};
  boardEl.innerHTML = "";

  const pathByCell = new Map();
  const showCurrentPath = !level.commitMode || state.committed;
  const visiblePath = showCurrentPath ? ray.path : [];
  visiblePath.forEach(step => {
    const key = `${step.x},${step.y}`;
    const current = pathByCell.get(key) || [];
    current.push(step);
    pathByCell.set(key, current);
  });

  const ghostPathByCell = new Map();
  const visibleHistory = state.committed && !state.cleared
    ? state.shotHistory.slice(0, -1)
    : state.shotHistory;
  visibleHistory.flat().forEach(step => {
    const key = `${step.x},${step.y}`;
    const current = ghostPathByCell.get(key) || [];
    current.push(step);
    ghostPathByCell.set(key, current);
  });

  grid.forEach((row, y) => {
    row.forEach((cell, x) => {
      const isMirror = cell === "/" || cell === "\\" || (cell === "m" && level.stowableMirrors);
      const isRotatableLaser = cell === "L" && level.rotatableLaser;
      const isInteractive = isMirror || isRotatableLaser;
      const tile = document.createElement(isInteractive ? "button" : "div");
      if (isInteractive) tile.type = "button";
      tile.className = "cell";
      tile.dataset.x = x;
      tile.dataset.y = y;
      tile.setAttribute("role", isInteractive ? "button" : "gridcell");

      const pathSteps = pathByCell.get(`${x},${y}`) || [];
      const ghostSteps = ghostPathByCell.get(`${x},${y}`) || [];
      const sourceDir = cell === "L" ? laser.dir : null;
      if (ghostSteps.length) tile.appendChild(makeBeamSvg(ghostSteps, null, true));
      if (pathSteps.length || sourceDir) tile.appendChild(makeBeamSvg(pathSteps, sourceDir));

      if (cell === "#") tile.classList.add("wall");
      if (cell === "L") tile.classList.add("laser-source");
      if (isRotatableLaser) tile.classList.add("rotatable");
      if (cell === "S") tile.classList.add("sensor");
      if (cell === "K") tile.classList.add("key-sensor");
      if (cell === "Q") tile.classList.add("key-sensor", "secondary-key");
      if (cell === "X") tile.classList.add("fake-sensor");
      if (isMirror) tile.classList.add("mirror");
      if (cell === "m") tile.classList.add("stowed-mirror");
      if (showCurrentPath && ray.activeSensors.has(`${x},${y}`)) tile.classList.add("active");
      if (showCurrentPath && ray.alarmSensors.has(`${x},${y}`)) tile.classList.add("alarm");
      if (showCurrentPath && ray.mirrorHits.has(`${x},${y}`)) tile.classList.add("hit");
      if (selected && selected.x === x && selected.y === y) tile.classList.add("selected");

      let angle = "";
      if (cell === "m") {
        tile.appendChild(makeStowedMirrorIcon());
        const badge = document.createElement("span");
        badge.className = "angle-badge stowed-badge";
        badge.textContent = state.lang === "ko" ? "통과" : "PASS";
        tile.appendChild(badge);
      } else if (isMirror) {
        angle = cell === "/" ? "45°" : "135°";
        tile.appendChild(makeMirrorIcon(cell));
        const badge = document.createElement("span");
        badge.className = "angle-badge";
        badge.textContent = angle;
        tile.appendChild(badge);
      } else if (cell === "L") {
        tile.appendChild(makeLaserIcon(laser.dir));
        if (isRotatableLaser) {
          const badge = document.createElement("span");
          badge.className = "object-action-badge";
          badge.textContent = "ROT";
          tile.appendChild(badge);
        }
      } else if (cell === "S") {
        tile.appendChild(makeSensorIcon(false));
      } else if (cell === "K") {
        tile.appendChild(makeKeySensorIcon());
      } else if (cell === "Q") {
        tile.appendChild(makeKeySensorIcon(true));
      } else if (cell === "X") {
        tile.appendChild(makeSensorIcon(true));
      } else if (cell === "#") {
        tile.appendChild(makeWallIcon());
      }

      const label = objectLabel(cell, state.lang, angle, isRotatableLaser);
      if (label) tile.setAttribute("aria-label", label);
      if (isMirror && actions.selectMirror) {
        tile.addEventListener("click", () => actions.selectMirror(x, y));
      }
      if (isRotatableLaser && actions.selectLaser) {
        tile.addEventListener("click", () => actions.selectLaser(x, y));
      }
      boardEl.appendChild(tile);
    });
  });
}

function renderStars(stars) {
  return "★".repeat(stars) + "☆".repeat(3 - stars);
}
