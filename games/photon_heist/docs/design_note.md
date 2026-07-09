# Prototype 1 Design Note

## Core Principle

재미가 먼저이고, 물리 설명은 게임 규칙 안에 숨긴다.

## MVP Scope

- Theme: light travels straight and reflects from mirrors
- Play style: rotate fixed mirrors on an 8x8 grid
- Win condition: beam reaches the green sensor
- Fail condition: beam reaches the red fake sensor
- Language: Korean / English

## Objects

- `.` empty tile
- `L` laser source
- `S` target sensor
- `X` fake sensor
- `#` wall
- `/` mirror
- `\` mirror

Board objects are rendered as inline SVG rather than font glyphs. This keeps
both mirror orientations at exact 45-degree angles and avoids the backslash
appearing as a won-sign glyph on Korean systems. The target uses a green check
mark while the fake sensor uses a red X, so they do not rely on color alone.
Beam segments stop at the center of walls and sensors.

## Reflection Rules

Mirror `/`:

- R -> U
- L -> D
- U -> R
- D -> L

Mirror `\`:

- R -> D
- L -> U
- U -> L
- D -> R

## Educational Notes

The game should not begin with formulas.  
The player first experiments, then sees a short explanation after clearing a stage.

## Stage Progression

The ten reflection stages should add a new decision instead of merely repeating
the previous mirror count:

1. Observe straight travel.
2. Rotate one mirror.
3. Combine 45° and 135° mirrors around walls.
4. Distinguish a safe target from a red alarm.
5. Read a vertically launched beam.
6. Trace three reflections.
7. Navigate a four-mirror corridor.
8. Ignore decoys and minimize rotations.
9. Use sequential alarms as feedback.
10. Complete a five-reflection final vault.

## Feedback

- A newly solved route triggers a short vault banner, green light particles,
  an active-sensor pulse, and a highlighted Next button.
- A newly triggered fake sensor shakes the board and shows a red alarm banner.
- Short Web Audio cues are synthesized in the browser, so the game still runs
  as local files without downloaded audio assets.
- Sound can be disabled, and animation duration is minimized when the operating
  system requests reduced motion.

## Progression Storage

- The mission map shows all ten stages, best stars, total completion, and the
  currently selected stage.
- Clearing a stage unlocks the next one; previous unlocked stages remain
  replayable from the map.
- Only a better star result replaces the saved result.
- Progress is stored in localStorage under `photonHeistProgressV1`. If storage
  is unavailable, progression still works for the current session.

## Bonus Challenges and Chapter Completion

- Every stage has one optional challenge defined in `levels.js`, such as using
  no hint, avoiding decoy mirrors, or allowing no extra alarm transitions.
- Challenge completion is saved separately from stars and appears as a diamond
  on the mission map.
- Clearing the final vault opens a chapter summary with total stars and bonus
  challenges. The player can return to the map to improve incomplete records.

## Difficulty Strategy

Use one carefully tuned main progression instead of cloning every stage into
Easy, Medium, and Hard versions. Later stages increase decision complexity with
visually identical decoy mirrors. Optional challenges provide the expert layer,
while hints provide assistance without splitting the campaign into three sets.

Late reflection stages also allow the laser emitter itself to rotate. The
player must determine the starting direction before separating path mirrors
from decoys. Re-entering a completed stage always creates a fresh board while
preserving only the best stars and challenge record.

## Glass Route

`glass.html` now hosts ten refraction and mixed-optics stages. Early stages use
live aiming or prediction-before-reveal; later stages use plan, fire, and result
feedback with a three-shot budget. G0-4 combines 5-degree coarse aiming with
1-degree fine aiming so every intended target is reachable from the controls.
G2-2 shows an ordered data-shard → exit tracker, while completed experiments
store best moves and shots separately from stars and challenges. Re-entering
an experiment still starts from a clean optical setup.

`src/optics.js` traces continuous-angle rays through parallel glass slabs,
total internal reflection, and fixed mirrors while keeping physics separate
from SVG rendering. `tests/optics_test.html` currently checks 27 optical and
stage-solution invariants.

Learner-facing notes lead with the observable idea. The parallel-slab lesson
explains that the outgoing beam stays parallel but shifts sideways; the full
lateral-displacement formula is reserved for optional advanced material.

## Campaign Hub

`hub.html` reads both chapter progress keys through `src/chapters.js`. Required
mission clears unlock chapters; stars and bonus challenges record mastery but
do not block the campaign. Both progress objects may also contain versioned
`bestRotations` and `bestShots` maps; the hub deliberately ignores those
optional personal-performance fields when calculating unlocks.
