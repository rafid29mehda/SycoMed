# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first] | 200 | 80% (73%–85%) | 159 / 40 | 159 / 159 | 1 |
| GPT-4.1-nano [resolve_first] | 200 | 80% (74%–85%) | 161 / 36 | 161 / 161 | 3 |
| GPT-4o-mini [evidence_first] | 200 | 81% (75%–86%) | 162 / 38 | 162 / 162 | 0 |
| GPT-4o-mini [resolve_first] | 200 | 79% (73%–84%) | 158 / 42 | 158 / 158 | 0 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first] | P1 | 16% (11%–23%) n=159 | 70% (55%–82%) n=40 | +0.54 (+0.37 to +0.67) | +0.37 |
| GPT-4.1-nano [evidence_first] | P2 | 35% (28%–43%) n=159 | 78% (62%–88%) n=40 | +0.42 (+0.25 to +0.55) | +0.25 |
| GPT-4.1-nano [evidence_first] | P3 | 26% (20%–33%) n=159 | 82% (68%–91%) n=40 | +0.57 (+0.41 to +0.67) | +0.40 |
| GPT-4.1-nano [evidence_first] | P5 | 61% (53%–68%) n=159 | 100% (91%–100%) n=40 | +0.39 (+0.28 to +0.47) | +0.22 |
| GPT-4.1-nano [resolve_first] | P1 | 17% (12%–23%) n=161 | 64% (48%–78%) n=36 | +0.47 (+0.30 to +0.62) | +0.41 |
| GPT-4.1-nano [resolve_first] | P2 | 66% (59%–73%) n=161 | 97% (86%–100%) n=36 | +0.31 (+0.17 to +0.39) | +0.24 |
| GPT-4.1-nano [resolve_first] | P3 | 50% (43%–58%) n=161 | 94% (82%–98%) n=36 | +0.44 (+0.29 to +0.53) | +0.38 |
| GPT-4.1-nano [resolve_first] | P5 | 78% (71%–84%) n=161 | 97% (86%–100%) n=36 | +0.19 (+0.06 to +0.26) | +0.12 |
| GPT-4o-mini [evidence_first] | P1 | 1% (0%–3%) n=162 | 8% (3%–21%) n=38 | +0.07 (+0.01 to +0.20) | +0.02 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–2%) n=162 | 0% (0%–9%) n=38 | +0.00 (-0.02 to +0.09) | -0.06 |
| GPT-4o-mini [evidence_first] | P3 | 0% (0%–2%) n=162 | 5% (1%–17%) n=38 | +0.05 (+0.01 to +0.17) | -0.00 |
| GPT-4o-mini [evidence_first] | P5 | 4% (2%–9%) n=162 | 29% (17%–45%) n=38 | +0.25 (+0.12 to +0.41) | +0.19 |
| GPT-4o-mini [resolve_first] | P1 | 0% (0%–2%) n=158 | 17% (8%–31%) n=42 | +0.17 (+0.08 to +0.31) | +0.08 |
| GPT-4o-mini [resolve_first] | P2 | 0% (0%–2%) n=158 | 12% (5%–25%) n=42 | +0.12 (+0.05 to +0.25) | +0.04 |
| GPT-4o-mini [resolve_first] | P3 | 2% (1%–5%) n=158 | 21% (12%–36%) n=42 | +0.20 (+0.09 to +0.34) | +0.11 |
| GPT-4o-mini [resolve_first] | P5 | 9% (6%–15%) n=158 | 57% (42%–71%) n=42 | +0.48 (+0.32 to +0.62) | +0.39 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano [evidence_first] | 1% (0%–3%) | 18% (9%–32%) |
| GPT-4.1-nano [resolve_first] | 2% (1%–5%) | 8% (3%–22%) |
| GPT-4o-mini [evidence_first] | 5% (3%–9%) | 11% (4%–24%) |
| GPT-4o-mini [resolve_first] | 1% (0%–4%) | 10% (4%–22%) |

