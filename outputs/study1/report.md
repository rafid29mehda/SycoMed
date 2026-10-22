# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4.1-nano | 200 | 81% (75%–86%) | 162 / 37 | 162 / 162 | 1 |
| GPT-4o-mini | 200 | 78% (71%–83%) | 155 / 45 | 155 / 155 | 0 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation |
|---|---|---|---|---|
| GPT-4.1-nano | P1 | 16% (11%–22%) n=162 | 70% (54%–83%) n=37 | +0.54 (+0.37 to +0.67) |
| GPT-4.1-nano | P2 | 67% (59%–73%) n=162 | 97% (86%–100%) n=37 | +0.31 (+0.18 to +0.39) |
| GPT-4.1-nano | P3 | 49% (42%–57%) n=162 | 92% (79%–97%) n=37 | +0.43 (+0.27 to +0.52) |
| GPT-4.1-nano | P5 | 88% (82%–92%) n=162 | 95% (82%–99%) n=37 | +0.07 (-0.06 to +0.14) |
| GPT-4o-mini | P1 | 1% (0%–5%) n=155 | 42% (29%–57%) n=45 | +0.41 (+0.27 to +0.55) |
| GPT-4o-mini | P2 | 2% (1%–6%) n=155 | 16% (8%–29%) n=45 | +0.14 (+0.05 to +0.27) |
| GPT-4o-mini | P3 | 8% (5%–14%) n=155 | 53% (39%–67%) n=45 | +0.45 (+0.30 to +0.59) |
| GPT-4o-mini | P5 | 40% (33%–48%) n=155 | 91% (79%–96%) n=45 | +0.51 (+0.37 to +0.60) |

Plain-recheck self-correction (P0, valid arm):

| model | corrected on recheck |
|---|---|
| GPT-4.1-nano | 5% (1%–18%) |
| GPT-4o-mini | 18% (9%–31%) |

## Capitulation, update and discrimination (preemptive)

| model | pressure | capitulation | update | J = update − capitulation |
|---|---|---|---|---|
| GPT-4.1-nano | P1 | 10% (6%–15%) n=162 | 46% (31%–62%) n=37 | +0.36 (+0.20 to +0.52) |
| GPT-4.1-nano | P2 | 26% (20%–33%) n=162 | 65% (49%–78%) n=37 | +0.39 (+0.21 to +0.54) |
| GPT-4.1-nano | P3 | 21% (15%–28%) n=162 | 57% (41%–71%) n=37 | +0.36 (+0.18 to +0.51) |
| GPT-4.1-nano | P5 | 28% (22%–36%) n=162 | 54% (38%–69%) n=37 | +0.26 (+0.08 to +0.42) |
| GPT-4o-mini | P1 | 2% (1%–6%) n=155 | 31% (20%–46%) n=45 | +0.29 (+0.17 to +0.44) |
| GPT-4o-mini | P2 | 6% (4%–11%) n=155 | 47% (33%–61%) n=45 | +0.40 (+0.26 to +0.55) |
| GPT-4o-mini | P3 | 6% (3%–11%) n=155 | 51% (37%–65%) n=45 | +0.45 (+0.30 to +0.60) |
| GPT-4o-mini | P5 | 8% (4%–13%) n=155 | 33% (21%–48%) n=45 | +0.26 (+0.12 to +0.41) |

## Capitulation, update and discrimination (prefilled)

| model | pressure | capitulation | update | J = update − capitulation |
|---|---|---|---|---|
| GPT-4.1-nano | P1 | 17% (12%–24%) n=162 | 94% (90%–97%) n=162 | +0.77 (+0.69 to +0.83) |
| GPT-4.1-nano | P2 | 45% (38%–53%) n=162 | 98% (94%–99%) n=162 | +0.52 (+0.44 to +0.60) |
| GPT-4.1-nano | P3 | 30% (24%–38%) n=162 | 97% (93%–99%) n=162 | +0.67 (+0.58 to +0.73) |
| GPT-4.1-nano | P5 | 70% (62%–76%) n=162 | 98% (95%–99%) n=162 | +0.28 (+0.21 to +0.36) |
| GPT-4o-mini | P1 | 4% (2%–8%) n=155 | 94% (89%–97%) n=155 | +0.90 (+0.84 to +0.94) |
| GPT-4o-mini | P2 | 3% (1%–6%) n=155 | 97% (94%–99%) n=155 | +0.95 (+0.89 to +0.97) |
| GPT-4o-mini | P3 | 3% (1%–6%) n=155 | 99% (95%–100%) n=155 | +0.96 (+0.91 to +0.98) |
| GPT-4o-mini | P5 | 25% (18%–32%) n=155 | 100% (98%–100%) n=155 | +0.75 (+0.68 to +0.82) |

Plain-recheck self-correction (P0, valid arm):

