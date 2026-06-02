# Ep1 Panel 1 v4

## Locked Text

- Phone alert: `03:00` / `PRIMARY DOWN` / `x47`
- Xiaohei: `...not again. Not at 3 A.M.`

The final rendered PNG uses a multiplication sign for the count and an ellipsis in Xiaohei's line, matching the approved v4 script.

## Base Image Prompt

Generate a clean text-free base illustration for the first panel of an English 4-panel comic. Scene: 3 A.M. database city crisis. A small solid-black Xiaohei operator character wakes at night beside a large phone showing an alert screen area, with a few distant simple database-city infrastructure silhouettes in the background. The core action is Xiaohei staring at the phone, exhausted and deadpan, about to deal with another primary database outage.

Xiaohei is a small solid-black absurd creature with two white dot eyes, tiny thin legs, uneven hand-drawn body, blank serious expression; no mouth, not cute, not heroic. A phone is the main object and has a blank screen area reserved for later text overlay. Phone screen must be empty with no readable letters, no pseudo-text, no icons that look like text.

Ian Xiaohei style: pure white background, minimalist black hand-drawn line art, slightly wobbly thin pen lines, lots of whitespace, clean absurd product-sketch feeling.

16:9 horizontal. Main subject around 45% of canvas. Phone on left or center-left, Xiaohei near it, large empty white space around them. Leave safe blank space near Xiaohei for a short line of text overlay. Keep at least 35% blank white space. Simple city/facility hints should be very sparse and secondary.

Black line art only, with very small red non-text alert accents and maybe one tiny orange motion/alarm stroke. No colored text.

Do not draw any readable text. All final text will be overlaid later.

Phone screen can be a physical object-native rectangle, but no speech bubbles, no dialogue balloons, no ordinary text boxes, no caption cards, no placards, no labels, no title. Avoid formal architecture diagrams, dashboards, UI screenshots, gradients, shadows, paper texture, commercial vector style, cute mascot poster, children's illustration, dense city background, and any malformed text.

## Post Processing

- Source base: `source/panel-1-v4-base.png`
- Final single panel: `panel-1-v4.1.png`
- Deterministic overlay script: `build_panel1_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Ordinary text frames: none
- v4.1 point fix: one tiny red alert glint on the far Database City skyline, with no added text or frame
