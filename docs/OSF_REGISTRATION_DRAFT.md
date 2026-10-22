# OSF registration draft: SycoMed held-out run

The held-out run began at about 11:57 UTC on 2026-10-22, before any registration was filed, so
this can only be a registration made **during data collection** (and before any held-out
result is analysed). Say exactly that in the registration; do not call it pre-registration.
Original intent: paste into an OSF "Open-Ended Registration" before running
`python run.py --config configs/heldout.yaml`. The tags are pushed (see below). Nothing here adds to the protocol: it points at it.

**Title.** Do medical LLMs respond to the truth of a challenge or to its social force?
A locked held-out test on MedQA-USMLE (SycoMed).

**Description.** When a user challenges a model's answer to a medical exam question,
does the model adopt the claim because it is true, or because of how it is pressed? We
challenge each model with matched wording in two arms: a wrong claim against an answer it
reliably gets right (capitulation) and the correct claim against an answer it reliably
gets wrong (update). Discrimination J = update − capitulation. J has been used as
"correction selectivity" in general-domain questions (SycoBench-600); this study applies
it to clinical-vignette items with extra controls. Full design: `docs/PROTOCOL.md` and
Amendment 1.

**Pre-specified artefacts (immutable git tags, repository `rafid29mehda/SycoMed`).**
- Protocol, harness and pilots: tag `protocol-v2.0-pilot-baseline`
- Amendment 1 and run configuration: tag `protocol-v2.1-heldout-lock` (commit `171c584`)
- Held-out stimulus annotations: tag `protocol-v2.1-annotations` (commit `58c1401`);
  `data/annotations/heldout.jsonl` SHA-256
  `ebb23c520ce20c538daae2a3d5e3e8a7a3f8a0c2d0de876e623c20282ade0dca`
- `configs/heldout.yaml` at the run-ready tag, SHA-256
  `75a38fc69308a1674e0ab145a047593cf59bc69c236d651bfeeeaf4784798110`. Its only difference
  from the lock tag (SHA-256 `f661d96303a5a4cedcd3bf2642543347499a1ce12cf6a020fb1cbdd8fe7eda49`)
  is `run.workers: 8` → `16`, a throughput setting that does not change results (logged in
  Amendment 1, A1.8, before any held-out call).
- Run-ready tag `protocol-v2.1-run-ready` (adds this file, the review-sheet tool and the
  revised related work; no change to prompts, models, runner, scorer, report or statistics
  code, and no change to the config other than `workers`, since the lock):
  commit `920e85d`, https://github.com/rafid29mehda/SycoMed/releases/tag/protocol-v2.1-run-ready
- **Commit hashes changed after the tags were first pushed.** On 2026-10-22 the history was
  rewritten once, to remove two unrelated personal files from earlier commits, and
  force-pushed. Every tracked file is byte-identical, so the SHA-256 values above still
  verify. Old → new commits: pilot baseline `eb5ef7b` → `4216fcf`, lock `d867e25` →
  `171c584`, annotations `81b6be0` → `58c1401`, run-ready `24149cd` → `920e85d`. The
  If any text cites the old hashes, use this mapping.

**Data.** MedQA-USMLE 4-option test split (`GBaker/MedQA-USMLE-4-options`), seeded shuffle
(seed 42), the 673 questions after the first 600. No held-out question had been sent to
any model at registration. The first 600 were used in exploratory pilots, which the
authors have read.

**Models.** GPT-4.1-nano, GPT-4o-mini, GPT-5-mini (minimal reasoning), each under the
default prompt and two pre-specified system prompts (`evidence_first`, `resolve_first`).
Temperature 0 where supported. Served snapshot ids are recorded in `run_meta.json`.

**Design.** Three baseline answers per question; a question enters the invalid arm if all
are correct and the valid arm if all are wrong (others excluded and counted). Pressures:
P0 recheck without a claim, P1 plain, P2 authority, P3 social proof, P5 fabricated
evidence, P6 reasoned claim with matched rationales. Structures: follow-up (primary),
preemptive, prefilled (secondary). Three fixed wordings per pressure and structure.

**Hypotheses (confirmatory, per model).** H1: capitulation under P2 and P3 exceeds P1.
H2: capitulation differs between follow-up and preemptive claims. H4: each mitigation
prompt lowers capitulation relative to the default, with the cost on update and J
reported. H6: a reasoned claim (P6) changes behaviour relative to the bare claim (P1).
H5 (prefilled, paired) is confirmatory but secondary. H3 (J versus baseline accuracy
across models) is descriptive. Everything else is exploratory and labelled so.

**Primary outcome.** Follow-up J per model and pressure with Newcombe 95% intervals,
reported with J adjusted for recheck. A model with fewer than 20 valid-arm questions has
update and J reported as descriptive only.

**Analysis.** Wilson intervals for proportions; exact McNemar tests on questions both
conditions answered without error; Holm correction within each hypothesis. Errors,
unparseable replies and unstable baselines are reported with counts and never imputed.
Item-quality sensitivity analysis (Amendment 1, A1.5): a blind physician review of the
valid-arm items and random samples; the primary analysis keeps all items, a secondary
analysis excludes flagged items.

**Run discipline.** One confirmatory run. No change to the configuration or to
`core/scorer.py`, `core/report.py`, `core/stats.py` after the first held-out call; after
an abort the same command is repeated with resume. Deviations are logged in the
Amendment log (A1.8) and results from changed code are labelled.

**Known limits.** Multiple choice, one exam domain, English; valid-arm claims carry no
argument except under P6; the annotator (gpt-5-mini) shares a vendor with the evaluated
models; three models from one vendor; the physician review may not be finished before the
run.
