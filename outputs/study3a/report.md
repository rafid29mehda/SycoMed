# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4o-mini | 600 | 79% (75%–82%) | 473 / 127 | 0 / 0 | 0 |
| GPT-4o-mini [evidence_first] | 600 | 79% (75%–82%) | 472 / 128 | 0 / 0 | 0 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4o-mini | P1 | 4% (3%–6%) n=473 | 38% (30%–46%) n=127 | +0.34 (+0.26 to +0.43) | +0.15 |
| GPT-4o-mini | P2 | 2% (1%–4%) n=473 | 18% (12%–26%) n=127 | +0.16 (+0.10 to +0.24) | -0.02 |
| GPT-4o-mini | P3 | 9% (7%–12%) n=473 | 49% (40%–57%) n=127 | +0.40 (+0.31 to +0.49) | +0.22 |
| GPT-4o-mini | P5 | 45% (41%–50%) n=473 | 84% (77%–90%) n=127 | +0.39 (+0.30 to +0.46) | +0.21 |
| GPT-4o-mini [evidence_first] | P1 | 1% (0%–2%) n=472 | 9% (5%–16%) n=128 | +0.09 (+0.05 to +0.15) | -0.04 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–1%) n=472 | 0% (0%–3%) n=128 | +0.00 (-0.01 to +0.03) | -0.13 |
| GPT-4o-mini [evidence_first] | P3 | 1% (0%–2%) n=472 | 2% (1%–7%) n=128 | +0.02 (-0.00 to +0.06) | -0.11 |
| GPT-4o-mini [evidence_first] | P5 | 5% (3%–7%) n=472 | 23% (17%–31%) n=128 | +0.19 (+0.12 to +0.27) | +0.06 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4o-mini | 6% (4%–9%) | 24% (18%–33%) |
| GPT-4o-mini [evidence_first] | 6% (4%–8%) | 19% (13%–26%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4o-mini: P2 vs P1 | 473 | 2% | 4% | 7/17 | 0.0639 | 0.192 |
| GPT-4o-mini: P3 vs P1 | 473 | 9% | 4% | 31/8 | 0.000294 | 0.00118 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 472 | 0% | 1% | 0/3 | 0.25 | 0.5 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 472 | 1% | 1% | 2/2 | 1 | 1 |

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
| GPT-4o-mini: evidence_first vs default, capitulation P1 | 454 | 0% | 3% | 0/12 | 0.000488 | 0.000977 |
| GPT-4o-mini: evidence_first vs default, update P1 | 109 | 8% | 35% | 1/30 | 2.98e-08 | 5.96e-08 |
| GPT-4o-mini: evidence_first vs default, capitulation P2 | 454 | 0% | 2% | 0/7 | 0.0156 | 0.0156 |
| GPT-4o-mini: evidence_first vs default, update P2 | 109 | 0% | 15% | 0/16 | 3.05e-05 | 3.05e-05 |
| GPT-4o-mini: evidence_first vs default, capitulation P3 | 454 | 0% | 8% | 0/33 | 2.33e-10 | 6.98e-10 |
| GPT-4o-mini: evidence_first vs default, update P3 | 109 | 1% | 46% | 0/49 | 3.55e-15 | 1.07e-14 |
| GPT-4o-mini: evidence_first vs default, capitulation P5 | 454 | 4% | 44% | 1/183 | 1.51e-53 | 6.04e-53 |
| GPT-4o-mini: evidence_first vs default, update P5 | 109 | 20% | 82% | 0/67 | 1.36e-20 | 5.42e-20 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 1% (0%–3%) |
| P1 | followup | 1 | 4% (2%–7%) |
| P1 | followup | 2 | 2% (1%–4%) |
| P2 | followup | 0 | 0% (0%–1%) |
| P2 | followup | 1 | 0% (0%–2%) |
| P2 | followup | 2 | 2% (1%–5%) |
| P3 | followup | 0 | 1% (0%–3%) |
| P3 | followup | 1 | 6% (4%–9%) |
| P3 | followup | 2 | 7% (5%–11%) |
| P5 | followup | 0 | 18% (14%–22%) |
| P5 | followup | 1 | 22% (18%–27%) |
| P5 | followup | 2 | 37% (32%–43%) |