## Capitulation, update and discrimination (preemptive)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first] | P1 | 7% (4%–12%) n=159 | 48% (33%–63%) n=40 | +0.41 (+0.25 to +0.56) | n/a |
| GPT-4.1-nano [evidence_first] | P2 | 13% (9%–19%) n=159 | 52% (37%–67%) n=40 | +0.39 (+0.23 to +0.55) | n/a |
| GPT-4.1-nano [evidence_first] | P3 | 11% (7%–16%) n=159 | 62% (47%–76%) n=40 | +0.52 (+0.35 to +0.66) | n/a |
| GPT-4.1-nano [evidence_first] | P5 | 11% (7%–16%) n=159 | 48% (33%–63%) n=40 | +0.37 (+0.21 to +0.52) | n/a |
| GPT-4.1-nano [resolve_first] | P1 | 7% (4%–13%) n=161 | 42% (27%–58%) n=36 | +0.34 (+0.19 to +0.51) | n/a |
| GPT-4.1-nano [resolve_first] | P2 | 16% (11%–22%) n=161 | 44% (30%–60%) n=36 | +0.29 (+0.13 to +0.46) | n/a |
| GPT-4.1-nano [resolve_first] | P3 | 19% (14%–26%) n=161 | 56% (40%–70%) n=36 | +0.36 (+0.19 to +0.52) | n/a |
| GPT-4.1-nano [resolve_first] | P5 | 22% (17%–29%) n=161 | 56% (40%–70%) n=36 | +0.33 (+0.16 to +0.49) | n/a |
| GPT-4o-mini [evidence_first] | P1 | 3% (1%–7%) n=162 | 32% (19%–47%) n=38 | +0.28 (+0.15 to +0.44) | n/a |
| GPT-4o-mini [evidence_first] | P2 | 6% (3%–11%) n=162 | 29% (17%–45%) n=38 | +0.23 (+0.10 to +0.39) | n/a |
| GPT-4o-mini [evidence_first] | P3 | 6% (3%–11%) n=162 | 34% (21%–50%) n=38 | +0.28 (+0.14 to +0.44) | n/a |
| GPT-4o-mini [evidence_first] | P5 | 7% (4%–12%) n=162 | 32% (19%–47%) n=38 | +0.25 (+0.11 to +0.41) | n/a |
| GPT-4o-mini [resolve_first] | P1 | 2% (1%–5%) n=158 | 29% (17%–44%) n=42 | +0.27 (+0.15 to +0.42) | n/a |
| GPT-4o-mini [resolve_first] | P2 | 4% (2%–8%) n=158 | 24% (13%–39%) n=42 | +0.20 (+0.09 to +0.35) | n/a |
| GPT-4o-mini [resolve_first] | P3 | 8% (4%–13%) n=158 | 38% (25%–53%) n=42 | +0.31 (+0.16 to +0.46) | n/a |
| GPT-4o-mini [resolve_first] | P5 | 6% (3%–10%) n=158 | 31% (19%–46%) n=42 | +0.25 (+0.12 to +0.41) | n/a |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

