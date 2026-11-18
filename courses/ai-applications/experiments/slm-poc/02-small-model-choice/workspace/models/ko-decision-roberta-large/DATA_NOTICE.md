# Attribution and modification notice

KLUE Benchmark contributors; Sungjoon Park et al. (2021), https://arxiv.org/abs/2105.09680.
Source: https://huggingface.co/datasets/klue/klue/tree/349481ec73fff722f88e0453ca05c77a447d967c
KoBEST / SK Telecom; Dohyeong Kim et al. (2022), https://arxiv.org/abs/2204.04541.
Source: https://huggingface.co/datasets/skt/kobest_v1/tree/a5ea15e3ac77ed694b79f6204eb31889a2ba989f
Real adapted rows: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/.
Retain authors, source, license, and modification notices; share adapted data under the same or compatible license.
Original cards and legal notices are recorded in manifest.json inputs and license_evidence_paths.
Modifications: inherited normalization/deduplication/connected-group holdout exclusions; nested seed42 selection;
task-specific Korean/English candidate descriptions and state field markers; complete-group prompt assignment;
three development protocols with correlated repeated source rows. Original source text, labels and STS score targets remain intact.
Synthetic policy probes are project-created diagnostic templates, not human annotations.
Data licensing does not by itself determine model-weight release conditions.

Fullpool modification: extend only unused eligible official train source rows in the same five tasks; preserve every criteria19k derived train row and evaluation bytes. Assign fixed prompt variants only to new complete groups. No replication or additional corpus.

Stage 2 addition: KLUE-RE official train split (same KLUE source and revision, CC BY-SA 4.0) rendered as 30-way Choice rows with the label names as options; sentence text, entities and labels are unchanged. 300 train rows are held out for monitoring.

Stage 3 additions: KoBEST-HellaSwag official train split (same KoBEST source and revision, CC BY-SA 4.0) rendered as 4-way Choice rows, half with letter-labelled options; contexts, endings and labels unchanged. English rows from `jaredpalmer/kev-suites` `public-pool-v6/train.jsonl` (revision cc4bac803e), restricted to seven sources with open terms: Banking77 (CC BY 4.0), BoolQ and DBpedia-14 (CC BY-SA 3.0), ARC (CC BY-SA 4.0), CommonsenseQA (MIT), OpenBookQA (Apache-2.0), MNLI (permissive mix). Not used: Yelp, Amazon reviews, AG News, IMDb, SST-5, TREC. None of this data is redistributed in this repository.

Note-taking additions (stage 4): query-passage relevance, category and tag questions built by re-rendering public datasets downloaded from the Hugging Face Hub. Texts, labels and relevance judgements are unchanged; prompts, option letters and negative examples were added. Sources and the license tag each carries on the Hub: Mr. TyDi (castorini/mr-tydi, Apache-2.0), TyDi QA (google-research-datasets/tydiqa, Apache-2.0), KLUE-MRC and KLUE-YNAT (klue/klue, CC BY-SA 4.0), CoNaLa (neulab/conala, MIT), MASSIVE (AmazonScience/massive via mteb/amazon_massive_intent and mteb/amazon_massive_scenario, CC BY 4.0), SIB-200 (Davlan/sib200, CC BY-SA 4.0), DBpedia-14 (fancyzhx/dbpedia_14) and its Korean translation (KETI-AIR/kor_dbpedia_14), CC BY-SA 3.0, arXiv abstract metadata (gfissore/arxiv-abstracts-2021, CC0 1.0), GoEmotions (google-research-datasets/go_emotions, Apache-2.0), K-MHaS (jeanlee/kmhas_korean_hate_speech, CC BY-SA 4.0). Evaluation only: Belebele (facebook/belebele, CC BY-SA 4.0) and the bilingual-v1 suite of hyeondata/brain-openkit (MIT). None of this data is redistributed in this repository.
