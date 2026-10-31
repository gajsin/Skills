# SVG master and exports

The master is real vector artwork. Use paths, shapes, groups, text, clipping,
masks, and reusable vector definitions. Do not embed a PNG, JPEG, screenshot,
or generated image under an `.svg` filename. A font embedded as font data is
not a bitmap illustration.

## Make the master portable

- Set `xmlns`, `viewBox`, and explicit output dimensions. Give meaningful
  groups stable identifiers for editing and optional animation.
- Include a title and useful description. Keep visible captions in the user's
  language; descriptions must match what the image actually shows.
- Use the bundled design roles for fills, lines, and type. Scope identifiers
  when several SVGs share a page so clips, markers, and masks do not collide.
- Use the bundled Martian Mono. For a standalone SVG rendered in a browser,
  an internal `@font-face` with a base64 `data:font/woff2` source makes the font
  independent of local paths. Declare its real weight and width axes. Preserve
  the accompanying OFL notice. Do not embed unsupported glyph substitutions.
- Some SVG renderers ignore embedded webfonts. Check the chosen renderer's
  actual font loading, or supply the font through its supported font input.
  Do not infer font fidelity from an existing font-family declaration.
- Avoid external image/font URLs and local absolute paths in the delivered
  master. Do not add scripts to a static illustration. Keep an editable text
  master if a separate outlined-text export is explicitly requested.

## Render without image generation

Use an already available SVG renderer or browser. Open the SVG at its intended
logical size; wait for the font to load, check the frame and text, then export
the requested raster dimensions or scale factor. An inline HTML wrapper is
useful for inspection, but it does not replace checking the standalone master.

Keep the SVG source alongside a PNG export. Reopen the exported PNG and inspect
it at the destination width. Check missing glyphs, fallback fonts, clipping,
background, and meaningful overlaps. Confirm that raster dimensions match the
request. Renderer success alone does not prove that the idea is understandable.

A browser, Playwright, Cairo, or another SVG renderer is a host capability,
not a mandatory dependency of the skill. Do not install a large stack merely
to preview an SVG. If a requested PNG or video export cannot be made in the
available environment, deliver the real SVG and state the specific export
limit; do not claim the missing format was produced.