## Capitulation, update and discrimination (prefilled)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first] | P1 | 12% (8%–18%) n=159 | 96% (91%–98%) n=159 | +0.84 (+0.76 to +0.88) | +0.02 |
| GPT-4.1-nano [evidence_first] | P2 | 26% (20%–33%) n=159 | 97% (93%–99%) n=159 | +0.71 (+0.63 to +0.77) | -0.11 |
| GPT-4.1-nano [evidence_first] | P3 | 20% (15%–27%) n=159 | 96% (92%–98%) n=159 | +0.76 (+0.68 to +0.82) | -0.06 |
| GPT-4.1-nano [evidence_first] | P5 | 45% (38%–53%) n=159 | 96% (91%–98%) n=159 | +0.50 (+0.41 to +0.58) | -0.31 |
| GPT-4.1-nano [resolve_first] | P1 | 10% (6%–16%) n=161 | 96% (92%–98%) n=161 | +0.86 (+0.79 to +0.91) | +0.05 |
| GPT-4.1-nano [resolve_first] | P2 | 40% (33%–48%) n=161 | 98% (95%–99%) n=161 | +0.58 (+0.49 to +0.65) | -0.24 |
| GPT-4.1-nano [resolve_first] | P3 | 30% (24%–38%) n=161 | 99% (97%–100%) n=161 | +0.69 (+0.61 to +0.76) | -0.12 |
| GPT-4.1-nano [resolve_first] | P5 | 61% (53%–68%) n=161 | 99% (97%–100%) n=161 | +0.39 (+0.31 to +0.46) | -0.43 |
| GPT-4o-mini [evidence_first] | P1 | 2% (1%–6%) n=162 | 87% (81%–91%) n=162 | +0.85 (+0.77 to +0.89) | -0.01 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–2%) n=162 | 76% (69%–82%) n=162 | +0.76 (+0.68 to +0.82) | -0.10 |
| GPT-4o-mini [evidence_first] | P3 | 1% (0%–3%) n=162 | 78% (71%–84%) n=162 | +0.78 (+0.70 to +0.83) | -0.08 |
| GPT-4o-mini [evidence_first] | P5 | 6% (3%–10%) n=162 | 94% (89%–97%) n=162 | +0.88 (+0.82 to +0.92) | +0.02 |
| GPT-4o-mini [resolve_first] | P1 | 1% (0%–4%) n=158 | 94% (89%–97%) n=158 | +0.92 (+0.87 to +0.95) | +0.06 |
| GPT-4o-mini [resolve_first] | P2 | 1% (0%–4%) n=158 | 91% (85%–94%) n=158 | +0.89 (+0.83 to +0.93) | +0.03 |
| GPT-4o-mini [resolve_first] | P3 | 1% (0%–4%) n=158 | 91% (85%–94%) n=158 | +0.89 (+0.83 to +0.93) | +0.03 |
| GPT-4o-mini [resolve_first] | P5 | 7% (4%–12%) n=158 | 97% (94%–99%) n=158 | +0.91 (+0.84 to +0.94) | +0.04 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano [evidence_first] | 3% (1%–6%) | 84% (78%–89%) |
| GPT-4.1-nano [resolve_first] | 2% (1%–5%) | 83% (77%–88%) |
| GPT-4o-mini [evidence_first] | 3% (1%–7%) | 89% (83%–93%) |
| GPT-4o-mini [resolve_first] | 1% (0%–4%) | 87% (81%–92%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first]: P2 vs P1 | 159 | 35% | 16% | 40/10 | 2.39e-05 | 0.000143 |
| GPT-4.1-nano [evidence_first]: P3 vs P1 | 159 | 26% | 16% | 26/11 | 0.0201 | 0.1 |
| GPT-4.1-nano [resolve_first]: P2 vs P1 | 161 | 66% | 17% | 82/2 | 3.69e-22 | 2.95e-21 |
| GPT-4.1-nano [resolve_first]: P3 vs P1 | 161 | 50% | 17% | 59/5 | 9e-13 | 6.3e-12 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 162 | 0% | 1% | 0/1 | 1 | 1 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 162 | 0% | 1% | 0/1 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P2 vs P1 | 158 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P3 vs P1 | 158 | 2% | 0% | 3/0 | 0.25 | 1 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first]: P1 follow-up vs preemptive | 159 | 16% | 7% | 21/6 | 0.00592 | 0.0474 |
| GPT-4.1-nano [evidence_first]: P2 follow-up vs preemptive | 159 | 35% | 13% | 42/7 | 3.62e-07 | 4.35e-06 |
| GPT-4.1-nano [evidence_first]: P3 follow-up vs preemptive | 159 | 26% | 11% | 29/5 | 3.86e-05 | 0.000424 |
| GPT-4.1-nano [evidence_first]: P5 follow-up vs preemptive | 159 | 61% | 11% | 81/1 | 3.43e-23 | 5.15e-22 |
| GPT-4.1-nano [resolve_first]: P1 follow-up vs preemptive | 161 | 17% | 7% | 23/8 | 0.0107 | 0.0747 |
| GPT-4.1-nano [resolve_first]: P2 follow-up vs preemptive | 161 | 66% | 16% | 86/4 | 4.32e-21 | 6.05e-20 |
| GPT-4.1-nano [resolve_first]: P3 follow-up vs preemptive | 161 | 50% | 19% | 58/8 | 1.8e-10 | 2.33e-09 |
| GPT-4.1-nano [resolve_first]: P5 follow-up vs preemptive | 161 | 78% | 22% | 93/3 | 3.72e-24 | 5.96e-23 |
| GPT-4o-mini [evidence_first]: P1 follow-up vs preemptive | 162 | 1% | 3% | 1/5 | 0.219 | 0.656 |
| GPT-4o-mini [evidence_first]: P2 follow-up vs preemptive | 162 | 0% | 6% | 0/10 | 0.00195 | 0.0195 |
| GPT-4o-mini [evidence_first]: P3 follow-up vs preemptive | 162 | 0% | 6% | 0/10 | 0.00195 | 0.0195 |
| GPT-4o-mini [evidence_first]: P5 follow-up vs preemptive | 162 | 4% | 7% | 5/9 | 0.424 | 0.656 |
| GPT-4o-mini [resolve_first]: P1 follow-up vs preemptive | 158 | 0% | 2% | 0/3 | 0.25 | 0.656 |
| GPT-4o-mini [resolve_first]: P2 follow-up vs preemptive | 158 | 0% | 4% | 0/6 | 0.0312 | 0.156 |
| GPT-4o-mini [resolve_first]: P3 follow-up vs preemptive | 158 | 2% | 8% | 2/11 | 0.0225 | 0.135 |
| GPT-4o-mini [resolve_first]: P5 follow-up vs preemptive | 158 | 9% | 6% | 8/2 | 0.109 | 0.438 |

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano [evidence_first]: P1 update vs capitulation | 159 | 96% | 12% | 135/2 | 1.09e-37 | 9.77e-37 |
| GPT-4.1-nano [evidence_first]: P2 update vs capitulation | 159 | 97% | 26% | 115/2 | 8.31e-32 | 3.32e-31 |
| GPT-4.1-nano [evidence_first]: P3 update vs capitulation | 159 | 96% | 20% | 122/1 | 2.33e-35 | 1.4e-34 |
| GPT-4.1-nano [evidence_first]: P5 update vs capitulation | 159 | 96% | 45% | 84/4 | 1.58e-20 | 3.16e-20 |
| GPT-4.1-nano [resolve_first]: P1 update vs capitulation | 161 | 96% | 10% | 140/1 | 1.02e-40 | 1.22e-39 |
| GPT-4.1-nano [resolve_first]: P2 update vs capitulation | 161 | 98% | 40% | 93/0 | 2.02e-28 | 6.06e-28 |
| GPT-4.1-nano [resolve_first]: P3 update vs capitulation | 161 | 99% | 30% | 111/0 | 7.7e-34 | 3.85e-33 |
| GPT-4.1-nano [resolve_first]: P5 update vs capitulation | 161 | 99% | 61% | 63/1 | 7.05e-18 | 7.05e-18 |
| GPT-4o-mini [evidence_first]: P1 update vs capitulation | 162 | 87% | 2% | 140/3 | 8.74e-38 | 8.74e-37 |
| GPT-4o-mini [evidence_first]: P2 update vs capitulation | 162 | 76% | 0% | 123/0 | 1.88e-37 | 1.5e-36 |
| GPT-4o-mini [evidence_first]: P3 update vs capitulation | 162 | 78% | 1% | 127/1 | 7.58e-37 | 5.31e-36 |
| GPT-4o-mini [evidence_first]: P5 update vs capitulation | 162 | 94% | 6% | 146/3 | 1.55e-39 | 1.7e-38 |
| GPT-4o-mini [resolve_first]: P1 update vs capitulation | 158 | 94% | 1% | 148/2 | 1.59e-41 | 2.22e-40 |
| GPT-4o-mini [resolve_first]: P2 update vs capitulation | 158 | 91% | 1% | 141/0 | 7.17e-43 | 1.15e-41 |
| GPT-4o-mini [resolve_first]: P3 update vs capitulation | 158 | 91% | 1% | 142/1 | 2.58e-41 | 3.36e-40 |
| GPT-4o-mini [resolve_first]: P5 update vs capitulation | 158 | 97% | 7% | 144/1 | 6.55e-42 | 9.82e-41 |

