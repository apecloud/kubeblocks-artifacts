# Ep2 Panel 4 v4

## Locked Text

- Xiaohei: `…just one. For emergencies.`
- Counter: `Sleep: 20m`

## Base Image Prompt

Generate a cleaner Panel 4 punchline base for `One Operator, Seven Scripts`. This is the quiet final joke: after everything is organized, Xiaohei still secretly keeps one old script for emergencies.

Scene: a very clean, calm operator room with lots of blank white space. Only 2-3 core elements: Xiaohei, a tiny sleep counter in the lower-left, and maybe a simple clean desk/floor line. No product explanation.

Xiaohei: small solid-black absurd operator creature with two white dot eyes, tiny thin legs, uneven hand-drawn body, no mouth, tired deadpan guilty expression. Place Xiaohei around center-left. Xiaohei must hold one old blank script paper behind its back: the hand/arm is behind the black body, and only a small corner or side of the paper peeks out from behind the body, clearly hidden rather than openly presented. Body language: pretending to be innocent while hiding the paper. Dryly funny, quiet, not dramatic.

Sleep counter: lower-left corner, a small simple desk timer/status meter with a blank screen rectangle reserved for local text overlay. No text on it. It should be an object-native display, not a caption card.

Composition: 16:9 horizontal, pure white background, lots of whitespace. Leave clean blank space near Xiaohei for later local dialogue text overlay. Keep the scene sparse and uncluttered. No control tower as main subject; if there is any background, it should be extremely faint and secondary, preferably none.

Style: Ian Xiaohei style: minimalist black hand-drawn line art, slightly wobbly thin pen lines, clean absurd product-sketch feeling, large empty white areas. Black line art only, with no color unless a tiny neutral indicator dot on the sleep counter is necessary.

Strict exclusions: no readable text, no pseudo-text, no labels, no title, no speech bubbles, no dialogue balloons, no ordinary text boxes, no UI screenshot, no brand text/logo, no Kubernetes logo, no dense background, no product/control tower explanation, no multiple characters, no dramatic action, no malformed text.

Avoid formal architecture diagrams, dashboards, gradients, shadows, paper texture, commercial vector style, cute mascot poster, and children's illustration.

## Post Processing

- Source base: `source/panel-4-v4-base.png`
- Final single panel: `panel-4-v4.png`
- Deterministic overlay script: `build_panel4_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Xiaohei line is black text in open whitespace, no bubble or ordinary frame
- Counter text is object-native inside the timer screen
