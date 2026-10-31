---
name: visual-explainer
description: "Author meaningful SVG illustrations and explanatory diagrams directly in code, using a monochrome design system. Animate when requested. Invoke explicitly."
license: MIT
disable-model-invocation: true
---

# Visual Explainer

Create a visual that explains the requested idea: an editorial illustration,
diagram, comparison, instructional card, or a short animation. Topics can belong
to any domain. The bundled [design system](references/design-system.md) defines
the default appearance; the subject, metaphor, composition, and visual structure
must come from the current request. Use the user's language.

Create all artwork directly as native SVG geometry and text. Do not use imagegen,
other image-generation tools or APIs, generated-image tracing, or bitmaps hidden
inside SVG. The agent designs the image and writes its vector source; an external
image model is not part of this workflow.

This is an explanation workflow, not a logo interview, UI redesign, or automatic
video-production job. Create only the requested deliverables. A normal request
should produce an artifact without a setup questionnaire.

## Establish what needs explaining

Read the supplied text, facts, references, audience, and destination. Separate
confirmed facts from assumptions. Identify the one relationship or change the
viewer should understand; a requested series may contain several distinct ideas.
Infer ordinary presentation choices. Ask only when a missing fact would materially
change the explanation or its correctness.

If the request is to clarify an existing visual, preserve its correct content and
approved features. Do not replace it with a new concept just because this skill
was invoked. Do not edit a website or publish material without that scope.

## Turn the idea into a visual mechanism

Choose the requested visual form before building. For an illustration, read
[illustration.md](references/illustration.md) and develop an editorial image;
do not default to boxes and arrows. For a diagram, make the relationships
explicit. Neither form is universally preferable.

- Choose a representation that exposes the relationship: sequence, spatial
  constraint, comparison, hierarchy, feedback, transformation, or another useful
  structure. Use a literal diagram when it is clearer than a metaphor.
- Assign meaning to the important marks, connections, positions, and changes.
  Make cause, direction, grouping, and before/after states distinguishable.
  Do not force every subject into circles, arrows, funnels, or the reference video.
- A metaphor may simplify the subject; it must not add an unsupported causal claim,
  change its logic, or present qualitative sizes as measured data. Use supplied
  values faithfully when drawing actual charts; label an illustrative schematic.
- Test the concept internally: can you explain how the drawing communicates the
  idea, and what a viewer could misunderstand? A caption may orient the reader,
  but should not have to invent meaning for decorative geometry afterwards.

When variants are requested, make the requested number visually inspectable.
Explore different useful mechanisms before tiny contour or spacing changes.
Keep semantic alternatives distinct from refinements of an approved direction;
preserve approved source files and identify versions clearly.

## Build in the bundled visual language

Read [design-system.md](references/design-system.md) before drawing. Its paper/ink
palette, typography, spacing, flat surfaces, and motion character apply by default
to every subject. Do not reselect a style for each illustration. Explicit user
design requirements override this default; a topic alone does not.

Use native SVG for geometric artwork, precise flat fills, editable diagrams,
and exact labels. SVG can draw expressive silhouettes, objects, and organic
contours; it does not imply a flowchart. Build paths, layers, negative space,
repeated geometry, clips, and masks as the concept needs them. Code may calculate
geometry; it must not merely call an image generator. Keep labels as real text.
Correct material mismatches before calling an image final. A requested concept
study may expose unresolved choices; do not silently downgrade a finished-artwork
request to a study. Deliver the drawing, not just instructions for making it.

Use the bundled Martian Mono font for supported text. Use the design reference's
font roles and script-coverage rules; do not silently render missing glyphs in a
different face. Keep text readable at the intended display size. Choose the
canvas for the destination rather than making every output a poster or card.

Deliver an editable, self-contained `.svg` master. Read
[svg-export.md](references/svg-export.md) when preparing the master or exports.
PNG is an optional raster export of this SVG, never an image-generation step.
Use an available SVG renderer or browser when PNG is requested; do not impose a
new service or account. Make exports independent of local machine paths and
verify required assets load. Preserve font notices when copying the bundled font.
Never label a renamed raster file as SVG or promise an export not produced.

## Animate only when requested

Read [motion.md](references/motion.md). Define what movement explains before
animating it. Reuse an available host animation workflow and its renderer; follow
its approval and verification rules. No specific commercial tool, account,
operating system, or installed sibling skill is required for static illustrations.
If a requested export cannot be produced, state the missing capability and the
actual artifact available instead of treating a preview as the finished export.

## Check the artifact and hand it over

Open the actual render at its intended display width, not just the large export.
Check the visual claim against the input, the meaning of connections, reading
order, labels, contrast, and clipping. Simplify or reflow small text rather than
approving an unreadable thumbnail. Distinguish requested content from your
explanatory assumptions. For a series, retain consistent meanings and styling
without repeating one composition.

Show or link the artifact first. Add a short explanation of its visual mechanism,
the delivered formats, and any material limitations. Report what was inspected;
do not claim approval, accessibility, or semantic accuracy from a successful
render command alone.