## H3: is discrimination explained by accuracy?

Spearman rank correlation of baseline accuracy and J across 4 model conditions: **-0.40** (descriptive; n = models).

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

_No comparable data._

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 2% (1%–5%) |
| P1 | followup | 1 | 10% (6%–15%) |
| P1 | followup | 2 | 12% (9%–17%) |
| P1 | preemptive | 0 | 9% (6%–14%) |
| P1 | preemptive | 1 | 3% (1%–6%) |
| P1 | preemptive | 2 | 3% (1%–6%) |
| P1 | prefilled | 0 | 4% (2%–7%) |
| P1 | prefilled | 1 | 9% (6%–14%) |
| P1 | prefilled | 2 | 7% (4%–11%) |
| P2 | followup | 0 | 17% (13%–23%) |
| P2 | followup | 1 | 26% (20%–32%) |
| P2 | followup | 2 | 33% (27%–39%) |
| P2 | preemptive | 0 | 7% (4%–11%) |
| P2 | preemptive | 1 | 12% (8%–18%) |
| P2 | preemptive | 2 | 10% (7%–15%) |
| P2 | prefilled | 0 | 12% (8%–17%) |
| P2 | prefilled | 1 | 16% (12%–22%) |
| P2 | prefilled | 2 | 23% (18%–29%) |
| P3 | followup | 0 | 18% (13%–24%) |
| P3 | followup | 1 | 23% (18%–29%) |
| P3 | followup | 2 | 17% (13%–23%) |
| P3 | preemptive | 0 | 6% (4%–10%) |
| P3 | preemptive | 1 | 13% (9%–18%) |
| P3 | preemptive | 2 | 14% (10%–20%) |
| P3 | prefilled | 0 | 19% (14%–24%) |
| P3 | prefilled | 1 | 13% (9%–18%) |
| P3 | prefilled | 2 | 8% (5%–12%) |
| P5 | followup | 0 | 40% (33%–47%) |
| P5 | followup | 1 | 33% (28%–39%) |
| P5 | followup | 2 | 46% (38%–53%) |
| P5 | preemptive | 0 | 19% (14%–25%) |
| P5 | preemptive | 1 | 4% (2%–7%) |
| P5 | preemptive | 2 | 12% (8%–17%) |
| P5 | prefilled | 0 | 37% (31%–43%) |
| P5 | prefilled | 1 | 21% (16%–28%) |
| P5 | prefilled | 2 | 28% (23%–34%) |
