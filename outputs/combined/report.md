# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4.1-nano | 200 | 81% (75%–86%) | 162 / 37 | 162 / 162 | 1 |
| GPT-4.1-nano [evidence_first] | 200 | 80% (73%–85%) | 159 / 40 | 159 / 159 | 1 |
| GPT-4.1-nano [resolve_first] | 200 | 80% (74%–85%) | 161 / 36 | 161 / 161 | 3 |
| GPT-4o-mini | 200 | 78% (71%–83%) | 155 / 45 | 155 / 155 | 0 |
| GPT-4o-mini [evidence_first] | 200 | 81% (75%–86%) | 162 / 38 | 162 / 162 | 0 |
| GPT-4o-mini [resolve_first] | 200 | 79% (73%–84%) | 158 / 42 | 158 / 158 | 0 |
| GPT-5-mini | 200 | 90% (85%–93%) | 180 / 20 | 180 / 180 | 0 |

_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 16% (11%–22%) n=162 | 70% (54%–83%) n=37 | +0.54 (+0.37 to +0.67) | +0.50 |
| GPT-4.1-nano | P2 | 67% (59%–73%) n=162 | 97% (86%–100%) n=37 | +0.31 (+0.18 to +0.39) | +0.26 |
| GPT-4.1-nano | P3 | 49% (42%–57%) n=162 | 92% (79%–97%) n=37 | +0.43 (+0.27 to +0.52) | +0.38 |
| GPT-4.1-nano | P5 | 88% (82%–92%) n=162 | 95% (82%–99%) n=37 | +0.07 (-0.06 to +0.14) | +0.03 |
| GPT-4.1-nano [evidence_first] | P1 | 16% (11%–23%) n=159 | 70% (55%–82%) n=40 | +0.54 (+0.37 to +0.67) | +0.37 |
| GPT-4.1-nano [evidence_first] | P2 | 35% (28%–43%) n=159 | 78% (62%–88%) n=40 | +0.42 (+0.25 to +0.55) | +0.25 |
| GPT-4.1-nano [evidence_first] | P3 | 26% (20%–33%) n=159 | 82% (68%–91%) n=40 | +0.57 (+0.41 to +0.67) | +0.40 |
| GPT-4.1-nano [evidence_first] | P5 | 61% (53%–68%) n=159 | 100% (91%–100%) n=40 | +0.39 (+0.28 to +0.47) | +0.22 |
| GPT-4.1-nano [resolve_first] | P1 | 17% (12%–23%) n=161 | 64% (48%–78%) n=36 | +0.47 (+0.30 to +0.62) | +0.41 |
| GPT-4.1-nano [resolve_first] | P2 | 66% (59%–73%) n=161 | 97% (86%–100%) n=36 | +0.31 (+0.17 to +0.39) | +0.24 |
| GPT-4.1-nano [resolve_first] | P3 | 50% (43%–58%) n=161 | 94% (82%–98%) n=36 | +0.44 (+0.29 to +0.53) | +0.38 |
| GPT-4.1-nano [resolve_first] | P5 | 78% (71%–84%) n=161 | 97% (86%–100%) n=36 | +0.19 (+0.06 to +0.26) | +0.12 |
| GPT-4o-mini | P1 | 1% (0%–5%) n=155 | 42% (29%–57%) n=45 | +0.41 (+0.27 to +0.55) | +0.30 |
| GPT-4o-mini | P2 | 2% (1%–6%) n=155 | 16% (8%–29%) n=45 | +0.14 (+0.05 to +0.27) | +0.02 |
| GPT-4o-mini | P3 | 8% (5%–14%) n=155 | 53% (39%–67%) n=45 | +0.45 (+0.30 to +0.59) | +0.34 |
| GPT-4o-mini | P5 | 40% (33%–48%) n=155 | 91% (79%–96%) n=45 | +0.51 (+0.37 to +0.60) | +0.40 |
| GPT-4o-mini [evidence_first] | P1 | 1% (0%–3%) n=162 | 8% (3%–21%) n=38 | +0.07 (+0.01 to +0.20) | +0.02 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–2%) n=162 | 0% (0%–9%) n=38 | +0.00 (-0.02 to +0.09) | -0.06 |
| GPT-4o-mini [evidence_first] | P3 | 0% (0%–2%) n=162 | 5% (1%–17%) n=38 | +0.05 (+0.01 to +0.17) | -0.00 |
| GPT-4o-mini [evidence_first] | P5 | 4% (2%–9%) n=162 | 29% (17%–45%) n=38 | +0.25 (+0.12 to +0.41) | +0.19 |
| GPT-4o-mini [resolve_first] | P1 | 0% (0%–2%) n=158 | 17% (8%–31%) n=42 | +0.17 (+0.08 to +0.31) | +0.08 |
| GPT-4o-mini [resolve_first] | P2 | 0% (0%–2%) n=158 | 12% (5%–25%) n=42 | +0.12 (+0.05 to +0.25) | +0.04 |
| GPT-4o-mini [resolve_first] | P3 | 2% (1%–5%) n=158 | 21% (12%–36%) n=42 | +0.20 (+0.09 to +0.34) | +0.11 |
| GPT-4o-mini [resolve_first] | P5 | 9% (6%–15%) n=158 | 57% (42%–71%) n=42 | +0.48 (+0.32 to +0.62) | +0.39 |
| GPT-5-mini | P1 | 0% (0%–2%) n=180 | 20% (8%–42%) n=20 | +0.20 (+0.08 to +0.42) | +0.06 |
| GPT-5-mini | P2 | 1% (0%–3%) n=180 | 10% (3%–30%) n=20 | +0.09 (+0.02 to +0.30) | -0.05 |
| GPT-5-mini | P3 | 2% (1%–5%) n=180 | 20% (8%–42%) n=20 | +0.18 (+0.06 to +0.40) | +0.04 |
| GPT-5-mini | P5 | 4% (2%–9%) n=180 | 45% (26%–66%) n=20 | +0.41 (+0.21 to +0.61) | +0.26 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 1% (0%–4%) | 5% (1%–18%) |
| GPT-4.1-nano [evidence_first] | 1% (0%–3%) | 18% (9%–32%) |
| GPT-4.1-nano [resolve_first] | 2% (1%–5%) | 8% (3%–22%) |
| GPT-4o-mini | 6% (4%–11%) | 18% (9%–31%) |
| GPT-4o-mini [evidence_first] | 5% (3%–9%) | 11% (4%–24%) |
| GPT-4o-mini [resolve_first] | 1% (0%–4%) | 10% (4%–22%) |
| GPT-5-mini | 1% (0%–3%) | 15% (5%–36%) |

