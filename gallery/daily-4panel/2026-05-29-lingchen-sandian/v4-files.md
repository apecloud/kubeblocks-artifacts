# Ep1 v4 Files

## Final Images

- `comic-v4.png`: original high-resolution 2x2 final image
- `comic-v4-review.png`: scaled review version for chat and quick whole-strip QA
- Public-facing final images keep the episode title only. Internal brand/version/meta text such as `KubeBlocks comic v4` must not appear in the artwork.

## Approved Panels

- `panel-1-v4.1.png`
- `panel-2-v4.1.png`
- `panel-3-v4.png`
- `panel-4-v4.png`

## Source Bases

- `source/panel-1-v4-base.png`
- `source/panel-2-v4-base.png`
- `source/panel-3-v4-base.png`
- `source/panel-4-v4-base.png`

## Build Scripts

- `build_panel1_v4.py`
- `build_panel2_v4.py`
- `build_panel3_v4.py`
- `build_panel4_v4.py`
- `build_comic_v4.py`

## QA Notes

- English comic text only.
- Readable text is black by default.
- Public-facing artwork keeps the episode title but excludes internal version numbers, product-name meta labels, and project tags.
- No ordinary speech bubbles, dialogue balloons, caption cards, or normal text boxes.
- Object-native text surfaces only: phone screen, robot sign, tower screen, sleep counter.
- Color is limited to non-text alert/workflow/status accents.
- Panels were generated and reviewed one by one before 2x2 assembly.
