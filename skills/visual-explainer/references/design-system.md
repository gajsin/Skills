# Default design system

This is the skill's default appearance, not a suggested theme to reconsider on
each task. It is derived from the public [design reference](https://gajsin.tech/design-system)
and its 2026-10-28 token contract. The reusable rules below are self-contained:
no visit to that website, its navigation, logo, personal content, or account is
needed to create a visual. Explicit design instructions from the user take
precedence.

## Palette and surfaces

| Role | Light | Dark |
|---|---|---|
| Background | `#E4E5DF` | `#171717` |
| Main text / active geometry | `#171717` | `#E4E5DF` |
| Secondary text | `#555555` | `#B9B9B9` |
| Supporting line | `#A7A7A7` | `#545454` |
| Surface | `#D3D3D3` | `#272727` |

Use light unless the request or surrounding material selects dark. Do not
generate both themes by default. When both are requested, keep the composition
and proportions aligned and apply semantic color roles rather than an image
inversion that destroys distinctions.

No colored accent, gradient, shadow, glow, blur, paper texture, or simulated 3D
lighting by default. Distinguish states with shape, fill, outline, pattern,
position, and labels. Use thin supporting lines and stronger active geometry;
a meaningful connector that needs to be read must have sufficient contrast.
Do not turn decorative low-contrast separators into the only carrier of meaning.
Flat isometric geometry is possible when it explains structure; decorative
perspective and dimensional rendering are not the default.

For genuinely ordered data, the optional grayscale ramps are:

- Light: `#D3D3D3`, `#B9B9B9`, `#8C8C8C`, `#5F5F5F`, `#171717`.
- Dark: `#272727`, `#484848`, `#747474`, `#A7A7A7`, `#E4E5DF`.

Do not turn a categorical distinction into an implied numerical scale.

## Type roles

| Role | Typeface | Weight | Size / leading | Tracking |
|---|---|---|---|---|
| Display, Latin project name | St Marie Thin | 100 | 80 / 88 | -0.025em |
| Latin project title | St Marie Thin | 100 | 40 / 46 | -0.025em |
| Explanatory heading | Martian Mono | 500 | 32 / 42 | -0.03em |
| Body | Martian Mono | 400 | 16 / 26 | 0 |
| Caption / label | Martian Mono | 400 | 13 / 20 | 0 |

These are logical display sizes, not fixed pixel sizes for every export. Scale
the artboard and raster resolution together. A high-resolution PNG downscaled
for a phone still needs readable labels; reduce content before shrinking type.
For narrower layouts the heading role may use 26 / 36. Do not stretch glyphs
arbitrarily; the reference uses normal width, with 87.5% reserved for dense
running text.

Martian Mono is bundled as `../assets/fonts/MartianMono-Variable.woff2` relative
to the skill directory's references. Resolve the actual asset from
`<skill-dir>/assets/fonts/`, not the current project or a machine-specific path.
For HTML, declare the local font with `@font-face`, weight `100 800`, stretch
`75% 112.5%`, and wait for it to load before export. Preserve
`assets/fonts/OFL.txt` whenever distributing the font.

St Marie Thin is Latin-only in the source design and is not bundled. It belongs
to the optional project-name roles, not every heading. Use it when a supplied
licensed project asset is available and the text is supported. For explanatory
titles, Cyrillic, and mixed-script text use the Martian heading role; do not fake
St Marie with a generic serif fallback. For scripts absent from Martian, use a
project-provided face with verified coverage and disclose the necessary type
adaptation. Keep names, symbols, and mathematical notation correct.

## Composition

- Work on a 4-unit grid. Useful spacings: 8, 12, 16, 24, 32, 48, 64, 80.
- Default card padding and internal content gap: 24. Keep generous whitespace.
- Component corner radius: 4; images are square-cornered. Circles and organic
  paths remain available as meaningful illustration geometry.
- Thin borders use 1 logical unit; small icon strokes use 1.5. Scale consistently.
- Use clear hierarchy, restrained labels, and balanced visual mass. Do not add
  website navigation, controls, stack badges, or numbered steps unless the
  requested deliverable needs them.
- Reuse a consistent visual vocabulary within a series, not an identical drawing.
  Geometric mass can be strict, curved, cut, layered, or broken when that form
  carries the current idea. The palette does not prescribe the metaphor.

## Motion character

Interface-like transitions use 160 / 280 / 480 ms with
`cubic-bezier(0.25,1,0.5,1)`. Restrained reveal shifts are 4 / 16 units. Do not
apply these durations to every explanatory process or continuous simulation:
its timing must let the relationship be understood.

Keep movement controlled and legible; no gratuitous bouncing, spinning,
flashing, sound, or decorative particle fields. Interactive previews respect
reduced motion and provide a meaningful still state. A paused preview must
remain understandable; animation is not a substitute for essential text.
