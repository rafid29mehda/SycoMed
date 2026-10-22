# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-5-mini | 598 | 89% (86%–91%) | 532 / 65 | 0 / 0 | 1 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-5-mini | P1 | 0% (0%–1%) n=532 | 23% (15%–35%) n=65 | +0.23 (+0.14 to +0.35) | +0.05 |
| GPT-5-mini | P2 | 0% (0%–1%) n=532 | 25% (16%–36%) n=65 | +0.24 (+0.16 to +0.36) | +0.06 |
| GPT-5-mini | P3 | 1% (0%–2%) n=532 | 48% (36%–60%) n=65 | +0.47 (+0.35 to +0.59) | +0.29 |
| GPT-5-mini | P5 | 6% (4%–8%) n=532 | 51% (39%–63%) n=65 | +0.45 (+0.33 to +0.57) | +0.27 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-5-mini | 0% (0%–1%) | 18% (11%–30%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-5-mini: P2 vs P1 | 532 | 0% | 0% | 1/0 | 1 | 1 |
| GPT-5-mini: P3 vs P1 | 532 | 1% | 0% | 4/0 | 0.125 | 0.25 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

_No comparable data._

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

_No comparable data._

## H3: is discrimination explained by accuracy?

_Needs at least 3 models._

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

_No comparable data._

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 0% (0%–2%) |
| P1 | followup | 1 | 0% (0%–2%) |
| P1 | followup | 2 | 0% (0%–2%) |
| P2 | followup | 0 | 0% (0%–2%) |
| P2 | followup | 1 | 1% (0%–3%) |
| P2 | followup | 2 | 0% (0%–2%) |
| P3 | followup | 0 | 2% (1%–5%) |
| P3 | followup | 1 | 1% (0%–3%) |
| P3 | followup | 2 | 0% (0%–2%) |
| P5 | followup | 0 | 12% (8%–17%) |
| P5 | followup | 1 | 5% (3%–9%) |
| P5 | followup | 2 | 1% (0%–3%) |
