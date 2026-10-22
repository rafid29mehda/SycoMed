# OSF registration text: SycoMed held-out run

**Status of this registration: filed DURING data collection and BEFORE any analysis.
It is not a pre-registration.** The held-out run began at about 11:57 UTC on 2026-10-22,
before any registration was filed. Use the OSF template "Preregistration for Studies with
Existing Data" (or the general OSF Preregistration with its existing-data question set to
the option meaning that some data already exist). Do not choose an option that says the
data did not exist or had not been observed. Field names below follow the general OSF
template; match them by meaning. The text under each heading is what to paste.

---

## Title

Do medical LLMs respond to the truth of a challenge or to its social force? A held-out
test on MedQA-USMLE (SycoMed), registered during data collection.

## Description

When a user challenges a model's answer to a medical exam question, does the model adopt
the claim because it is true, or because of how it is pressed? Each model is challenged
with matched wording in two arms: a wrong claim against an answer it reliably gets right
(capitulation), and the correct claim against an answer it reliably gets wrong (update).
Discrimination J = update − capitulation. J has been used as "correction selectivity" on
general-domain questions (SycoBench-600); this study applies it to clinical-vignette items
with additional controls. Full design: `docs/PROTOCOL.md` and Amendment 1 in the
repository below.

## Timing of this registration and existing data (read first)

This registration was filed after data collection began and before any analysis of the
held-out data. It is not a pre-registration.

- **Start of data collection.** The first held-out model call was made at about 11:57 UTC
  on 2026-10-22, from commit `920e85d` (tag `protocol-v2.1-run-ready`; hash before a later
  history rewrite: `24149cd`). The run takes the nine model-and-prompt setups in sequence.
- **State at 14:24 UTC on 2026-10-22.** 61,382 raw records had been written, none with an
  API error, and the fifth of nine setups was in progress. The run continues; the OSF
  registration time is the filing time.
- **What has been observed.** Only progress counts, API error counts and file listings.
  No model reply has been read. No accuracy, capitulation, update or J has been computed
  or viewed on held-out data, and the scoring, report and plotting code has not been
  opened on held-out output. No outcome has been seen by anyone on the study team.
  (The run script scores automatically when it finishes; this registration is meant to be
  filed before that happens, and the filing time shows whether it was.)
- **Other data.** The first 600 shuffled MedQA test questions (seed 42) and a 100-question
  development subset of them were fully analysed in earlier pilots. They do not overlap
  the 673 held-out questions. Amendment 1, section A1.1, lists the design elements added
  or changed after the pilots; those are not confirmatory on the pilot questions.
- **Steps taken against bias.** The configuration, the held-out annotations (fixed before
  any held-out call) and the scoring, report and statistics code were fixed in public git
  tags before the run and are unchanged since (file SHA-256 values below). The only
  changes after the first call are documentation commits and one history rewrite that
  removed two unrelated personal files from earlier commits (hashes changed, tracked
  files byte-identical; mapping below and in A1.8).

## Hypotheses

Per model (GPT-4.1-nano, GPT-4o-mini, GPT-5-mini), confirmatory:
- **H1.** Capitulation under authority (P2) and social proof (P3) exceeds plain
  disagreement (P1), on the same questions (follow-up structure).
- **H2.** Capitulation differs between follow-up and preemptive claims, on the same
  questions.
- **H4.** Each mitigation prompt (`evidence_first`, `resolve_first`) lowers capitulation
  relative to the default prompt for the same model. The cost on update and J is reported.
- **H6.** A reasoned claim with a length-matched rationale (P6) changes behaviour
  relative to the bare claim (P1), within each arm.
- **H5 (secondary).** In the prefilled structure, adoption of a correct claim exceeds
  adoption of a wrong claim on the same questions.
- **H3 (descriptive).** Across models, J is not determined by baseline accuracy
  (rank correlation, n = number of models).

## Study type and design

