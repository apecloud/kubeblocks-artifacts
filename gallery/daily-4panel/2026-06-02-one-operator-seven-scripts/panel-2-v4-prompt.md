# Ep2 Panel 2 v4

## Locked Text

- Xiaohei: `…always one more script.`
- MySQL: `We've always done it this way.`
- Short script labels: `mysql.sh`, `backup.sh`, `resize.sh`

## Base Image Prompt

Generate Panel 2 of the comic `One Operator, Seven Scripts` as a clean text-free base illustration. The panel shows the escalation of script debt: Xiaohei is being pressed down by another incoming script page/folder added to an already messy pile of scripts. Nearby, a MySQL-like database facility character calmly represents old habits and legacy practice.

Scene: a minimalist hand-drawn Database City maintenance corner. Xiaohei, a small solid-black absurd operator creature with two white dot eyes, tiny thin legs, uneven body, no mouth, tired deadpan expression, is partly buried or flattened under loose blank script papers and folders. One new blank script page is dropping in or sliding onto the pile, making it clear there is always one more script. The mood is exhausted but dryly funny, not disastrous.

MySQL facility: on the right or mid-right, draw a simple database-cylinder / small infrastructure building with a subtle MySQL identity cue only through shape and context, not logos or readable text. It should look stubborn and old-fashioned but not stupid, villainous, or broken. Leave clean blank whitespace near it for later local dialogue text overlay.

Script labels: include 2-3 small blank paper tabs or tag shapes attached to scripts, with enough empty space for local short labels to be overlaid later. Do not render any text on them.

Composition: 16:9 horizontal, pure white background, black wobbly pen line art with lots of whitespace. Xiaohei and the script pile should be the main read on left/center-left; MySQL facility on right. Leave one blank area near Xiaohei for the line `…always one more script.` and one blank area near MySQL for `We've always done it this way.` Keep distant Database City hints extremely sparse and secondary.

Style: Ian Xiaohei style: minimalist black hand-drawn line art, slightly wobbly thin pen lines, clean absurd product-sketch feeling, large empty white areas. Use tiny red non-text accent strokes only for motion/pressure if helpful. No ordinary text boxes, no speech bubbles, no caption cards, no title, no readable text, no pseudo-text, no labels, no UI, no product/control tower, no Kubernetes logo, no KubeBlocks reveal.

Avoid formal architecture diagrams, dashboards, gradients, shadows, paper texture, commercial vector style, cute mascot poster, children's illustration, dense city background, and any malformed text.

## Post Processing

- Source base: `source/panel-2-v4-base.png`
- Final single panel: `panel-2-v4.png`
- Deterministic overlay script: `build_panel2_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Ordinary text frames: none
- Script labels are object-native labels placed on script tabs/papers
- Control tower/product reveal: intentionally absent
