# Research figures

## Conceptual research instrument

`assets/images/research-instrument.webp` is a conceptual illustration of the
research apparatus. It presents four stages from left to right: a game
environment, AI suggestion cards, a human decision point, and accumulated event
records. The image is an explanatory model, not an actual game screenshot or a
visualization of measured results. It contains no rendered labels, values, or
statistical claims; explanatory labels belong in accessible HTML near the
figure.

Suggested alternative text:

> Conceptual research instrument with a tiled game board, AI suggestion cards,
> a human choosing between two options, and a tray of event records.

The artwork uses an orthographic camera, soft studio lighting, and a warm ivory,
sage, clay, and ochre palette. Its rounded clay-like forms are designed to remain
recognizable at responsive web sizes and to sit naturally on the site's paper
background.

To regenerate the figure from the repository root with Blender 5.0.1:

```sh
/usr/bin/blender --background --python scripts/render_research_figure.py
```

The script uses no external textures or fonts. It recreates the full scene,
saves the editable source as `artwork/research-instrument.blend`, and writes a
1600 × 1000 RGB WebP directly to
`assets/images/research-instrument.webp`. The checked image should remain below
450 KB after regeneration.