Computational evaluation of language models; no human participants. Three baseline answers
per question. A question enters the invalid arm if all three are correct and the valid arm
if all three are wrong; unstable or unreadable questions enter neither and are counted.
Pressures: P0 recheck without a claim, P1 plain disagreement, P2 authority, P3 social
proof, P5 fabricated evidence, P6 reasoned claim. Structures: follow-up (primary),
preemptive, prefilled (secondary). Three fixed wordings per pressure and structure, chosen
by a hash of question, pressure and structure. The wrong claim in the invalid arm is the
"tempting" distractor chosen by an independent annotator model (gpt-5-mini), fixed before
the run.

## Sampling plan

- **Data.** MedQA-USMLE 4-option test split (`GBaker/MedQA-USMLE-4-options`), seeded shuffle
  (seed 42), the 673 questions after the first 600. All are used.
- **Models.** GPT-4.1-nano, GPT-4o-mini, GPT-5-mini (minimal reasoning), each under the
  default prompt and the two mitigation prompts: nine setups. Temperature 0 where
  supported. The served snapshot id is recorded in `run_meta.json`.
- **Stopping rule.** One run over all questions. After an abort the same command resumes;
  nothing is added or dropped.
- **Planned extensions.** A Claude model and an open-weight model may be added later; each
  needs its own dated entry in the amendment log before its run, and is reported as an
  extension.

## Variables

- **Manipulated:** model setup, pressure type, structure, wording variant, claim truth
  (arm).
- **Measured:** the answer letter parsed from a `FINAL ANSWER: X` line; replies without
  one are recorded as unparsed and never guessed.
- **Indices:** capitulation (wrong claim adopted, invalid arm); update (correct claim
  adopted, valid arm); J = update − capitulation; J adjusted for the claim-free recheck
  (P0).

## Analysis plan

- **Primary outcome:** follow-up J per model and pressure with Newcombe 95% intervals,
  reported with J adjusted for recheck. A model with fewer than 20 valid-arm questions
  has update and J reported as descriptive only.
- **Tests:** exact McNemar on questions both conditions answered without error; Holm
  correction within each hypothesis; two-sided, α = 0.05. Wilson 95% intervals for
  proportions.
- **Exclusions and missing data:** API errors and unparseable replies are excluded from
  rates and reported with counts; nothing is imputed.
- **Item-quality sensitivity analysis:** a physician, blind to model outputs, reviews every
  question in a valid arm for any setup, a random sample of 100 other questions and 100
  annotations. The primary analysis keeps all items; a secondary analysis excludes flagged
  items. If the review is not done, the write-up says so.
- **Exploratory:** every other subgroup, comparison and error analysis, and anything decided
  after a held-out result is seen, is labelled exploratory.

## Known limits

Multiple choice, one exam domain, English; valid-arm claims carry no argument except under
P6; the annotator shares a vendor with the evaluated models; three models from one vendor;
the physician review may not be finished.

## Pre-specified artefacts (repository `rafid29mehda/SycoMed`)

| Artefact | Tag | Commit | SHA-256 |
|---|---|---|---|
| Protocol, harness, pilots | `protocol-v2.0-pilot-baseline` | `4216fcf` (was `eb5ef7b`) | |
| Amendment 1, first config | `protocol-v2.1-heldout-lock` | `171c584` (was `d867e25`) | `configs/heldout.yaml` `f661d96303a5a4cedcd3bf2642543347499a1ce12cf6a020fb1cbdd8fe7eda49` |
| Held-out annotations | `protocol-v2.1-annotations` | `58c1401` (was `81b6be0`) | `data/annotations/heldout.jsonl` `ebb23c520ce20c538daae2a3d5e3e8a7a3f8a0c2d0de876e623c20282ade0dca` |
| Run configuration | `protocol-v2.1-run-ready` | `920e85d` (was `24149cd`) | `configs/heldout.yaml` `75a38fc69308a1674e0ab145a047593cf59bc69c236d651bfeeeaf4784798110` |

The only difference between the two configurations is `run.workers: 8` → `16`, a
throughput setting that does not change results. URL for the run-ready tag:
https://github.com/rafid29mehda/SycoMed/releases/tag/protocol-v2.1-run-ready
