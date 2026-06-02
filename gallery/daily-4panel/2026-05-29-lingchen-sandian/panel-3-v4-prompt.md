# Ep1 Panel 3 v4

## Locked Text

- Tower: `Declare the desired state. I'll orchestrate the workflow.`
- Labels: `Backup` / `Restore` / `Scale` / `Failover`
- Xiaohei: `...how is it not panicking?`

The rendered PNG uses line breaks for readability and a typographic ellipsis in Xiaohei's line.

## Base Image Prompt

Generate a clean text-free base illustration for the third panel of an English 4-panel comic. The scene shows KubeBlocks as a calm municipal control tower / dispatch center orchestrating database operations after the chaos in Panel 2. Xiaohei watches, surprised that the tower is calmly coordinating workflows instead of panicking.

Sparse Database City control area at night, pure white background. A central or right-of-center control tower / dispatch console sends a few simple orange workflow paths toward database-city facilities. The tower should be a system/control-plane object, not a face, not a mascot, not a hero. It can have one blank object-native status screen or panel reserved for later text overlay. Around or below the tower, leave four small blank areas along simple workflow paths where local labels will be overlaid later. Xiaohei stands lower-left or center-left, small and deadpan, looking up at the tower.

Xiaohei is the recurring small solid-black absurd operator creature with two white dot eyes, tiny thin legs, uneven hand-drawn body, blank serious expression; not cute, not heroic. KubeBlocks control tower is a calm infrastructure object: simple tower, console, antenna, workflow lanes, status lights. Database facilities are distant and dignified, very sparse.

Ian Xiaohei style: pure white background, minimalist black hand-drawn line art, slightly wobbly thin pen lines, lots of whitespace, clean absurd product-sketch feeling.

16:9 horizontal. Control tower is the main object, about 35-45% of canvas, with a blank status screen/panel large enough for a short two-line English overlay. Xiaohei should be smaller, observing rather than controlling. Orange workflow lines should be sparse and readable, leading through four small operation stations. Leave safe blank space near Xiaohei for one short local text overlay. Leave at least 35% blank white space.

Black line art only, with rare orange non-text workflow lines and tiny red/blue non-text status accents if needed. No colored text.

Do not draw any readable text, labels, pseudo-text, UI words, icons that look like words, or title. All final English text and labels will be overlaid later.

Object-native status screen/panel on the control tower is allowed as the only explicit text surface. No speech bubbles, no dialogue balloons, no ordinary text boxes, no caption cards, no placards, no labels, no title. Do not personify the tower. Do not make KubeBlocks look like a database engine. Do not show a dense dashboard or formal architecture diagram. Avoid gradients, shadows, paper texture, commercial vector style, cute mascot poster, children's illustration, crowded flowchart, and malformed text.

## Post Processing

- Source base: `source/panel-3-v4-base.png`
- Final single panel: `panel-3-v4.png`
- Deterministic overlay script: `build_panel3_v4.py`
- Font: Bradley Hand Bold with Chalkboard fallback
- Text color: black
- Ordinary text frames: none