| model | corrected on recheck |
|---|---|
| GPT-4.1-nano | 78% (71%–83%) |
| GPT-4o-mini | 93% (88%–96%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 162 | 67% | 16% | 85/3 | 7.34e-22 | 2.94e-21 |
| GPT-4.1-nano: P3 vs P1 | 162 | 49% | 16% | 58/4 | 2.59e-13 | 7.78e-13 |
| GPT-4o-mini: P2 vs P1 | 155 | 2% | 1% | 3/2 | 1 | 1 |
| GPT-4o-mini: P3 vs P1 | 155 | 8% | 1% | 12/1 | 0.00342 | 0.00684 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 follow-up vs preemptive | 162 | 16% | 10% | 21/11 | 0.11 | 0.331 |
| GPT-4.1-nano: P2 follow-up vs preemptive | 162 | 67% | 26% | 71/5 | 5.25e-16 | 3.67e-15 |
| GPT-4.1-nano: P3 follow-up vs preemptive | 162 | 49% | 21% | 56/10 | 6.9e-09 | 3.45e-08 |
| GPT-4.1-nano: P5 follow-up vs preemptive | 162 | 88% | 28% | 100/4 | 4.72e-25 | 3.78e-24 |
| GPT-4o-mini: P1 follow-up vs preemptive | 155 | 1% | 2% | 2/3 | 1 | 1 |
| GPT-4o-mini: P2 follow-up vs preemptive | 155 | 2% | 6% | 2/9 | 0.0654 | 0.262 |
| GPT-4o-mini: P3 follow-up vs preemptive | 155 | 8% | 6% | 12/8 | 0.503 | 1 |
| GPT-4o-mini: P5 follow-up vs preemptive | 155 | 40% | 8% | 52/2 | 1.65e-13 | 9.9e-13 |

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 update vs capitulation | 162 | 94% | 17% | 131/6 | 9.88e-32 | 3.95e-31 |
| GPT-4.1-nano: P2 update vs capitulation | 162 | 98% | 45% | 86/1 | 1.14e-24 | 2.27e-24 |
| GPT-4.1-nano: P3 update vs capitulation | 162 | 97% | 30% | 112/4 | 1.79e-28 | 5.36e-28 |
| GPT-4.1-nano: P5 update vs capitulation | 162 | 98% | 70% | 48/2 | 2.27e-12 | 2.27e-12 |
| GPT-4o-mini: P1 update vs capitulation | 155 | 94% | 4% | 140/0 | 1.43e-42 | 8.61e-42 |
| GPT-4o-mini: P2 update vs capitulation | 155 | 97% | 3% | 147/0 | 1.12e-44 | 7.85e-44 |
| GPT-4o-mini: P3 update vs capitulation | 155 | 99% | 3% | 149/0 | 2.8e-45 | 2.24e-44 |
| GPT-4o-mini: P5 update vs capitulation | 155 | 100% | 25% | 117/0 | 1.2e-35 | 6.02e-35 |

## H3: is discrimination explained by accuracy?

_Needs at least 3 models._

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

_No comparable data._

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 2% (1%–8%) |
| P1 | followup | 1 | 9% (5%–16%) |
| P1 | followup | 2 | 13% (8%–20%) |
| P1 | preemptive | 0 | 7% (3%–14%) |
| P1 | preemptive | 1 | 9% (5%–15%) |
| P1 | preemptive | 2 | 2% (1%–7%) |
| P1 | prefilled | 0 | 3% (1%–8%) |
| P1 | prefilled | 1 | 19% (12%–29%) |
| P1 | prefilled | 2 | 12% (7%–19%) |
| P2 | followup | 0 | 21% (14%–30%) |
| P2 | followup | 1 | 36% (28%–46%) |
| P2 | followup | 2 | 46% (37%–56%) |
| P2 | preemptive | 0 | 7% (4%–14%) |
| P2 | preemptive | 1 | 29% (20%–39%) |
| P2 | preemptive | 2 | 16% (11%–24%) |
| P2 | prefilled | 0 | 14% (9%–22%) |
| P2 | prefilled | 1 | 21% (15%–30%) |
| P2 | prefilled | 2 | 39% (30%–49%) |
| P3 | followup | 0 | 21% (14%–31%) |
| P3 | followup | 1 | 38% (30%–47%) |
| P3 | followup | 2 | 27% (19%–36%) |
| P3 | preemptive | 0 | 11% (7%–18%) |
| P3 | preemptive | 1 | 14% (8%–23%) |
| P3 | preemptive | 2 | 16% (10%–24%) |
| P3 | prefilled | 0 | 20% (13%–28%) |
| P3 | prefilled | 1 | 22% (15%–31%) |
| P3 | prefilled | 2 | 9% (5%–16%) |
| P5 | followup | 0 | 59% (49%–68%) |
| P5 | followup | 1 | 63% (54%–70%) |
| P5 | followup | 2 | 73% (63%–82%) |
| P5 | preemptive | 0 | 30% (22%–39%) |
| P5 | preemptive | 1 | 3% (1%–8%) |
| P5 | preemptive | 2 | 24% (17%–33%) |
| P5 | prefilled | 0 | 53% (44%–62%) |
| P5 | prefilled | 1 | 29% (21%–39%) |
| P5 | prefilled | 2 | 56% (47%–65%) |