## Capitulation, update and discrimination (preemptive)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 10% (6%–15%) n=162 | 46% (31%–62%) n=37 | +0.36 (+0.20 to +0.52) | n/a |
| GPT-4.1-nano | P2 | 26% (20%–33%) n=162 | 65% (49%–78%) n=37 | +0.39 (+0.21 to +0.54) | n/a |
| GPT-4.1-nano | P3 | 21% (15%–28%) n=162 | 57% (41%–71%) n=37 | +0.36 (+0.18 to +0.51) | n/a |
| GPT-4.1-nano | P5 | 28% (22%–36%) n=162 | 54% (38%–69%) n=37 | +0.26 (+0.08 to +0.42) | n/a |
| GPT-4.1-nano [evidence_first] | P1 | 7% (4%–12%) n=159 | 48% (33%–63%) n=40 | +0.41 (+0.25 to +0.56) | n/a |
| GPT-4.1-nano [evidence_first] | P2 | 13% (9%–19%) n=159 | 52% (37%–67%) n=40 | +0.39 (+0.23 to +0.55) | n/a |
| GPT-4.1-nano [evidence_first] | P3 | 11% (7%–16%) n=159 | 62% (47%–76%) n=40 | +0.52 (+0.35 to +0.66) | n/a |
| GPT-4.1-nano [evidence_first] | P5 | 11% (7%–16%) n=159 | 48% (33%–63%) n=40 | +0.37 (+0.21 to +0.52) | n/a |
| GPT-4.1-nano [resolve_first] | P1 | 7% (4%–13%) n=161 | 42% (27%–58%) n=36 | +0.34 (+0.19 to +0.51) | n/a |
| GPT-4.1-nano [resolve_first] | P2 | 16% (11%–22%) n=161 | 44% (30%–60%) n=36 | +0.29 (+0.13 to +0.46) | n/a |
| GPT-4.1-nano [resolve_first] | P3 | 19% (14%–26%) n=161 | 56% (40%–70%) n=36 | +0.36 (+0.19 to +0.52) | n/a |
| GPT-4.1-nano [resolve_first] | P5 | 22% (17%–29%) n=161 | 56% (40%–70%) n=36 | +0.33 (+0.16 to +0.49) | n/a |
| GPT-4o-mini | P1 | 2% (1%–6%) n=155 | 31% (20%–46%) n=45 | +0.29 (+0.17 to +0.44) | n/a |
| GPT-4o-mini | P2 | 6% (4%–11%) n=155 | 47% (33%–61%) n=45 | +0.40 (+0.26 to +0.55) | n/a |
| GPT-4o-mini | P3 | 6% (3%–11%) n=155 | 51% (37%–65%) n=45 | +0.45 (+0.30 to +0.60) | n/a |
| GPT-4o-mini | P5 | 8% (4%–13%) n=155 | 33% (21%–48%) n=45 | +0.26 (+0.12 to +0.41) | n/a |
| GPT-4o-mini [evidence_first] | P1 | 3% (1%–7%) n=162 | 32% (19%–47%) n=38 | +0.28 (+0.15 to +0.44) | n/a |
| GPT-4o-mini [evidence_first] | P2 | 6% (3%–11%) n=162 | 29% (17%–45%) n=38 | +0.23 (+0.10 to +0.39) | n/a |
| GPT-4o-mini [evidence_first] | P3 | 6% (3%–11%) n=162 | 34% (21%–50%) n=38 | +0.28 (+0.14 to +0.44) | n/a |
| GPT-4o-mini [evidence_first] | P5 | 7% (4%–12%) n=162 | 32% (19%–47%) n=38 | +0.25 (+0.11 to +0.41) | n/a |
| GPT-4o-mini [resolve_first] | P1 | 2% (1%–5%) n=158 | 29% (17%–44%) n=42 | +0.27 (+0.15 to +0.42) | n/a |
| GPT-4o-mini [resolve_first] | P2 | 4% (2%–8%) n=158 | 24% (13%–39%) n=42 | +0.20 (+0.09 to +0.35) | n/a |
| GPT-4o-mini [resolve_first] | P3 | 8% (4%–13%) n=158 | 38% (25%–53%) n=42 | +0.31 (+0.16 to +0.46) | n/a |
| GPT-4o-mini [resolve_first] | P5 | 6% (3%–10%) n=158 | 31% (19%–46%) n=42 | +0.25 (+0.12 to +0.41) | n/a |
| GPT-5-mini | P1 | 1% (0%–4%) n=180 | 25% (11%–47%) n=20 | +0.24 (+0.10 to +0.46) | n/a |
| GPT-5-mini | P2 | 8% (5%–13%) n=180 | 45% (26%–66%) n=20 | +0.37 (+0.17 to +0.58) | n/a |
| GPT-5-mini | P3 | 3% (1%–6%) n=180 | 47% (27%–68%) n=19 | +0.45 (+0.24 to +0.66) | n/a |
| GPT-5-mini | P5 | 20% (15%–26%) n=180 | 55% (34%–74%) n=20 | +0.35 (+0.13 to +0.55) | n/a |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

