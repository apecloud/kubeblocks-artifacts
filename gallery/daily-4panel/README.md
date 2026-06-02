# Daily 4-Panel Comics

Each 4-panel comic lives in its own folder:

```text
gallery/daily-4panel/<date>-<episode-slug>/
```

Do not place final comic images directly under `gallery/daily-4panel/`.

## Required Outputs

Every episode should ship both English and Chinese versions from the same approved text-free source bases.

- `comic-v4.png` — English original 2x2 final comic
- `comic-v4-review.png` — English review-scaled 2x2 comic
- `comic-v4-cn.png` — Chinese original 2x2 final comic
- `comic-v4-review-cn.png` — Chinese review-scaled 2x2 comic
- `panel-*-v4*.png` — English locked single panels
- `panel-*-v4-cn.png` — Chinese locked single panels
- `source/panel-*-v4-base.png` — text-free source bases
- `build_*_v4*.py` — deterministic local build scripts
- `panel-*-v4-prompt.md` — prompt records
- `v4-files.md` — file manifest and episode notes

## Visual Rules

- Keep public-facing artwork free of internal meta, version labels, product watermarks, brand logos, and Kubernetes logos.
- Keep readable text black by default.
- Avoid ordinary speech bubbles, dialogue balloons, caption cards, and normal text boxes.
- Put text only in open whitespace or object-native surfaces such as screens, signs, cards, and counters.
- Use color only for small non-text alert/workflow/status accents.
- Keep technical names such as `PG`, `Redis`, `Kafka`, `MySQL`, and `*.sh` labels in English unless a script explicitly says otherwise.
