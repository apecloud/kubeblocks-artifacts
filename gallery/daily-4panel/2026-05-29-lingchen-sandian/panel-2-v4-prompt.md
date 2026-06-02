# Ep1 Panel 2 v4

## Locked Text

- Robot sign: `Default assumption: stateless?`
- Xiaohei: `7 scripts... and 0 hours of sleep.`
- Citizens/facilities: `We have state!` / `Nothing gets lost!`

The rendered PNG uses a line break for each longer phrase and uses a typographic ellipsis in Xiaohei's line.

## Base Image Prompt

Generate a clean text-free base illustration for the second panel of an English 4-panel comic. The scene shows the crisis escalating after the 3 A.M. alert: stateful database facilities and business citizens push back against a naive robot assumption that everything is stateless, while Xiaohei is buried in manual script debt.

Sparse Database City operations room / street corner at night, pure white background. A small robot or automation kiosk stands on one side with a blank object-native sign panel reserved for later text overlay. Xiaohei stands near the center, exhausted, holding or being surrounded by a messy pile of blank script pages and cables. Two small facility/citizen figures on the other side react calmly but urgently; they should represent stateful systems and users depending on persisted data, not foolish databases.

Xiaohei is the recurring small solid-black absurd operator creature with two white dot eyes, tiny thin legs, uneven hand-drawn body, blank serious expression; not cute, not heroic. The robot/kiosk should look generic and slightly naive but not malicious. Database facilities should look professional and dignified: one archive/records-hall shape and one old utility/shop shape are enough. Citizens/facility caretakers should be small and secondary.

Ian Xiaohei style: pure white background, minimalist black hand-drawn line art, slightly wobbly thin pen lines, lots of whitespace, clean absurd product-sketch feeling.

16:9 horizontal. Keep main action in the middle 60% of canvas. Robot sign on left or upper-left with a blank rectangular sign surface. Xiaohei in center with blank script papers around him. Two small reaction figures/facility hints on right, leaving safe blank spaces for two short local text overlays. Leave a safe blank area near Xiaohei for one short line overlay. Main subject 45-55% of canvas; at least 35% blank white space.

Black line art only, with rare red/orange non-text accents for alarm tension or tangled script lines. No colored text.

Do not draw any readable text, labels, pseudo-text, icons that look like words, or title. All final English text will be overlaid later.

Object-native robot sign is allowed as the only explicit sign/frame. No speech bubbles, no dialogue balloons, no ordinary text boxes, no caption cards, no placards beyond the robot's physical sign, no labels, no title. Do not depict Kubernetes as silly or as a database. Do not depict databases as stupid or broken; show state complexity and manual script debt as the problem. Avoid formal architecture diagrams, dense flowcharts, dashboards, UI screenshots, gradients, shadows, paper texture, commercial vector style, cute mascot poster, children's illustration, crowded scene, and malformed text.

## Post Processing

- Source base: `source/panel-2-v4-base.png`
- Final single panel: `panel-2-v4.1.png`
- Deterministic overlay script: `build_panel2_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Ordinary text frames: none
- Local cleanup: removed a model-generated empty oval so it does not read as a speech bubble
- v4.1 point fix: the `0` in `0 hours` is locally drawn as a slashed numeric zero for readability
