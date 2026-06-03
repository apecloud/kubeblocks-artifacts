# Daily 2026-06-03 Panel 4 v4

## Locked Text

- EN Xiaohei: `…I said the words.`
- EN counter: `Sleep: jinxed.`
- CN Xiaohei: `……我真说出口了。`
- CN counter: `睡眠：乌鸦嘴`

## Base Image Prompt

Generate a clean text-free base illustration for Panel 4 of `The Q-Word / 乌鸦嘴`. Xiaohei is deadpan and half-buried in a pile of blank red alert cards, acknowledging the jinx. Place a small blank sleep/status counter in the lower-left as an object-native display. Keep the punchline simple: only Xiaohei, the alert pile, and the counter should matter.

Style: Ian Xiaohei minimalist black hand-drawn line art, 16:9 horizontal, large whitespace, red alert cards as the only strong color.

Strict exclusions: no readable text, pseudo-text, speech bubbles, ordinary text boxes, title, brand/logo, Kubernetes mark, dense background, or product explanation. Counter screen must be blank for later local overlay.

## Post Processing

- Source base: `source/panel-4-v4-base.png`
- Final panels: `panel-4-v4.png`, `panel-4-v4-cn.png`
- Deterministic overlay script: `build_comic_v4.py`
- Counter text is object-native inside the counter display

