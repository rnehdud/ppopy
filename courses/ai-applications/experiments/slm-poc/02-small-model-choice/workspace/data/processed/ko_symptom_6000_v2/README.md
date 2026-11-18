# Korean symptom decision pilot: 6,000 examples

This is an exploratory local research dataset, not a human-reviewed gold
corpus or a medical dataset. It is not 6,000 separate conversations: it has
6,000 unique `(utterance, target symptom, previous value)` decisions and 2,464
distinct utterances. The target is `present`, `absent`, `unchanged` or
explicit `unknown` for one of five symptoms.

- 5,000 decisions are generated from assistant-authored Korean templates.
- 1,000 decisions are sampled from user turns of the locally downloaded
  [KLUE / Wizard of Seoul training split](https://huggingface.co/datasets/klue/klue).
  These are dialogue-state data in other domains, not skin-condition labels.
  A keyword filter creates provisional `unchanged` labels: they require review.
- `heldout_cases.json` has 20 assistant-authored multi-turn scenarios; labels
  are not independently reviewed. Exact text overlap with this training set,
  prior training and previously reported cases is checked in the training
  script. Shared authorship and semantic similarities mean this is not a
  representative real-world benchmark.
- The source KLUE card states CC BY-SA 4.0. Review the original dataset and
  applicable attribution/share-alike terms before redistributing derivatives.

`manifest.json` fixes counts and SHA-256 values. The builder intentionally
refuses to overwrite a dataset directory; this v2 supersedes a draft v1 whose
evaluation text overlapped earlier development examples.
