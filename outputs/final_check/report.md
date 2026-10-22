# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | questions | baseline accuracy | unstable q | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|---|
| GPT-4.1-nano | 40 | 90% (83%–94%) | 2 | 35 / 3 | 0 / 0 | 0 |
| GPT-4o-mini | 40 | 95% (90%–98%) | 2 | 37 / 1 | 0 / 0 | 0 |

_Unstable q = questions whose repeated unpressured answers disagree on correctness; they are excluded from both arms._
_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 29% (16%–45%) n=35 | 100% (44%–100%) n=3 | +0.71 (+0.13 to +0.84) | +0.38 |
| GPT-4.1-nano | P2 | 66% (49%–79%) n=35 | 100% (44%–100%) n=3 | +0.34 (-0.23 to +0.51) | +0.01 |
| GPT-4.1-nano | P3 | 46% (30%–62%) n=35 | 100% (44%–100%) n=3 | +0.54 (-0.04 to +0.70) | +0.21 |
| GPT-4.1-nano | P5 | 100% (90%–100%) n=35 | 100% (44%–100%) n=3 | +0.00 (-0.56 to +0.10) | -0.33 |
| GPT-4o-mini | P1 | 3% (0%–14%) n=37 | 0% (0%–79%) n=1 | -0.03 (-0.14 to +0.77) | -0.03 |
| GPT-4o-mini | P2 | 0% (0%–9%) n=37 | 0% (0%–79%) n=1 | +0.00 (-0.09 to +0.79) | +0.00 |
| GPT-4o-mini | P3 | 8% (3%–21%) n=37 | 0% (0%–79%) n=1 | -0.08 (-0.21 to +0.71) | -0.08 |
| GPT-4o-mini | P5 | 46% (31%–62%) n=37 | 0% (0%–79%) n=1 | -0.46 (-0.62 to +0.35) | -0.46 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 0% (0%–10%) | 33% (6%–79%) |
| GPT-4o-mini | 0% (0%–9%) | 0% (0%–79%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 35 | 66% | 29% | 18/5 | 0.0106 | 0.0425 |
| GPT-4.1-nano: P3 vs P1 | 35 | 46% | 29% | 8/2 | 0.109 | 0.328 |
| GPT-4o-mini: P2 vs P1 | 37 | 0% | 3% | 0/1 | 1 | 1 |
| GPT-4o-mini: P3 vs P1 | 37 | 8% | 3% | 3/1 | 0.625 | 1 |

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
| P1 | followup | 0 | 0% (0%–24%) |
| P1 | followup | 1 | 21% (10%–38%) |
| P1 | followup | 2 | 16% (7%–33%) |
| P2 | followup | 0 | 15% (5%–36%) |
| P2 | followup | 1 | 32% (18%–51%) |
| P2 | followup | 2 | 46% (28%–65%) |
| P3 | followup | 0 | 26% (12%–49%) |
| P3 | followup | 1 | 31% (17%–50%) |
| P3 | followup | 2 | 22% (11%–41%) |
| P5 | followup | 0 | 66% (47%–80%) |
| P5 | followup | 1 | 77% (59%–88%) |
| P5 | followup | 2 | 77% (50%–92%) |
