const DIRS = {
  R: { dx: 1, dy: 0, beamClass: "beam-h", arrow: ">" },
  L: { dx: -1, dy: 0, beamClass: "beam-h", arrow: "<" },
  U: { dx: 0, dy: -1, beamClass: "beam-v", arrow: "^" },
  D: { dx: 0, dy: 1, beamClass: "beam-v", arrow: "v" }
};

function reflect(dir, mirror) {
  if (mirror === "/") {
    return { R: "U", L: "D", U: "R", D: "L" }[dir];
  }
  if (mirror === "\\") {
    return { R: "D", L: "U", U: "L", D: "R" }[dir];
  }
  return dir;
}

function inBounds(x, y, grid) {
  return y >= 0 && y < grid.length && x >= 0 && x < grid[0].length;
}

function castRay(grid, laser) {
  const path = [];
  const activeSensors = new Set();
  const keySensors = new Set();
  const secondaryKeySensors = new Set();
  const alarmSensors = new Set();
  const mirrorHits = new Set();
  const seen = new Set();
  let x = laser.x;
  let y = laser.y;
  let dir = laser.dir;
  let loop = false;
  let stoppedBy = null;

  for (let step = 0; step < 80; step += 1) {
    const delta = DIRS[dir];
    const nx = x + delta.dx;
    const ny = y + delta.dy;
    if (!inBounds(nx, ny, grid)) {
      stoppedBy = "out";
      break;
    }

    x = nx;
    y = ny;
    const stateKey = `${x},${y},${dir}`;
    if (seen.has(stateKey)) {
      loop = true;
      stoppedBy = "loop";
      break;
    }
    seen.add(stateKey);

    const cell = grid[y][x];
    const dirIn = dir;
    let dirOut = dir;
    if (cell === "/" || cell === "\\") {
      dirOut = reflect(dir, cell);
    }
    path.push({ x, y, dir, dirIn, dirOut, cell });

    if (cell === "#") {
      stoppedBy = "wall";
      break;
    }
    if (cell === "S") {
      activeSensors.add(`${x},${y}`);
    } else if (cell === "K") {
      keySensors.add(`${x},${y}`);
    } else if (cell === "Q") {
      secondaryKeySensors.add(`${x},${y}`);
    } else if (cell === "X") {
      alarmSensors.add(`${x},${y}`);
    } else if (cell === "/" || cell === "\\") {
      mirrorHits.add(`${x},${y}`);
      dir = dirOut;
    }
  }

  return { path, activeSensors, keySensors, secondaryKeySensors, alarmSensors, mirrorHits, stoppedBy, loop };
}
