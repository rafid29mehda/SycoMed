# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4.1-nano | 600 | 78% (75%–82%) | 471 / 123 | 0 / 0 | 6 |
| GPT-4.1-nano [evidence_first] | 600 | 77% (74%–81%) | 464 / 130 | 0 / 0 | 6 |
| GPT-4o-mini | 600 | 79% (75%–82%) | 473 / 127 | 0 / 0 | 0 |
| GPT-4o-mini [evidence_first] | 600 | 79% (75%–82%) | 472 / 128 | 0 / 0 | 0 |
| GPT-5-mini | 598 | 89% (86%–91%) | 532 / 65 | 0 / 0 | 1 |
| Gemini 3.5 Flash-Lite | 86 | 92% (84%–96%) | 79 / 4 | 0 / 0 | 3 |

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
| GPT-4o-mini | P1 | 4% (3%–6%) n=473 | 38% (30%–46%) n=127 | +0.34 (+0.26 to +0.43) | +0.15 |
| GPT-4o-mini | P2 | 2% (1%–4%) n=473 | 18% (12%–26%) n=127 | +0.16 (+0.10 to +0.24) | -0.02 |
| GPT-4o-mini | P3 | 9% (7%–12%) n=473 | 49% (40%–57%) n=127 | +0.40 (+0.31 to +0.49) | +0.22 |
| GPT-4o-mini | P5 | 45% (41%–50%) n=473 | 84% (77%–90%) n=127 | +0.39 (+0.30 to +0.46) | +0.21 |
| GPT-4o-mini [evidence_first] | P1 | 1% (0%–2%) n=472 | 9% (5%–16%) n=128 | +0.09 (+0.05 to +0.15) | -0.04 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–1%) n=472 | 0% (0%–3%) n=128 | +0.00 (-0.01 to +0.03) | -0.13 |
| GPT-4o-mini [evidence_first] | P3 | 1% (0%–2%) n=472 | 2% (1%–7%) n=128 | +0.02 (-0.00 to +0.06) | -0.11 |
| GPT-4o-mini [evidence_first] | P5 | 5% (3%–7%) n=472 | 23% (17%–31%) n=128 | +0.19 (+0.12 to +0.27) | +0.06 |
| GPT-5-mini | P1 | 0% (0%–1%) n=532 | 23% (15%–35%) n=65 | +0.23 (+0.14 to +0.35) | +0.05 |
| GPT-5-mini | P2 | 0% (0%–1%) n=532 | 25% (16%–36%) n=65 | +0.24 (+0.16 to +0.36) | +0.06 |
| GPT-5-mini | P3 | 1% (0%–2%) n=532 | 48% (36%–60%) n=65 | +0.47 (+0.35 to +0.59) | +0.29 |
| GPT-5-mini | P5 | 6% (4%–8%) n=532 | 51% (39%–63%) n=65 | +0.45 (+0.33 to +0.57) | +0.27 |
| Gemini 3.5 Flash-Lite | P1 | 5% (2%–12%) n=79 | 50% (15%–85%) n=4 | +0.45 (+0.09 to +0.80) | +0.46 |
| Gemini 3.5 Flash-Lite | P2 | 16% (10%–26%) n=79 | 75% (30%–95%) n=4 | +0.59 (+0.13 to +0.80) | +0.60 |
| Gemini 3.5 Flash-Lite | P3 | 20% (13%–30%) n=79 | 50% (15%–85%) n=4 | +0.30 (-0.07 to +0.66) | +0.31 |
| Gemini 3.5 Flash-Lite | P5 | 68% (57%–77%) n=78 | 100% (51%–100%) n=4 | +0.32 (-0.18 to +0.43) | +0.33 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 2% (1%–4%) | 13% (8%–20%) |
| GPT-4.1-nano [evidence_first] | 2% (1%–3%) | 18% (13%–26%) |
| GPT-4o-mini | 6% (4%–9%) | 24% (18%–33%) |
| GPT-4o-mini [evidence_first] | 6% (4%–8%) | 19% (13%–26%) |
| GPT-5-mini | 0% (0%–1%) | 18% (11%–30%) |
| Gemini 3.5 Flash-Lite | 1% (0%–7%) | 0% (0%–49%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 471 | 69% | 18% | 246/6 | 9.49e-65 | 1.14e-63 |
| GPT-4.1-nano: P3 vs P1 | 471 | 48% | 18% | 153/14 | 1.01e-30 | 1.11e-29 |
| GPT-4.1-nano [evidence_first]: P2 vs P1 | 464 | 39% | 16% | 128/22 | 2.22e-19 | 2.22e-18 |
| GPT-4.1-nano [evidence_first]: P3 vs P1 | 464 | 23% | 16% | 67/33 | 0.000874 | 0.00699 |
| GPT-4o-mini: P2 vs P1 | 473 | 2% | 4% | 7/17 | 0.0639 | 0.32 |
| GPT-4o-mini: P3 vs P1 | 473 | 9% | 4% | 31/8 | 0.000294 | 0.00265 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 472 | 0% | 1% | 0/3 | 0.25 | 0.75 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 472 | 1% | 1% | 2/2 | 1 | 1 |
| GPT-5-mini: P2 vs P1 | 532 | 0% | 0% | 1/0 | 1 | 1 |
| GPT-5-mini: P3 vs P1 | 532 | 1% | 0% | 4/0 | 0.125 | 0.5 |
| Gemini 3.5 Flash-Lite: P2 vs P1 | 79 | 16% | 5% | 10/1 | 0.0117 | 0.0703 |
| Gemini 3.5 Flash-Lite: P3 vs P1 | 79 | 20% | 5% | 13/1 | 0.00183 | 0.0128 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

_No comparable data._

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

_No comparable data._

## H3: is discrimination explained by accuracy?

Spearman rank correlation of baseline accuracy and J across 6 model conditions: **+0.26** (descriptive; n = models).

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: evidence_first vs default, capitulation P1 | 436 | 14% | 17% | 29/42 | 0.154 | 0.154 |
| GPT-4.1-nano: evidence_first vs default, update P1 | 95 | 58% | 66% | 10/18 | 0.185 | 0.185 |
| GPT-4.1-nano: evidence_first vs default, capitulation P2 | 436 | 37% | 68% | 8/144 | 2.17e-33 | 1.52e-32 |
| GPT-4.1-nano: evidence_first vs default, update P2 | 95 | 77% | 95% | 1/18 | 7.63e-05 | 0.000305 |
| GPT-4.1-nano: evidence_first vs default, capitulation P3 | 436 | 21% | 45% | 22/128 | 2.22e-19 | 1.11e-18 |
| GPT-4.1-nano: evidence_first vs default, update P3 | 95 | 68% | 85% | 4/20 | 0.00154 | 0.00463 |
| GPT-4.1-nano: evidence_first vs default, capitulation P5 | 436 | 62% | 87% | 19/126 | 1.47e-20 | 8.81e-20 |
| GPT-4.1-nano: evidence_first vs default, update P5 | 95 | 85% | 97% | 2/13 | 0.00739 | 0.0148 |
| GPT-4o-mini: evidence_first vs default, capitulation P1 | 454 | 0% | 3% | 0/12 | 0.000488 | 0.00146 |
| GPT-4o-mini: evidence_first vs default, update P1 | 109 | 8% | 35% | 1/30 | 2.98e-08 | 1.79e-07 |
| GPT-4o-mini: evidence_first vs default, capitulation P2 | 454 | 0% | 2% | 0/7 | 0.0156 | 0.0312 |
| GPT-4o-mini: evidence_first vs default, update P2 | 109 | 0% | 15% | 0/16 | 3.05e-05 | 0.000153 |
| GPT-4o-mini: evidence_first vs default, capitulation P3 | 454 | 0% | 8% | 0/33 | 2.33e-10 | 9.31e-10 |
| GPT-4o-mini: evidence_first vs default, update P3 | 109 | 1% | 46% | 0/49 | 3.55e-15 | 2.49e-14 |
| GPT-4o-mini: evidence_first vs default, capitulation P5 | 454 | 4% | 44% | 1/183 | 1.51e-53 | 1.21e-52 |
| GPT-4o-mini: evidence_first vs default, update P5 | 109 | 20% | 82% | 0/67 | 1.36e-20 | 1.08e-19 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 3% (2%–4%) |
| P1 | followup | 1 | 12% (10%–14%) |
| P1 | followup | 2 | 8% (6%–10%) |
| P2 | followup | 0 | 12% (10%–14%) |
| P2 | followup | 1 | 22% (19%–25%) |
| P2 | followup | 2 | 29% (26%–32%) |
| P3 | followup | 0 | 13% (11%–15%) |
| P3 | followup | 1 | 20% (17%–23%) |
| P3 | followup | 2 | 15% (13%–18%) |
| P5 | followup | 0 | 41% (38%–44%) |
| P5 | followup | 1 | 37% (34%–41%) |
| P5 | followup | 2 | 47% (43%–50%) |
