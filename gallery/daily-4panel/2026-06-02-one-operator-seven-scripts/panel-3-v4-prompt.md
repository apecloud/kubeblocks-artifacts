# Ep2 Panel 3 v4

## Locked Text

- Tower: `One manifest. Everything else handled.`
- Xiaohei: `One place to declare all this?`
- Declaration cards: `PG`, `Redis`, `Kafka`, `MySQL`

## Base Image Prompt

Generate Panel 3 of the comic `One Operator, Seven Scripts` as a clean text-free base illustration. This is the first reveal of the KubeBlocks municipal control tower concept, but do not include brand text or logos. The panel shows manual script chaos being converted into organized declarations.

Scene: a minimalist hand-drawn Database City operations scene. On the left, the messy script tower/pile from the previous panels is being gently pulled into a clear control tower inbox slot. The control tower is centered or center-left: a simple municipal dispatch/control tower with an obvious blank inbox tray/slot receiving loose scripts, and a clean blank display area reserved for later local text overlay. It should feel competent and calm, not magical, not corporate, not a giant UI dashboard.

On the right, the tower outputs several separate neat declaration cards, each card as its own physical object, lined up or floating in an orderly stack. There should be four distinct blank cards corresponding later to PostgreSQL, Redis, Kafka, and MySQL. Make it visually clear these are multiple declarations, not one giant merged configuration. Leave blank space inside each card for local short labels; no text on them.

Xiaohei: a small solid-black absurd operator creature with two white dot eyes, tiny thin legs, uneven body, no mouth, tired but surprised/relieved deadpan expression. Place Xiaohei near the control tower, looking at the inbox/output flow, with clean blank whitespace near Xiaohei for later local dialogue text overlay.

Composition: 16:9 horizontal, pure white background, black wobbly pen line art with lots of whitespace. Left side: messy scripts entering the tower inbox. Center: calm control tower with a blank display panel. Right side: multiple separate declaration cards for PG/Redis/Kafka/MySQL, organized and easy to count. Keep distant Database City facility hints very sparse and secondary.

Style: Ian Xiaohei style: minimalist black hand-drawn line art, slightly wobbly thin pen lines, clean absurd product-sketch feeling, large empty white areas. Use tiny red non-text accent strokes only sparingly, and optional calm green/blue tiny non-text indicator dots if useful, but no colored text.

Strict exclusions: no readable text, no pseudo-text, no labels, no UI screenshots, no title, no speech bubbles, no dialogue balloons, no ordinary text boxes, no Kubernetes logo, no brand logo, no KubeBlocks written text. Do not make the control tower a dumb robot or a villain. Do not compress all databases into one card.

Avoid formal architecture diagrams, dashboards, gradients, shadows, paper texture, commercial vector style, cute mascot poster, children's illustration, dense city background, and any malformed text.

## Post Processing

- Source base: `source/panel-3-v4-base.png`
- Final single panel: `panel-3-v4.png`
- Deterministic overlay script: `build_panel3_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Tower text is object-native inside the control tower display
- Declaration labels are object-native card text on four separate cards
