# Evidence about writing style and authorship

Checked on 8 October 2026. This is background for evidence questions, not a detector
or a compulsory part of editing. Do not infer authorship from punctuation or a word list.

## Upstream

[Humanizer 3.1.0](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md)
adds reader-context editing and revises document-about-itself examples. Its patterns
are editorial heuristics. An upstream version does not validate this editing
workflow.

## Recent primary research

[Writerslogic at PAN 2026](https://arxiv.org/abs/2610.03565), submitted 2 October:
reports transfer failures for generator-specific features under domain shift and
better results from a calibrated ensemble on evaluated tasks. The author describes
the framework as a hypothesis with limited corroboration. It does not establish a
universal blacklist of phrases or validate this editing skill.

[AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not](https://arxiv.org/abs/2608.27855),
revised 22 September: generation and editing showed different stylistic traces in
the evaluated corpus. The authors note mainly English long-form domains, limited
editor coverage, and associational rather than causal feature analysis. Those results
do not establish detection accuracy for Russian correspondence or this editing workflow.

## Practical interpretation

Preserve useful author-specific variation and natural grammar. Evaluate an edit by
meaning, voice, reader needs, and readability. Do not present a neat list, a dash,
high lexical diversity, a date cutoff, or a detector score as definitive authorship
evidence. Do not fabricate anecdotes or mistakes to manipulate such cues.

## Editorial practice reviewed on 26 October 2026

These sources inform editorial choices; they do not experimentally validate this
skill or require runtime browsing, a style questionnaire, or another reviewer:

- [Ilyahov and Sarycheva: business correspondence](https://letters.glvrd.ru/):
  reader needs and a clear thought matter more than ceremonial polite formulas.
- [Sarycheva: payment reminders](https://bureau.ru/soviet/20200322/): a concrete
  request and useful context can remain respectful without forced affection.
- [Ilyahov: workplace messages](https://alpinabook.ru/blog/3-nelovkie-situatsii-v-pismakh-po-rabote/):
  tone follows relationships and purpose. A reminder's actual deadline or offer of
  help cannot be imported into an unrelated message.
- [Mailchimp: voice and tone](https://styleguide.mailchimp.com/voice-and-tone/):
  adapt tone to the recipient and situation, rather than adding compulsory humor.
- [Shelter Humanizer RU](https://github.com/IT-Shelter-Labs/Shelter-Humanizer/blob/main/skills/shelter-humanizer-ru/SKILL.md):
  useful Russian-specific reminders about case government and preserving register.
  No application code or source passages are included here.

The Russian pairs in examples.md are locally authored teaching cases from fixed
facts, not quotations from those publications or a corpus of private messages.
No detector score or token reduction is used as a substitute for semantic fidelity.
