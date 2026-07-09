const Optics = (() => {
  const EPSILON = 1e-7;

  const add = (a, b) => ({ x: a.x + b.x, y: a.y + b.y });
  const subtract = (a, b) => ({ x: a.x - b.x, y: a.y - b.y });
  const scale = (v, amount) => ({ x: v.x * amount, y: v.y * amount });
  const dot = (a, b) => a.x * b.x + a.y * b.y;
  const cross = (a, b) => a.x * b.y - a.y * b.x;
  const length = v => Math.hypot(v.x, v.y);
  const normalize = v => {
    const magnitude = length(v);
    return magnitude < EPSILON ? { x: 0, y: 0 } : scale(v, 1 / magnitude);
  };
  const rotate = (v, radians) => ({
    x: v.x * Math.cos(radians) - v.y * Math.sin(radians),
    y: v.x * Math.sin(radians) + v.y * Math.cos(radians)
  });
  const degreesToVector = degrees => {
    const radians = degrees * Math.PI / 180;
    return { x: Math.cos(radians), y: Math.sin(radians) };
  };
  const radiansToDegrees = radians => radians * 180 / Math.PI;

  function glassVertices(glass) {
    const angle = glass.angle * Math.PI / 180;
    const halfWidth = glass.width / 2;
    const halfHeight = glass.height / 2;
    return [
      { x: -halfWidth, y: -halfHeight },
      { x: halfWidth, y: -halfHeight },
      { x: halfWidth, y: halfHeight },
      { x: -halfWidth, y: halfHeight }
    ].map(point => add(rotate(point, angle), { x: glass.cx, y: glass.cy }));
  }

  function pointInsideGlass(point, glass) {
    const local = rotate(
      subtract(point, { x: glass.cx, y: glass.cy }),
      -glass.angle * Math.PI / 180
    );
    return Math.abs(local.x) < glass.width / 2 - EPSILON
      && Math.abs(local.y) < glass.height / 2 - EPSILON;
  }

  function intersectRaySegment(origin, direction, start, end) {
    const segment = subtract(end, start);
    const denominator = cross(direction, segment);
    if (Math.abs(denominator) < EPSILON) return null;
    const offset = subtract(start, origin);
    const distance = cross(offset, segment) / denominator;
    const position = cross(offset, direction) / denominator;
    if (distance <= EPSILON || position < -EPSILON || position > 1 + EPSILON) return null;
    return { distance, point: add(origin, scale(direction, distance)) };
  }

  function nearestGlassIntersection(origin, direction, glass) {
    const vertices = glassVertices(glass);
    let nearest = null;
    vertices.forEach((start, index) => {
      const end = vertices[(index + 1) % vertices.length];
      const hit = intersectRaySegment(origin, direction, start, end);
      if (!hit || (nearest && hit.distance >= nearest.distance)) return;
      const edge = subtract(end, start);
      const outward = normalize({ x: edge.y, y: -edge.x });
      nearest = { ...hit, outward, sideIndex: index };
    });
    return nearest;
  }

  function mirrorEndpoints(mirror) {
    const tangent = degreesToVector(mirror.angle);
    const half = (mirror.length || 0.18) / 2;
    const center = { x: mirror.cx, y: mirror.cy };
    return {
      start: subtract(center, scale(tangent, half)),
      end: add(center, scale(tangent, half))
    };
  }

  function nearestMirrorIntersection(origin, direction, mirrors = []) {
    let nearest = null;
    mirrors.forEach((mirror, mirrorIndex) => {
      const endpoints = mirrorEndpoints(mirror);
      const hit = intersectRaySegment(origin, direction, endpoints.start, endpoints.end);
      if (!hit || (nearest && hit.distance >= nearest.distance)) return;
      const tangent = normalize(subtract(endpoints.end, endpoints.start));
      const normal = { x: -tangent.y, y: tangent.x };
      nearest = { ...hit, normal, mirrorIndex };
    });
    return nearest;
  }

  function distanceToBounds(origin, direction) {
    const candidates = [];
    if (direction.x > EPSILON) candidates.push((1 - origin.x) / direction.x);
    if (direction.x < -EPSILON) candidates.push((0 - origin.x) / direction.x);
    if (direction.y > EPSILON) candidates.push((1 - origin.y) / direction.y);
    if (direction.y < -EPSILON) candidates.push((0 - origin.y) / direction.y);
    return Math.min(...candidates.filter(value => value > EPSILON));
  }

  function refract(incident, normalFromOneToTwo, indexOne, indexTwo) {
    let normal = normalize(normalFromOneToTwo);
    const incoming = normalize(incident);
    if (dot(incoming, normal) < 0) normal = scale(normal, -1);
    const tangent = { x: -normal.y, y: normal.x };
    const signedSinIncident = dot(incoming, tangent);
    const sinTransmitted = indexOne / indexTwo * signedSinIncident;
    const incidenceAngle = radiansToDegrees(Math.asin(Math.min(1, Math.abs(signedSinIncident))));

    if (Math.abs(sinTransmitted) > 1) {
      const reflected = normalize(subtract(incoming, scale(normal, 2 * dot(incoming, normal))));
      return { direction: reflected, tir: true, incidenceAngle, refractionAngle: null };
    }

    const cosTransmitted = Math.sqrt(Math.max(0, 1 - sinTransmitted ** 2));
    const transmitted = normalize(add(scale(normal, cosTransmitted), scale(tangent, sinTransmitted)));
    return {
      direction: transmitted,
      tir: false,
      incidenceAngle,
      refractionAngle: radiansToDegrees(Math.asin(Math.abs(sinTransmitted)))
    };
  }

  function traceRay({ source, glass, mirrors = [], ambientIndex = 1, maxInteractions = 12 }) {
    let origin = { x: source.x, y: source.y };
    let direction = degreesToVector(source.angle);
    let inside = pointInsideGlass(origin, glass);
    const segments = [];
    const events = [];

    for (let interaction = 0; interaction < maxInteractions; interaction += 1) {
      const boundaryDistance = distanceToBounds(origin, direction);
      const glassHit = nearestGlassIntersection(origin, direction, glass);
      const mirrorHit = nearestMirrorIntersection(origin, direction, mirrors);
      const mirrorIsNearest = mirrorHit
        && mirrorHit.distance < boundaryDistance
        && (!glassHit || mirrorHit.distance < glassHit.distance);

      if (mirrorIsNearest) {
        segments.push({ start: origin, end: mirrorHit.point, medium: inside ? "glass" : "air" });
        const normal = dot(direction, mirrorHit.normal) > 0
          ? scale(mirrorHit.normal, -1)
          : mirrorHit.normal;
        const reflected = normalize(subtract(direction, scale(normal, 2 * dot(direction, normal))));
        const incidenceAngle = radiansToDegrees(Math.acos(Math.min(1, Math.abs(dot(direction, normal)))));
        events.push({
          type: "mirror",
          point: mirrorHit.point,
          normal,
          mirrorIndex: mirrorHit.mirrorIndex,
          incidenceAngle,
          refractionAngle: incidenceAngle,
          tir: false
        });
        direction = reflected;
        origin = add(mirrorHit.point, scale(direction, 1e-5));
        continue;
      }

      if (!glassHit || glassHit.distance >= boundaryDistance) {
        segments.push({
          start: origin,
          end: add(origin, scale(direction, boundaryDistance)),
          medium: inside ? "glass" : "air"
        });
        break;
      }

      segments.push({ start: origin, end: glassHit.point, medium: inside ? "glass" : "air" });
      const indexOne = inside ? glass.index : ambientIndex;
      const indexTwo = inside ? ambientIndex : glass.index;
      const normal = inside ? glassHit.outward : scale(glassHit.outward, -1);
      const result = refract(direction, normal, indexOne, indexTwo);
      events.push({
        type: "refraction",
        point: glassHit.point,
        normal,
        indexOne,
        indexTwo,
        incidenceAngle: result.incidenceAngle,
        refractionAngle: result.refractionAngle,
        tir: result.tir
      });
      direction = result.direction;
      if (!result.tir) inside = !inside;
      origin = add(glassHit.point, scale(direction, 1e-5));
    }

    return {
      segments,
      events,
      glassVertices: glassVertices(glass),
      mirrorSegments: mirrors.map(mirror => ({ ...mirrorEndpoints(mirror), label: mirror.label || "" }))
    };
  }

  function segmentDistance(point, start, end) {
    const segment = subtract(end, start);
    const denominator = dot(segment, segment);
    if (denominator < EPSILON) return length(subtract(point, start));
    const amount = Math.max(0, Math.min(1, dot(subtract(point, start), segment) / denominator));
    return length(subtract(point, add(start, scale(segment, amount))));
  }

  function traceHitsSensor(trace, sensor) {
    return trace.segments.some(segment => segmentDistance(sensor, segment.start, segment.end) <= sensor.radius);
  }

  function pointOnTraceAtX(trace, targetX) {
    for (const segment of trace.segments) {
      const minX = Math.min(segment.start.x, segment.end.x) - EPSILON;
      const maxX = Math.max(segment.start.x, segment.end.x) + EPSILON;
      if (targetX < minX || targetX > maxX || Math.abs(segment.end.x - segment.start.x) < EPSILON) continue;
      const ratio = (targetX - segment.start.x) / (segment.end.x - segment.start.x);
      if (ratio >= 0 && ratio <= 1) {
        return {
          x: targetX,
          y: segment.start.y + (segment.end.y - segment.start.y) * ratio
        };
      }
    }
    return null;
  }

  return {
    traceRay,
    traceHitsSensor,
    pointOnTraceAtX,
    refract,
    glassVertices,
    mirrorEndpoints,
    pointInsideGlass
  };
})();