## Capitulation, update and discrimination (prefilled)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 17% (12%–24%) n=162 | 94% (90%–97%) n=162 | +0.77 (+0.69 to +0.83) | +0.02 |
| GPT-4.1-nano | P2 | 45% (38%–53%) n=162 | 98% (94%–99%) n=162 | +0.52 (+0.44 to +0.60) | -0.22 |
| GPT-4.1-nano | P3 | 30% (24%–38%) n=162 | 97% (93%–99%) n=162 | +0.67 (+0.58 to +0.73) | -0.08 |
| GPT-4.1-nano | P5 | 70% (62%–76%) n=162 | 98% (95%–99%) n=162 | +0.28 (+0.21 to +0.36) | -0.46 |
| GPT-4.1-nano [evidence_first] | P1 | 12% (8%–18%) n=159 | 96% (91%–98%) n=159 | +0.84 (+0.76 to +0.88) | +0.02 |
| GPT-4.1-nano [evidence_first] | P2 | 26% (20%–33%) n=159 | 97% (93%–99%) n=159 | +0.71 (+0.63 to +0.77) | -0.11 |
| GPT-4.1-nano [evidence_first] | P3 | 20% (15%–27%) n=159 | 96% (92%–98%) n=159 | +0.76 (+0.68 to +0.82) | -0.06 |
| GPT-4.1-nano [evidence_first] | P5 | 45% (38%–53%) n=159 | 96% (91%–98%) n=159 | +0.50 (+0.41 to +0.58) | -0.31 |
| GPT-4.1-nano [resolve_first] | P1 | 10% (6%–16%) n=161 | 96% (92%–98%) n=161 | +0.86 (+0.79 to +0.91) | +0.05 |
| GPT-4.1-nano [resolve_first] | P2 | 40% (33%–48%) n=161 | 98% (95%–99%) n=161 | +0.58 (+0.49 to +0.65) | -0.24 |
| GPT-4.1-nano [resolve_first] | P3 | 30% (24%–38%) n=161 | 99% (97%–100%) n=161 | +0.69 (+0.61 to +0.76) | -0.12 |
| GPT-4.1-nano [resolve_first] | P5 | 61% (53%–68%) n=161 | 99% (97%–100%) n=161 | +0.39 (+0.31 to +0.46) | -0.43 |
| GPT-4o-mini | P1 | 4% (2%–8%) n=155 | 94% (89%–97%) n=155 | +0.90 (+0.84 to +0.94) | -0.00 |
| GPT-4o-mini | P2 | 3% (1%–6%) n=155 | 97% (94%–99%) n=155 | +0.95 (+0.89 to +0.97) | +0.05 |
| GPT-4o-mini | P3 | 3% (1%–6%) n=155 | 99% (95%–100%) n=155 | +0.96 (+0.91 to +0.98) | +0.06 |
| GPT-4o-mini | P5 | 25% (18%–32%) n=155 | 100% (98%–100%) n=155 | +0.75 (+0.68 to +0.82) | -0.15 |
| GPT-4o-mini [evidence_first] | P1 | 2% (1%–6%) n=162 | 87% (81%–91%) n=162 | +0.85 (+0.77 to +0.89) | -0.01 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–2%) n=162 | 76% (69%–82%) n=162 | +0.76 (+0.68 to +0.82) | -0.10 |
| GPT-4o-mini [evidence_first] | P3 | 1% (0%–3%) n=162 | 78% (71%–84%) n=162 | +0.78 (+0.70 to +0.83) | -0.08 |
| GPT-4o-mini [evidence_first] | P5 | 6% (3%–10%) n=162 | 94% (89%–97%) n=162 | +0.88 (+0.82 to +0.92) | +0.02 |
| GPT-4o-mini [resolve_first] | P1 | 1% (0%–4%) n=158 | 94% (89%–97%) n=158 | +0.92 (+0.87 to +0.95) | +0.06 |
| GPT-4o-mini [resolve_first] | P2 | 1% (0%–4%) n=158 | 91% (85%–94%) n=158 | +0.89 (+0.83 to +0.93) | +0.03 |
| GPT-4o-mini [resolve_first] | P3 | 1% (0%–4%) n=158 | 91% (85%–94%) n=158 | +0.89 (+0.83 to +0.93) | +0.03 |
| GPT-4o-mini [resolve_first] | P5 | 7% (4%–12%) n=158 | 97% (94%–99%) n=158 | +0.91 (+0.84 to +0.94) | +0.04 |
| GPT-5-mini | P1 | 1% (0%–3%) n=180 | 98% (94%–99%) n=180 | +0.97 (+0.93 to +0.99) | +0.04 |
| GPT-5-mini | P2 | 4% (2%–8%) n=180 | 94% (90%–97%) n=180 | +0.91 (+0.85 to +0.94) | -0.03 |
| GPT-5-mini | P3 | 2% (1%–6%) n=180 | 97% (94%–99%) n=179 | +0.95 (+0.90 to +0.97) | +0.02 |
| GPT-5-mini | P5 | 10% (6%–15%) n=180 | 99% (96%–100%) n=180 | +0.89 (+0.83 to +0.93) | -0.04 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 3% (1%–7%) | 78% (71%–83%) |
| GPT-4.1-nano [evidence_first] | 3% (1%–6%) | 84% (78%–89%) |
| GPT-4.1-nano [resolve_first] | 2% (1%–5%) | 83% (77%–88%) |
| GPT-4o-mini | 3% (1%–6%) | 93% (88%–96%) |
| GPT-4o-mini [evidence_first] | 3% (1%–7%) | 89% (83%–93%) |
| GPT-4o-mini [resolve_first] | 1% (0%–4%) | 87% (81%–92%) |
| GPT-5-mini | 2% (1%–6%) | 96% (91%–98%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 162 | 67% | 16% | 85/3 | 7.34e-22 | 9.55e-21 |
| GPT-4.1-nano: P3 vs P1 | 162 | 49% | 16% | 58/4 | 2.59e-13 | 3.11e-12 |
| GPT-4.1-nano [evidence_first]: P2 vs P1 | 159 | 35% | 16% | 40/10 | 2.39e-05 | 0.000239 |
| GPT-4.1-nano [evidence_first]: P3 vs P1 | 159 | 26% | 16% | 26/11 | 0.0201 | 0.161 |
| GPT-4.1-nano [resolve_first]: P2 vs P1 | 161 | 66% | 17% | 82/2 | 3.69e-22 | 5.17e-21 |
| GPT-4.1-nano [resolve_first]: P3 vs P1 | 161 | 50% | 17% | 59/5 | 9e-13 | 9.9e-12 |
| GPT-4o-mini: P2 vs P1 | 155 | 2% | 1% | 3/2 | 1 | 1 |
| GPT-4o-mini: P3 vs P1 | 155 | 8% | 1% | 12/1 | 0.00342 | 0.0308 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 162 | 0% | 1% | 0/1 | 1 | 1 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 162 | 0% | 1% | 0/1 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P2 vs P1 | 158 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P3 vs P1 | 158 | 2% | 0% | 3/0 | 0.25 | 1 |
| GPT-5-mini: P2 vs P1 | 180 | 1% | 0% | 1/0 | 1 | 1 |
| GPT-5-mini: P3 vs P1 | 180 | 2% | 0% | 3/0 | 0.25 | 1 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 follow-up vs preemptive | 162 | 16% | 10% | 21/11 | 0.11 | 0.984 |
| GPT-4.1-nano: P2 follow-up vs preemptive | 162 | 67% | 26% | 71/5 | 5.25e-16 | 1.26e-14 |
| GPT-4.1-nano: P3 follow-up vs preemptive | 162 | 49% | 21% | 56/10 | 6.9e-09 | 1.45e-07 |
| GPT-4.1-nano: P5 follow-up vs preemptive | 162 | 88% | 28% | 100/4 | 4.72e-25 | 1.32e-23 |
| GPT-4.1-nano [evidence_first]: P1 follow-up vs preemptive | 159 | 16% | 7% | 21/6 | 0.00592 | 0.0829 |
| GPT-4.1-nano [evidence_first]: P2 follow-up vs preemptive | 159 | 35% | 13% | 42/7 | 3.62e-07 | 7.25e-06 |
| GPT-4.1-nano [evidence_first]: P3 follow-up vs preemptive | 159 | 26% | 11% | 29/5 | 3.86e-05 | 0.000694 |
| GPT-4.1-nano [evidence_first]: P5 follow-up vs preemptive | 159 | 61% | 11% | 81/1 | 3.43e-23 | 8.93e-22 |
| GPT-4.1-nano [resolve_first]: P1 follow-up vs preemptive | 161 | 17% | 7% | 23/8 | 0.0107 | 0.139 |
| GPT-4.1-nano [resolve_first]: P2 follow-up vs preemptive | 161 | 66% | 16% | 86/4 | 4.32e-21 | 1.08e-19 |
| GPT-4.1-nano [resolve_first]: P3 follow-up vs preemptive | 161 | 50% | 19% | 58/8 | 1.8e-10 | 3.95e-09 |
| GPT-4.1-nano [resolve_first]: P5 follow-up vs preemptive | 161 | 78% | 22% | 93/3 | 3.72e-24 | 1.01e-22 |
| GPT-4o-mini: P1 follow-up vs preemptive | 155 | 1% | 2% | 2/3 | 1 | 1 |
| GPT-4o-mini: P2 follow-up vs preemptive | 155 | 2% | 6% | 2/9 | 0.0654 | 0.654 |
| GPT-4o-mini: P3 follow-up vs preemptive | 155 | 8% | 6% | 12/8 | 0.503 | 1 |
| GPT-4o-mini: P5 follow-up vs preemptive | 155 | 40% | 8% | 52/2 | 1.65e-13 | 3.79e-12 |
| GPT-4o-mini [evidence_first]: P1 follow-up vs preemptive | 162 | 1% | 3% | 1/5 | 0.219 | 1 |
| GPT-4o-mini [evidence_first]: P2 follow-up vs preemptive | 162 | 0% | 6% | 0/10 | 0.00195 | 0.0312 |
| GPT-4o-mini [evidence_first]: P3 follow-up vs preemptive | 162 | 0% | 6% | 0/10 | 0.00195 | 0.0312 |
| GPT-4o-mini [evidence_first]: P5 follow-up vs preemptive | 162 | 4% | 7% | 5/9 | 0.424 | 1 |
| GPT-4o-mini [resolve_first]: P1 follow-up vs preemptive | 158 | 0% | 2% | 0/3 | 0.25 | 1 |
| GPT-4o-mini [resolve_first]: P2 follow-up vs preemptive | 158 | 0% | 4% | 0/6 | 0.0312 | 0.344 |
| GPT-4o-mini [resolve_first]: P3 follow-up vs preemptive | 158 | 2% | 8% | 2/11 | 0.0225 | 0.27 |
| GPT-4o-mini [resolve_first]: P5 follow-up vs preemptive | 158 | 9% | 6% | 8/2 | 0.109 | 0.984 |
| GPT-5-mini: P1 follow-up vs preemptive | 180 | 0% | 1% | 0/2 | 0.5 | 1 |
| GPT-5-mini: P2 follow-up vs preemptive | 180 | 1% | 8% | 0/13 | 0.000244 | 0.00415 |
| GPT-5-mini: P3 follow-up vs preemptive | 180 | 2% | 3% | 3/5 | 0.727 | 1 |
| GPT-5-mini: P5 follow-up vs preemptive | 180 | 4% | 20% | 6/34 | 8.36e-06 | 0.000159 |

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 update vs capitulation | 162 | 94% | 17% | 131/6 | 9.88e-32 | 6.92e-31 |
| GPT-4.1-nano: P2 update vs capitulation | 162 | 98% | 45% | 86/1 | 1.14e-24 | 4.55e-24 |
| GPT-4.1-nano: P3 update vs capitulation | 162 | 97% | 30% | 112/4 | 1.79e-28 | 1.07e-27 |
| GPT-4.1-nano: P5 update vs capitulation | 162 | 98% | 70% | 48/2 | 2.27e-12 | 2.27e-12 |
| GPT-4.1-nano [evidence_first]: P1 update vs capitulation | 159 | 96% | 12% | 135/2 | 1.09e-37 | 1.52e-36 |
| GPT-4.1-nano [evidence_first]: P2 update vs capitulation | 159 | 97% | 26% | 115/2 | 8.31e-32 | 6.65e-31 |
| GPT-4.1-nano [evidence_first]: P3 update vs capitulation | 159 | 96% | 20% | 122/1 | 2.33e-35 | 2.33e-34 |
| GPT-4.1-nano [evidence_first]: P5 update vs capitulation | 159 | 96% | 45% | 84/4 | 1.58e-20 | 4.74e-20 |
| GPT-4.1-nano [resolve_first]: P1 update vs capitulation | 161 | 96% | 10% | 140/1 | 1.02e-40 | 1.73e-39 |
| GPT-4.1-nano [resolve_first]: P2 update vs capitulation | 161 | 98% | 40% | 93/0 | 2.02e-28 | 1.07e-27 |
| GPT-4.1-nano [resolve_first]: P3 update vs capitulation | 161 | 99% | 30% | 111/0 | 7.7e-34 | 6.93e-33 |
| GPT-4.1-nano [resolve_first]: P5 update vs capitulation | 161 | 99% | 61% | 63/1 | 7.05e-18 | 1.41e-17 |
| GPT-4o-mini: P1 update vs capitulation | 155 | 94% | 4% | 140/0 | 1.43e-42 | 3.01e-41 |
| GPT-4o-mini: P2 update vs capitulation | 155 | 97% | 3% | 147/0 | 1.12e-44 | 2.58e-43 |
| GPT-4o-mini: P3 update vs capitulation | 155 | 99% | 3% | 149/0 | 2.8e-45 | 6.73e-44 |
| GPT-4o-mini: P5 update vs capitulation | 155 | 100% | 25% | 117/0 | 1.2e-35 | 1.32e-34 |
| GPT-4o-mini [evidence_first]: P1 update vs capitulation | 162 | 87% | 2% | 140/3 | 8.74e-38 | 1.31e-36 |
| GPT-4o-mini [evidence_first]: P2 update vs capitulation | 162 | 76% | 0% | 123/0 | 1.88e-37 | 2.45e-36 |
| GPT-4o-mini [evidence_first]: P3 update vs capitulation | 162 | 78% | 1% | 127/1 | 7.58e-37 | 9.1e-36 |
| GPT-4o-mini [evidence_first]: P5 update vs capitulation | 162 | 94% | 6% | 146/3 | 1.55e-39 | 2.47e-38 |
| GPT-4o-mini [resolve_first]: P1 update vs capitulation | 158 | 94% | 1% | 148/2 | 1.59e-41 | 3.02e-40 |
| GPT-4o-mini [resolve_first]: P2 update vs capitulation | 158 | 91% | 1% | 141/0 | 7.17e-43 | 1.58e-41 |
| GPT-4o-mini [resolve_first]: P3 update vs capitulation | 158 | 91% | 1% | 142/1 | 2.58e-41 | 4.65e-40 |
| GPT-4o-mini [resolve_first]: P5 update vs capitulation | 158 | 97% | 7% | 144/1 | 6.55e-42 | 1.31e-40 |
| GPT-5-mini: P1 update vs capitulation | 180 | 98% | 1% | 175/0 | 4.18e-53 | 1.17e-51 |
| GPT-5-mini: P2 update vs capitulation | 180 | 94% | 4% | 164/1 | 7.1e-48 | 1.92e-46 |
| GPT-5-mini: P3 update vs capitulation | 179 | 97% | 2% | 173/3 | 1.9e-47 | 4.93e-46 |
| GPT-5-mini: P5 update vs capitulation | 180 | 99% | 10% | 161/1 | 5.58e-47 | 1.39e-45 |

## H3: is discrimination explained by accuracy?

Spearman rank correlation of baseline accuracy and J across 7 model conditions: **-0.63** (descriptive; n = models).

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: evidence_first vs default, capitulation P1 | 150 | 14% | 15% | 13/14 | 1 | 1 |
| GPT-4.1-nano: evidence_first vs default, update P1 | 28 | 64% | 71% | 2/4 | 0.688 | 1 |
| GPT-4.1-nano: evidence_first vs default, capitulation P2 | 150 | 34% | 65% | 4/50 | 3.8e-11 | 5.32e-10 |
| GPT-4.1-nano: evidence_first vs default, update P2 | 28 | 75% | 96% | 0/6 | 0.0312 | 0.312 |
| GPT-4.1-nano: evidence_first vs default, capitulation P3 | 150 | 26% | 47% | 11/43 | 1.4e-05 | 0.000168 |
| GPT-4.1-nano: evidence_first vs default, update P3 | 28 | 82% | 96% | 1/5 | 0.219 | 1 |
| GPT-4.1-nano: evidence_first vs default, capitulation P5 | 150 | 59% | 87% | 4/45 | 8.23e-10 | 1.07e-08 |
| GPT-4.1-nano: evidence_first vs default, update P5 | 28 | 100% | 93% | 2/0 | 0.5 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P1 | 149 | 15% | 15% | 12/11 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P1 | 24 | 58% | 67% | 4/6 | 0.754 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P2 | 149 | 66% | 66% | 22/22 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P2 | 24 | 96% | 100% | 0/1 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P3 | 149 | 50% | 47% | 23/19 | 0.644 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P3 | 24 | 96% | 96% | 1/1 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P5 | 149 | 79% | 87% | 11/23 | 0.0576 | 0.519 |
| GPT-4.1-nano: resolve_first vs default, update P5 | 24 | 96% | 96% | 1/1 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, capitulation P1 | 152 | 1% | 1% | 1/2 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, update P1 | 35 | 9% | 43% | 0/12 | 0.000488 | 0.00684 |
| GPT-4o-mini: evidence_first vs default, capitulation P2 | 152 | 0% | 2% | 0/3 | 0.25 | 1 |
| GPT-4o-mini: evidence_first vs default, update P2 | 35 | 0% | 11% | 0/4 | 0.125 | 1 |
| GPT-4o-mini: evidence_first vs default, capitulation P3 | 152 | 0% | 9% | 0/13 | 0.000244 | 0.00269 |
| GPT-4o-mini: evidence_first vs default, update P3 | 35 | 6% | 51% | 0/16 | 3.05e-05 | 0.000458 |
| GPT-4o-mini: evidence_first vs default, capitulation P5 | 152 | 3% | 40% | 1/57 | 4.09e-16 | 6.55e-15 |
| GPT-4o-mini: evidence_first vs default, update P5 | 35 | 29% | 91% | 0/22 | 4.77e-07 | 7.63e-06 |
| GPT-4o-mini: resolve_first vs default, capitulation P1 | 151 | 0% | 1% | 0/2 | 0.5 | 1 |
| GPT-4o-mini: resolve_first vs default, update P1 | 38 | 16% | 39% | 2/11 | 0.0225 | 0.247 |
| GPT-4o-mini: resolve_first vs default, capitulation P2 | 151 | 0% | 2% | 0/3 | 0.25 | 1 |
| GPT-4o-mini: resolve_first vs default, update P2 | 38 | 11% | 11% | 4/4 | 1 | 1 |
| GPT-4o-mini: resolve_first vs default, capitulation P3 | 151 | 1% | 9% | 0/11 | 0.000977 | 0.00977 |
| GPT-4o-mini: resolve_first vs default, update P3 | 38 | 21% | 53% | 1/13 | 0.00183 | 0.022 |
| GPT-4o-mini: resolve_first vs default, capitulation P5 | 151 | 8% | 40% | 2/50 | 6.12e-13 | 9.19e-12 |
| GPT-4o-mini: resolve_first vs default, update P5 | 38 | 55% | 89% | 1/14 | 0.000977 | 0.0127 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 2% (1%–4%) |
| P1 | followup | 1 | 8% (6%–11%) |
| P1 | followup | 2 | 11% (8%–14%) |
| P1 | preemptive | 0 | 8% (5%–11%) |
| P1 | preemptive | 1 | 4% (2%–6%) |
| P1 | preemptive | 2 | 2% (1%–4%) |
| P1 | prefilled | 0 | 3% (2%–5%) |
| P1 | prefilled | 1 | 11% (8%–14%) |
| P1 | prefilled | 2 | 7% (5%–10%) |
| P2 | followup | 0 | 16% (12%–20%) |
| P2 | followup | 1 | 25% (21%–29%) |
| P2 | followup | 2 | 32% (27%–37%) |
| P2 | preemptive | 0 | 6% (4%–9%) |
| P2 | preemptive | 1 | 17% (13%–21%) |
| P2 | preemptive | 2 | 12% (9%–15%) |
| P2 | prefilled | 0 | 11% (8%–14%) |
| P2 | prefilled | 1 | 16% (13%–20%) |
| P2 | prefilled | 2 | 25% (21%–30%) |
| P3 | followup | 0 | 16% (13%–20%) |
| P3 | followup | 1 | 24% (20%–28%) |
| P3 | followup | 2 | 17% (14%–22%) |
| P3 | preemptive | 0 | 7% (5%–10%) |
| P3 | preemptive | 1 | 12% (9%–16%) |
| P3 | preemptive | 2 | 13% (10%–17%) |
| P3 | prefilled | 0 | 16% (13%–20%) |
| P3 | prefilled | 1 | 14% (11%–18%) |
| P3 | prefilled | 2 | 7% (5%–10%) |
| P5 | followup | 0 | 41% (36%–46%) |
| P5 | followup | 1 | 37% (33%–41%) |
| P5 | followup | 2 | 45% (40%–51%) |
| P5 | preemptive | 0 | 25% (21%–30%) |
| P5 | preemptive | 1 | 6% (4%–8%) |
| P5 | preemptive | 2 | 14% (11%–18%) |
| P5 | prefilled | 0 | 39% (34%–44%) |
| P5 | prefilled | 1 | 21% (17%–26%) |
| P5 | prefilled | 2 | 32% (28%–36%) |
