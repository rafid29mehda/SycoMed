# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4.1-nano | 600 | 78% (75%–82%) | 471 / 123 | 0 / 0 | 6 |
| GPT-4.1-nano [evidence_first] | 600 | 77% (74%–81%) | 464 / 130 | 0 / 0 | 6 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 18% (15%–22%) n=471 | 72% (63%–79%) n=123 | +0.53 (+0.44 to +0.61) | +0.43 |
| GPT-4.1-nano | P2 | 69% (65%–73%) n=471 | 95% (90%–98%) n=123 | +0.26 (+0.19 to +0.31) | +0.15 |
| GPT-4.1-nano | P3 | 48% (43%–52%) n=471 | 87% (80%–92%) n=123 | +0.39 (+0.31 to +0.46) | +0.29 |
| GPT-4.1-nano | P5 | 87% (84%–90%) n=471 | 98% (93%–99%) n=123 | +0.10 (+0.05 to +0.14) | -0.00 |
| GPT-4.1-nano [evidence_first] | P1 | 16% (13%–20%) n=464 | 58% (49%–66%) n=130 | +0.42 (+0.32 to +0.50) | +0.25 |
| GPT-4.1-nano [evidence_first] | P2 | 39% (35%–44%) n=464 | 81% (73%–87%) n=130 | +0.42 (+0.33 to +0.49) | +0.25 |
| GPT-4.1-nano [evidence_first] | P3 | 23% (20%–28%) n=464 | 72% (64%–79%) n=130 | +0.49 (+0.40 to +0.57) | +0.32 |
| GPT-4.1-nano [evidence_first] | P5 | 64% (60%–68%) n=464 | 88% (82%–93%) n=130 | +0.24 (+0.16 to +0.31) | +0.07 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 2% (1%–4%) | 13% (8%–20%) |
| GPT-4.1-nano [evidence_first] | 2% (1%–3%) | 18% (13%–26%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 471 | 69% | 18% | 246/6 | 9.49e-65 | 3.79e-64 |
| GPT-4.1-nano: P3 vs P1 | 471 | 48% | 18% | 153/14 | 1.01e-30 | 3.03e-30 |
| GPT-4.1-nano [evidence_first]: P2 vs P1 | 464 | 39% | 16% | 128/22 | 2.22e-19 | 4.44e-19 |
| GPT-4.1-nano [evidence_first]: P3 vs P1 | 464 | 23% | 16% | 67/33 | 0.000874 | 0.000874 |

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

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: evidence_first vs default, capitulation P1 | 436 | 14% | 17% | 29/42 | 0.154 | 0.154 |
| GPT-4.1-nano: evidence_first vs default, update P1 | 95 | 58% | 66% | 10/18 | 0.185 | 0.185 |
| GPT-4.1-nano: evidence_first vs default, capitulation P2 | 436 | 37% | 68% | 8/144 | 2.17e-33 | 8.69e-33 |
| GPT-4.1-nano: evidence_first vs default, update P2 | 95 | 77% | 95% | 1/18 | 7.63e-05 | 0.000305 |
| GPT-4.1-nano: evidence_first vs default, capitulation P3 | 436 | 21% | 45% | 22/128 | 2.22e-19 | 4.44e-19 |
| GPT-4.1-nano: evidence_first vs default, update P3 | 95 | 68% | 85% | 4/20 | 0.00154 | 0.00463 |
| GPT-4.1-nano: evidence_first vs default, capitulation P5 | 436 | 62% | 87% | 19/126 | 1.47e-20 | 4.4e-20 |
| GPT-4.1-nano: evidence_first vs default, update P5 | 95 | 85% | 97% | 2/13 | 0.00739 | 0.0148 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 7% (4%–10%) |
| P1 | followup | 1 | 26% (21%–31%) |
| P1 | followup | 2 | 19% (15%–23%) |
| P2 | followup | 0 | 30% (25%–35%) |
| P2 | followup | 1 | 57% (51%–62%) |
| P2 | followup | 2 | 73% (68%–77%) |
| P3 | followup | 0 | 30% (25%–35%) |
| P3 | followup | 1 | 45% (39%–50%) |
| P3 | followup | 2 | 32% (27%–38%) |
| P5 | followup | 0 | 80% (75%–83%) |
| P5 | followup | 1 | 67% (62%–72%) |
| P5 | followup | 2 | 82% (77%–86%) |
