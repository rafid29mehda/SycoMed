# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | questions | baseline accuracy | unstable q | follow-up arms (invalid / valid q) | prefilled arms (invalid / valid q) | unparsed baselines |
|---|---|---|---|---|---|---|
| GPT-4.1-nano | 673 | 80% (79%–82%) | 74 | 502 / 91 | 502 / 502 | 20 |
| GPT-4.1-nano [evidence_first] | 673 | 81% (79%–83%) | 85 | 501 / 76 | 501 / 501 | 31 |
| GPT-4.1-nano [resolve_first] | 673 | 80% (79%–82%) | 91 | 494 / 79 | 494 / 494 | 32 |
| GPT-4o-mini | 673 | 80% (79%–82%) | 35 | 525 / 112 | 525 / 525 | 5 |
| GPT-4o-mini [evidence_first] | 673 | 80% (79%–82%) | 47 | 519 / 106 | 519 / 519 | 5 |
| GPT-4o-mini [resolve_first] | 673 | 80% (79%–82%) | 39 | 522 / 111 | 522 / 522 | 6 |
| GPT-5-mini | 673 | 93% (91%–94%) | 47 | 594 / 30 | 594 / 594 | 0 |
| GPT-5-mini [evidence_first] | 673 | 92% (90%–93%) | 63 | 580 / 27 | 580 / 580 | 0 |
| GPT-5-mini [resolve_first] | 673 | 92% (90%–93%) | 52 | 586 / 32 | 586 / 586 | 0 |

_Unstable q = questions whose repeated unpressured answers disagree on correctness; they are excluded from both arms._
_In the follow-up structure the valid arm is the model's own errors, so it is small for accurate models: do not interpret update rates there below ~20 questions. The prefilled design tests every known question both ways._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 23% (20%–27%) n=502 | 57% (47%–67%) n=91 | +0.34 (+0.23 to +0.44) | +0.33 |
| GPT-4.1-nano | P2 | 74% (69%–77%) n=502 | 91% (84%–95%) n=91 | +0.18 (+0.09 to +0.24) | +0.17 |
| GPT-4.1-nano | P3 | 51% (47%–56%) n=502 | 80% (71%–87%) n=91 | +0.29 (+0.19 to +0.37) | +0.28 |
| GPT-4.1-nano | P5 | 90% (88%–93%) n=502 | 99% (94%–100%) n=91 | +0.08 (+0.03 to +0.11) | +0.07 |
| GPT-4.1-nano | P6 | 29% (25%–33%) n=501 | 80% (71%–87%) n=91 | +0.52 (+0.41 to +0.60) | +0.51 |
| GPT-4.1-nano [evidence_first] | P1 | 16% (13%–19%) n=501 | 53% (42%–63%) n=76 | +0.37 (+0.25 to +0.48) | +0.30 |
| GPT-4.1-nano [evidence_first] | P2 | 40% (36%–44%) n=501 | 68% (57%–78%) n=76 | +0.29 (+0.17 to +0.39) | +0.21 |
| GPT-4.1-nano [evidence_first] | P3 | 25% (21%–29%) n=501 | 64% (53%–74%) n=76 | +0.40 (+0.28 to +0.50) | +0.33 |
| GPT-4.1-nano [evidence_first] | P5 | 71% (67%–74%) n=501 | 92% (84%–96%) n=76 | +0.21 (+0.12 to +0.27) | +0.14 |
| GPT-4.1-nano [evidence_first] | P6 | 23% (20%–27%) n=500 | 70% (59%–79%) n=76 | +0.47 (+0.35 to +0.57) | +0.40 |
| GPT-4.1-nano [resolve_first] | P1 | 20% (17%–24%) n=494 | 59% (48%–70%) n=79 | +0.39 (+0.27 to +0.50) | +0.27 |
| GPT-4.1-nano [resolve_first] | P2 | 73% (69%–76%) n=494 | 91% (83%–96%) n=79 | +0.18 (+0.09 to +0.25) | +0.07 |
| GPT-4.1-nano [resolve_first] | P3 | 53% (49%–58%) n=494 | 86% (77%–92%) n=79 | +0.33 (+0.23 to +0.40) | +0.21 |
| GPT-4.1-nano [resolve_first] | P5 | 89% (86%–92%) n=494 | 99% (93%–100%) n=79 | +0.09 (+0.03 to +0.13) | -0.02 |
| GPT-4.1-nano [resolve_first] | P6 | 26% (22%–30%) n=493 | 82% (72%–89%) n=79 | +0.56 (+0.45 to +0.64) | +0.44 |
| GPT-4o-mini | P1 | 6% (4%–8%) n=525 | 21% (15%–30%) n=112 | +0.15 (+0.08 to +0.24) | +0.09 |
| GPT-4o-mini | P2 | 2% (1%–4%) n=525 | 12% (8%–20%) n=112 | +0.10 (+0.05 to +0.18) | +0.04 |
| GPT-4o-mini | P3 | 16% (13%–19%) n=525 | 46% (37%–56%) n=112 | +0.31 (+0.21 to +0.40) | +0.25 |
| GPT-4o-mini | P5 | 54% (50%–59%) n=525 | 83% (75%–89%) n=112 | +0.29 (+0.20 to +0.36) | +0.23 |
| GPT-4o-mini | P6 | 7% (5%–10%) n=524 | 58% (49%–67%) n=112 | +0.51 (+0.41 to +0.60) | +0.45 |
| GPT-4o-mini [evidence_first] | P1 | 1% (0%–2%) n=519 | 8% (5%–15%) n=106 | +0.08 (+0.03 to +0.14) | +0.02 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–1%) n=519 | 1% (0%–5%) n=106 | +0.01 (-0.00 to +0.05) | -0.05 |
| GPT-4o-mini [evidence_first] | P3 | 0% (0%–1%) n=519 | 2% (1%–7%) n=106 | +0.02 (-0.00 to +0.06) | -0.04 |
| GPT-4o-mini [evidence_first] | P5 | 5% (3%–7%) n=519 | 26% (19%–36%) n=106 | +0.21 (+0.14 to +0.31) | +0.16 |
| GPT-4o-mini [evidence_first] | P6 | 2% (1%–3%) n=518 | 33% (25%–42%) n=106 | +0.31 (+0.23 to +0.41) | +0.26 |
| GPT-4o-mini [resolve_first] | P1 | 2% (1%–4%) n=522 | 11% (6%–18%) n=111 | +0.09 (+0.04 to +0.16) | +0.01 |
| GPT-4o-mini [resolve_first] | P2 | 1% (1%–3%) n=522 | 11% (6%–18%) n=111 | +0.09 (+0.05 to +0.17) | +0.02 |
| GPT-4o-mini [resolve_first] | P3 | 3% (2%–5%) n=522 | 17% (11%–25%) n=111 | +0.14 (+0.08 to +0.22) | +0.07 |
| GPT-4o-mini [resolve_first] | P5 | 16% (13%–19%) n=522 | 52% (43%–61%) n=111 | +0.36 (+0.26 to +0.46) | +0.29 |
| GPT-4o-mini [resolve_first] | P6 | 4% (3%–6%) n=521 | 43% (34%–53%) n=111 | +0.39 (+0.30 to +0.48) | +0.32 |
| GPT-5-mini | P1 | 1% (0%–1%) n=594 | 3% (1%–17%) n=30 | +0.03 (-0.00 to +0.16) | +0.03 |
| GPT-5-mini | P2 | 2% (1%–3%) n=594 | 3% (1%–17%) n=30 | +0.02 (-0.01 to +0.15) | +0.02 |
| GPT-5-mini | P3 | 3% (2%–5%) n=594 | 13% (5%–30%) n=30 | +0.10 (+0.02 to +0.27) | +0.11 |
| GPT-5-mini | P5 | 7% (5%–9%) n=594 | 30% (17%–48%) n=30 | +0.23 (+0.10 to +0.41) | +0.23 |
| GPT-5-mini | P6 | 3% (2%–5%) n=593 | 27% (14%–44%) n=30 | +0.24 (+0.11 to +0.42) | +0.24 |
| GPT-5-mini [evidence_first] | P1 | 0% (0%–1%) n=580 | 11% (4%–28%) n=27 | +0.11 (+0.04 to +0.28) | +0.11 |
| GPT-5-mini [evidence_first] | P2 | 0% (0%–1%) n=580 | 0% (0%–12%) n=27 | -0.00 (-0.01 to +0.12) | -0.00 |
| GPT-5-mini [evidence_first] | P3 | 1% (0%–2%) n=580 | 15% (6%–32%) n=27 | +0.14 (+0.05 to +0.32) | +0.14 |
| GPT-5-mini [evidence_first] | P5 | 4% (3%–6%) n=580 | 22% (11%–41%) n=27 | +0.18 (+0.06 to +0.37) | +0.18 |
| GPT-5-mini [evidence_first] | P6 | 1% (0%–2%) n=579 | 15% (6%–32%) n=27 | +0.14 (+0.05 to +0.31) | +0.14 |
| GPT-5-mini [resolve_first] | P1 | 0% (0%–1%) n=586 | 12% (5%–28%) n=32 | +0.12 (+0.05 to +0.28) | +0.09 |
| GPT-5-mini [resolve_first] | P2 | 1% (1%–2%) n=586 | 16% (7%–32%) n=32 | +0.14 (+0.06 to +0.31) | +0.11 |
| GPT-5-mini [resolve_first] | P3 | 1% (1%–3%) n=586 | 22% (11%–39%) n=32 | +0.21 (+0.10 to +0.37) | +0.17 |
| GPT-5-mini [resolve_first] | P5 | 3% (2%–5%) n=586 | 34% (20%–52%) n=32 | +0.31 (+0.17 to +0.48) | +0.28 |
| GPT-5-mini [resolve_first] | P6 | 1% (1%–3%) n=585 | 25% (13%–42%) n=32 | +0.24 (+0.12 to +0.41) | +0.21 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 2% (1%–4%) | 3% (1%–9%) |
| GPT-4.1-nano [evidence_first] | 1% (0%–2%) | 8% (4%–16%) |
| GPT-4.1-nano [resolve_first] | 1% (0%–2%) | 13% (7%–22%) |
| GPT-4o-mini | 7% (5%–10%) | 13% (8%–21%) |
| GPT-4o-mini [evidence_first] | 5% (3%–7%) | 10% (6%–18%) |
| GPT-4o-mini [resolve_first] | 3% (2%–5%) | 10% (6%–17%) |
| GPT-5-mini | 0% (0%–1%) | 0% (0%–11%) |
| GPT-5-mini [evidence_first] | 0% (0%–1%) | 0% (0%–12%) |
| GPT-5-mini [resolve_first] | 0% (0%–1%) | 3% (1%–16%) |

## Capitulation, update and discrimination (preemptive)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 16% (13%–20%) n=502 | 40% (30%–50%) n=91 | +0.23 (+0.13 to +0.34) | n/a |
| GPT-4.1-nano | P2 | 28% (24%–32%) n=502 | 46% (36%–56%) n=91 | +0.18 (+0.08 to +0.29) | n/a |
| GPT-4.1-nano | P3 | 28% (24%–32%) n=502 | 45% (35%–55%) n=91 | +0.17 (+0.07 to +0.28) | n/a |
| GPT-4.1-nano | P5 | 27% (23%–31%) n=502 | 43% (33%–53%) n=91 | +0.16 (+0.05 to +0.27) | n/a |
| GPT-4.1-nano | P6 | 53% (49%–57%) n=501 | 95% (88%–98%) n=91 | +0.42 (+0.34 to +0.47) | n/a |
| GPT-4.1-nano [evidence_first] | P1 | 12% (9%–15%) n=501 | 37% (27%–48%) n=76 | +0.25 (+0.15 to +0.37) | n/a |
| GPT-4.1-nano [evidence_first] | P2 | 15% (12%–18%) n=501 | 33% (23%–44%) n=76 | +0.18 (+0.08 to +0.30) | n/a |
| GPT-4.1-nano [evidence_first] | P3 | 16% (13%–19%) n=501 | 41% (30%–52%) n=76 | +0.25 (+0.14 to +0.36) | n/a |
| GPT-4.1-nano [evidence_first] | P5 | 16% (13%–19%) n=501 | 32% (22%–43%) n=76 | +0.16 (+0.06 to +0.27) | n/a |
| GPT-4.1-nano [evidence_first] | P6 | 43% (38%–47%) n=500 | 93% (86%–97%) n=76 | +0.51 (+0.42 to +0.56) | n/a |
| GPT-4.1-nano [resolve_first] | P1 | 11% (8%–14%) n=494 | 30% (21%–41%) n=79 | +0.20 (+0.10 to +0.31) | n/a |
| GPT-4.1-nano [resolve_first] | P2 | 17% (14%–20%) n=494 | 35% (26%–46%) n=79 | +0.19 (+0.09 to +0.30) | n/a |
| GPT-4.1-nano [resolve_first] | P3 | 21% (17%–25%) n=494 | 35% (26%–46%) n=79 | +0.15 (+0.04 to +0.26) | n/a |
| GPT-4.1-nano [resolve_first] | P5 | 23% (20%–27%) n=494 | 46% (35%–57%) n=79 | +0.22 (+0.11 to +0.34) | n/a |
| GPT-4.1-nano [resolve_first] | P6 | 39% (35%–44%) n=493 | 92% (84%–96%) n=79 | +0.53 (+0.44 to +0.59) | n/a |
| GPT-4o-mini | P1 | 7% (5%–10%) n=525 | 22% (16%–31%) n=112 | +0.15 (+0.08 to +0.24) | n/a |
| GPT-4o-mini | P2 | 10% (8%–13%) n=525 | 36% (27%–45%) n=112 | +0.25 (+0.17 to +0.35) | n/a |
| GPT-4o-mini | P3 | 13% (10%–16%) n=525 | 29% (21%–38%) n=112 | +0.16 (+0.08 to +0.25) | n/a |
| GPT-4o-mini | P5 | 9% (7%–12%) n=525 | 33% (25%–42%) n=112 | +0.24 (+0.16 to +0.33) | n/a |
| GPT-4o-mini | P6 | 37% (33%–41%) n=524 | 88% (81%–93%) n=112 | +0.52 (+0.43 to +0.58) | n/a |
| GPT-4o-mini [evidence_first] | P1 | 8% (6%–11%) n=519 | 30% (22%–39%) n=106 | +0.22 (+0.14 to +0.32) | n/a |
| GPT-4o-mini [evidence_first] | P2 | 8% (6%–11%) n=519 | 31% (23%–40%) n=106 | +0.23 (+0.15 to +0.33) | n/a |
| GPT-4o-mini [evidence_first] | P3 | 10% (8%–13%) n=519 | 30% (22%–39%) n=106 | +0.20 (+0.12 to +0.30) | n/a |
| GPT-4o-mini [evidence_first] | P5 | 8% (6%–11%) n=519 | 32% (24%–41%) n=106 | +0.24 (+0.15 to +0.33) | n/a |
| GPT-4o-mini [evidence_first] | P6 | 26% (23%–30%) n=518 | 78% (70%–85%) n=106 | +0.52 (+0.42 to +0.60) | n/a |
| GPT-4o-mini [resolve_first] | P1 | 8% (6%–10%) n=522 | 23% (17%–32%) n=111 | +0.16 (+0.08 to +0.24) | n/a |
| GPT-4o-mini [resolve_first] | P2 | 8% (6%–11%) n=522 | 32% (24%–41%) n=111 | +0.23 (+0.15 to +0.32) | n/a |
| GPT-4o-mini [resolve_first] | P3 | 10% (8%–13%) n=522 | 29% (21%–38%) n=111 | +0.19 (+0.11 to +0.28) | n/a |
| GPT-4o-mini [resolve_first] | P5 | 8% (6%–10%) n=522 | 33% (25%–43%) n=111 | +0.26 (+0.17 to +0.35) | n/a |
| GPT-4o-mini [resolve_first] | P6 | 27% (23%–31%) n=521 | 77% (68%–83%) n=111 | +0.50 (+0.40 to +0.58) | n/a |
| GPT-5-mini | P1 | 3% (2%–4%) n=593 | 17% (7%–34%) n=30 | +0.14 (+0.05 to +0.31) | n/a |
| GPT-5-mini | P2 | 10% (8%–12%) n=594 | 50% (33%–67%) n=30 | +0.40 (+0.23 to +0.57) | n/a |
| GPT-5-mini | P3 | 4% (3%–6%) n=593 | 27% (14%–44%) n=30 | +0.23 (+0.10 to +0.40) | n/a |
| GPT-5-mini | P5 | 24% (20%–27%) n=594 | 52% (34%–69%) n=29 | +0.28 (+0.10 to +0.45) | n/a |
| GPT-5-mini | P6 | 25% (21%–28%) n=593 | 77% (59%–88%) n=30 | +0.52 (+0.34 to +0.64) | n/a |
| GPT-5-mini [evidence_first] | P1 | 3% (2%–4%) n=580 | 11% (4%–28%) n=27 | +0.09 (+0.01 to +0.26) | n/a |
| GPT-5-mini [evidence_first] | P2 | 2% (1%–4%) n=578 | 19% (8%–37%) n=27 | +0.16 (+0.06 to +0.34) | n/a |
| GPT-5-mini [evidence_first] | P3 | 1% (1%–3%) n=580 | 11% (4%–28%) n=27 | +0.10 (+0.02 to +0.27) | n/a |
| GPT-5-mini [evidence_first] | P5 | 9% (7%–12%) n=580 | 23% (11%–42%) n=26 | +0.14 (+0.01 to +0.33) | n/a |
| GPT-5-mini [evidence_first] | P6 | 15% (12%–18%) n=579 | 63% (44%–78%) n=27 | +0.48 (+0.29 to +0.64) | n/a |
| GPT-5-mini [resolve_first] | P1 | 2% (1%–3%) n=585 | 12% (5%–28%) n=32 | +0.11 (+0.03 to +0.27) | n/a |
| GPT-5-mini [resolve_first] | P2 | 2% (1%–4%) n=586 | 19% (9%–35%) n=32 | +0.16 (+0.06 to +0.33) | n/a |
| GPT-5-mini [resolve_first] | P3 | 1% (1%–3%) n=586 | 16% (7%–32%) n=32 | +0.14 (+0.05 to +0.30) | n/a |
| GPT-5-mini [resolve_first] | P5 | 6% (4%–8%) n=586 | 32% (19%–50%) n=31 | +0.26 (+0.12 to +0.44) | n/a |
| GPT-5-mini [resolve_first] | P6 | 17% (14%–21%) n=585 | 66% (48%–80%) n=32 | +0.48 (+0.31 to +0.63) | n/a |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

## Capitulation, update and discrimination (prefilled)

| model | pressure | capitulation | update | J = update − capitulation | J adjusted for recheck |
|---|---|---|---|---|---|
| GPT-4.1-nano | P1 | 21% (17%–24%) n=502 | 98% (96%–99%) n=502 | +0.77 (+0.73 to +0.80) | -0.05 |
| GPT-4.1-nano | P2 | 58% (54%–62%) n=502 | 99% (98%–100%) n=502 | +0.41 (+0.37 to +0.45) | -0.41 |
| GPT-4.1-nano | P3 | 32% (29%–37%) n=502 | 99% (98%–100%) n=502 | +0.67 (+0.62 to +0.71) | -0.15 |
| GPT-4.1-nano | P5 | 70% (65%–73%) n=502 | 99% (98%–100%) n=502 | +0.30 (+0.26 to +0.34) | -0.52 |
| GPT-4.1-nano | P6 | 27% (23%–31%) n=501 | 93% (91%–95%) n=501 | +0.67 (+0.62 to +0.71) | -0.15 |
| GPT-4.1-nano [evidence_first] | P1 | 16% (13%–19%) n=501 | 97% (95%–98%) n=501 | +0.81 (+0.77 to +0.84) | -0.01 |
| GPT-4.1-nano [evidence_first] | P2 | 34% (30%–39%) n=501 | 97% (96%–98%) n=501 | +0.63 (+0.58 to +0.67) | -0.19 |
| GPT-4.1-nano [evidence_first] | P3 | 22% (19%–26%) n=501 | 97% (95%–98%) n=501 | +0.75 (+0.70 to +0.78) | -0.08 |
| GPT-4.1-nano [evidence_first] | P5 | 45% (41%–49%) n=501 | 99% (98%–100%) n=501 | +0.54 (+0.50 to +0.58) | -0.28 |
| GPT-4.1-nano [evidence_first] | P6 | 24% (20%–28%) n=500 | 94% (91%–96%) n=500 | +0.70 (+0.65 to +0.74) | -0.13 |
| GPT-4.1-nano [resolve_first] | P1 | 14% (12%–18%) n=494 | 98% (97%–99%) n=494 | +0.84 (+0.80 to +0.87) | +0.03 |
| GPT-4.1-nano [resolve_first] | P2 | 41% (37%–46%) n=494 | 99% (98%–100%) n=494 | +0.58 (+0.54 to +0.62) | -0.23 |
| GPT-4.1-nano [resolve_first] | P3 | 29% (25%–33%) n=494 | 99% (97%–99%) n=494 | +0.70 (+0.66 to +0.74) | -0.11 |
| GPT-4.1-nano [resolve_first] | P5 | 61% (57%–65%) n=494 | 99% (98%–100%) n=494 | +0.38 (+0.34 to +0.42) | -0.43 |
| GPT-4.1-nano [resolve_first] | P6 | 24% (20%–28%) n=493 | 98% (96%–99%) n=493 | +0.74 (+0.70 to +0.78) | -0.07 |
| GPT-4o-mini | P1 | 8% (6%–10%) n=525 | 91% (89%–94%) n=525 | +0.84 (+0.80 to +0.87) | -0.01 |
| GPT-4o-mini | P2 | 9% (7%–12%) n=525 | 92% (90%–94%) n=525 | +0.83 (+0.80 to +0.86) | -0.02 |
| GPT-4o-mini | P3 | 10% (8%–13%) n=525 | 94% (92%–96%) n=525 | +0.84 (+0.80 to +0.87) | -0.01 |
| GPT-4o-mini | P5 | 39% (35%–43%) n=525 | 99% (97%–99%) n=525 | +0.59 (+0.55 to +0.64) | -0.26 |
| GPT-4o-mini | P6 | 7% (5%–10%) n=524 | 94% (92%–96%) n=524 | +0.87 (+0.84 to +0.90) | +0.02 |
| GPT-4o-mini [evidence_first] | P1 | 2% (1%–3%) n=519 | 84% (81%–87%) n=519 | +0.83 (+0.79 to +0.86) | -0.03 |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–1%) n=519 | 70% (66%–74%) n=519 | +0.70 (+0.66 to +0.74) | -0.16 |
| GPT-4o-mini [evidence_first] | P3 | 0% (0%–1%) n=519 | 76% (72%–80%) n=519 | +0.76 (+0.72 to +0.80) | -0.10 |
| GPT-4o-mini [evidence_first] | P5 | 4% (3%–6%) n=519 | 93% (91%–95%) n=519 | +0.89 (+0.86 to +0.91) | +0.03 |
| GPT-4o-mini [evidence_first] | P6 | 3% (1%–4%) n=518 | 88% (85%–90%) n=518 | +0.85 (+0.82 to +0.88) | -0.01 |
| GPT-4o-mini [resolve_first] | P1 | 3% (2%–5%) n=522 | 90% (87%–92%) n=522 | +0.87 (+0.83 to +0.89) | +0.05 |
| GPT-4o-mini [resolve_first] | P2 | 3% (2%–5%) n=522 | 88% (85%–91%) n=522 | +0.85 (+0.82 to +0.88) | +0.03 |
| GPT-4o-mini [resolve_first] | P3 | 2% (1%–4%) n=522 | 88% (85%–90%) n=522 | +0.85 (+0.82 to +0.88) | +0.03 |
| GPT-4o-mini [resolve_first] | P5 | 7% (5%–9%) n=522 | 95% (92%–96%) n=522 | +0.88 (+0.84 to +0.90) | +0.06 |
| GPT-4o-mini [resolve_first] | P6 | 2% (1%–4%) n=521 | 87% (84%–90%) n=521 | +0.85 (+0.81 to +0.88) | +0.03 |
| GPT-5-mini | P1 | 2% (1%–3%) n=594 | 98% (96%–99%) n=594 | +0.96 (+0.94 to +0.97) | +0.02 |
| GPT-5-mini | P2 | 6% (4%–8%) n=594 | 95% (93%–96%) n=594 | +0.89 (+0.86 to +0.91) | -0.05 |
| GPT-5-mini | P3 | 5% (4%–8%) n=594 | 99% (98%–100%) n=594 | +0.94 (+0.91 to +0.95) | -0.01 |
| GPT-5-mini | P5 | 16% (14%–20%) n=594 | 98% (97%–99%) n=594 | +0.82 (+0.79 to +0.85) | -0.12 |
| GPT-5-mini | P6 | 7% (5%–9%) n=593 | 95% (93%–97%) n=593 | +0.89 (+0.85 to +0.91) | -0.06 |
| GPT-5-mini [evidence_first] | P1 | 1% (0%–2%) n=580 | 98% (97%–99%) n=579 | +0.98 (+0.96 to +0.98) | +0.01 |
| GPT-5-mini [evidence_first] | P2 | 1% (0%–2%) n=580 | 95% (93%–97%) n=580 | +0.94 (+0.92 to +0.96) | -0.03 |
| GPT-5-mini [evidence_first] | P3 | 3% (2%–5%) n=580 | 99% (98%–99%) n=580 | +0.96 (+0.93 to +0.97) | -0.01 |
| GPT-5-mini [evidence_first] | P5 | 10% (8%–13%) n=580 | 99% (97%–99%) n=580 | +0.89 (+0.86 to +0.91) | -0.08 |
| GPT-5-mini [evidence_first] | P6 | 4% (3%–6%) n=579 | 95% (93%–96%) n=579 | +0.91 (+0.88 to +0.93) | -0.06 |
| GPT-5-mini [resolve_first] | P1 | 1% (0%–2%) n=586 | 98% (96%–99%) n=586 | +0.97 (+0.95 to +0.98) | -0.00 |
| GPT-5-mini [resolve_first] | P2 | 2% (1%–3%) n=586 | 99% (98%–99%) n=586 | +0.97 (+0.95 to +0.98) | +0.01 |
| GPT-5-mini [resolve_first] | P3 | 2% (1%–4%) n=586 | 99% (98%–100%) n=586 | +0.97 (+0.95 to +0.98) | +0.00 |
| GPT-5-mini [resolve_first] | P5 | 4% (3%–6%) n=586 | 99% (98%–100%) n=586 | +0.95 (+0.93 to +0.96) | -0.02 |
| GPT-5-mini [resolve_first] | P6 | 2% (1%–4%) n=585 | 98% (96%–99%) n=585 | +0.95 (+0.93 to +0.97) | -0.01 |

_J adjusted for recheck = (update − P0 correction) − (capitulation − P0 departure): what is left after removing what the model does on a plain 'are you sure?' with no claim. Descriptive point estimate._

Plain recheck with no claim (P0):

| model | drops a right answer | corrects a wrong answer |
|---|---|---|
| GPT-4.1-nano | 1% (0%–2%) | 83% (79%–86%) |
| GPT-4.1-nano [evidence_first] | 1% (1%–3%) | 84% (80%–87%) |
| GPT-4.1-nano [resolve_first] | 1% (1%–3%) | 82% (79%–85%) |
| GPT-4o-mini | 2% (1%–4%) | 87% (84%–90%) |
| GPT-4o-mini [evidence_first] | 3% (1%–4%) | 89% (86%–91%) |
| GPT-4o-mini [resolve_first] | 1% (0%–2%) | 83% (79%–86%) |
| GPT-5-mini | 1% (0%–2%) | 95% (93%–97%) |
| GPT-5-mini [evidence_first] | 0% (0%–1%) | 97% (95%–98%) |
| GPT-5-mini [resolve_first] | 1% (0%–2%) | 97% (96%–98%) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P2 vs P1 | 502 | 74% | 23% | 265/12 | 2.89e-63 | 4.9e-62 |
| GPT-4.1-nano: P3 vs P1 | 502 | 51% | 23% | 157/16 | 2.79e-30 | 4.19e-29 |
| GPT-4.1-nano [evidence_first]: P2 vs P1 | 501 | 40% | 16% | 155/33 | 4.18e-20 | 5.85e-19 |
| GPT-4.1-nano [evidence_first]: P3 vs P1 | 501 | 25% | 16% | 76/30 | 9.1e-06 | 0.000109 |
| GPT-4.1-nano [resolve_first]: P2 vs P1 | 494 | 73% | 20% | 264/6 | 5.49e-70 | 9.88e-69 |
| GPT-4.1-nano [resolve_first]: P3 vs P1 | 494 | 53% | 20% | 173/11 | 1.32e-38 | 2.11e-37 |
| GPT-4o-mini: P2 vs P1 | 525 | 2% | 6% | 6/27 | 0.000324 | 0.00324 |
| GPT-4o-mini: P3 vs P1 | 525 | 16% | 6% | 63/12 | 1.69e-09 | 2.2e-08 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 519 | 0% | 1% | 0/5 | 0.0625 | 0.5 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 519 | 0% | 1% | 1/4 | 0.375 | 0.801 |
| GPT-4o-mini [resolve_first]: P2 vs P1 | 522 | 1% | 2% | 2/7 | 0.18 | 0.719 |
| GPT-4o-mini [resolve_first]: P3 vs P1 | 522 | 3% | 2% | 9/4 | 0.267 | 0.801 |
| GPT-5-mini: P2 vs P1 | 594 | 2% | 1% | 7/0 | 0.0156 | 0.141 |
| GPT-5-mini: P3 vs P1 | 594 | 3% | 1% | 15/0 | 6.1e-05 | 0.000671 |
| GPT-5-mini [evidence_first]: P2 vs P1 | 580 | 0% | 0% | 2/0 | 0.5 | 0.801 |
| GPT-5-mini [evidence_first]: P3 vs P1 | 580 | 1% | 0% | 5/0 | 0.0625 | 0.5 |
| GPT-5-mini [resolve_first]: P2 vs P1 | 586 | 1% | 0% | 6/1 | 0.125 | 0.625 |
| GPT-5-mini [resolve_first]: P3 vs P1 | 586 | 1% | 0% | 7/1 | 0.0703 | 0.5 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 follow-up vs preemptive | 502 | 23% | 16% | 79/44 | 0.00205 | 0.0266 |
| GPT-4.1-nano: P2 follow-up vs preemptive | 502 | 74% | 28% | 253/24 | 2.19e-49 | 8.75e-48 |
| GPT-4.1-nano: P3 follow-up vs preemptive | 502 | 51% | 28% | 152/34 | 5.18e-19 | 1.61e-17 |
| GPT-4.1-nano: P5 follow-up vs preemptive | 502 | 90% | 27% | 327/8 | 1.06e-85 | 4.66e-84 |
| GPT-4.1-nano: P6 follow-up vs preemptive | 501 | 29% | 53% | 42/164 | 3.15e-18 | 9.46e-17 |
| GPT-4.1-nano [evidence_first]: P1 follow-up vs preemptive | 501 | 16% | 12% | 59/39 | 0.0544 | 0.435 |
| GPT-4.1-nano [evidence_first]: P2 follow-up vs preemptive | 501 | 40% | 15% | 154/28 | 2.79e-22 | 9.21e-21 |
| GPT-4.1-nano [evidence_first]: P3 follow-up vs preemptive | 501 | 25% | 16% | 81/37 | 6.29e-05 | 0.000925 |
| GPT-4.1-nano [evidence_first]: P5 follow-up vs preemptive | 501 | 71% | 16% | 284/10 | 7.42e-71 | 3.19e-69 |
| GPT-4.1-nano [evidence_first]: P6 follow-up vs preemptive | 500 | 23% | 43% | 41/139 | 1.15e-13 | 3.1e-12 |
| GPT-4.1-nano [resolve_first]: P1 follow-up vs preemptive | 494 | 20% | 11% | 73/25 | 1.28e-06 | 2.3e-05 |
| GPT-4.1-nano [resolve_first]: P2 follow-up vs preemptive | 494 | 73% | 17% | 289/12 | 4.73e-70 | 1.99e-68 |
| GPT-4.1-nano [resolve_first]: P3 follow-up vs preemptive | 494 | 53% | 21% | 189/29 | 5.89e-30 | 2.18e-28 |
| GPT-4.1-nano [resolve_first]: P5 follow-up vs preemptive | 494 | 89% | 23% | 334/7 | 4.56e-89 | 2.05e-87 |
| GPT-4.1-nano [resolve_first]: P6 follow-up vs preemptive | 493 | 26% | 39% | 54/119 | 8.57e-07 | 1.63e-05 |
| GPT-4o-mini: P1 follow-up vs preemptive | 525 | 6% | 7% | 22/27 | 0.568 | 1 |
| GPT-4o-mini: P2 follow-up vs preemptive | 525 | 2% | 10% | 5/48 | 7.08e-10 | 1.7e-08 |
| GPT-4o-mini: P3 follow-up vs preemptive | 525 | 16% | 13% | 55/38 | 0.0966 | 0.579 |
| GPT-4o-mini: P5 follow-up vs preemptive | 525 | 54% | 9% | 244/6 | 3.62e-64 | 1.48e-62 |
| GPT-4o-mini: P6 follow-up vs preemptive | 524 | 7% | 37% | 11/166 | 1.09e-36 | 4.25e-35 |
| GPT-4o-mini [evidence_first]: P1 follow-up vs preemptive | 519 | 1% | 8% | 3/39 | 5.63e-09 | 1.24e-07 |
| GPT-4o-mini [evidence_first]: P2 follow-up vs preemptive | 519 | 0% | 8% | 0/41 | 9.09e-13 | 2.36e-11 |
| GPT-4o-mini [evidence_first]: P3 follow-up vs preemptive | 519 | 0% | 10% | 1/50 | 4.62e-14 | 1.29e-12 |
| GPT-4o-mini [evidence_first]: P5 follow-up vs preemptive | 519 | 5% | 8% | 14/32 | 0.0114 | 0.114 |
| GPT-4o-mini [evidence_first]: P6 follow-up vs preemptive | 518 | 2% | 26% | 4/131 | 6.26e-34 | 2.38e-32 |
| GPT-4o-mini [resolve_first]: P1 follow-up vs preemptive | 522 | 2% | 8% | 3/32 | 4.18e-07 | 8.77e-06 |
| GPT-4o-mini [resolve_first]: P2 follow-up vs preemptive | 522 | 1% | 8% | 3/40 | 3.02e-09 | 6.95e-08 |
| GPT-4o-mini [resolve_first]: P3 follow-up vs preemptive | 522 | 3% | 10% | 7/41 | 6.24e-07 | 1.25e-05 |
| GPT-4o-mini [resolve_first]: P5 follow-up vs preemptive | 522 | 16% | 8% | 68/24 | 4.94e-06 | 8.39e-05 |
| GPT-4o-mini [resolve_first]: P6 follow-up vs preemptive | 521 | 4% | 27% | 8/126 | 2.04e-28 | 7.14e-27 |
| GPT-5-mini: P1 follow-up vs preemptive | 593 | 1% | 3% | 2/14 | 0.00418 | 0.0502 |
| GPT-5-mini: P2 follow-up vs preemptive | 594 | 2% | 10% | 7/55 | 2.43e-10 | 6.08e-09 |
| GPT-5-mini: P3 follow-up vs preemptive | 593 | 3% | 4% | 12/18 | 0.362 | 1 |
| GPT-5-mini: P5 follow-up vs preemptive | 594 | 7% | 24% | 24/124 | 1.89e-17 | 5.49e-16 |
| GPT-5-mini: P6 follow-up vs preemptive | 593 | 3% | 25% | 11/141 | 6.57e-30 | 2.36e-28 |
| GPT-5-mini [evidence_first]: P1 follow-up vs preemptive | 580 | 0% | 3% | 0/15 | 6.1e-05 | 0.000925 |
| GPT-5-mini [evidence_first]: P2 follow-up vs preemptive | 578 | 0% | 2% | 2/14 | 0.00418 | 0.0502 |
| GPT-5-mini [evidence_first]: P3 follow-up vs preemptive | 580 | 1% | 1% | 3/6 | 0.508 | 1 |
| GPT-5-mini [evidence_first]: P5 follow-up vs preemptive | 580 | 4% | 9% | 15/47 | 5.78e-05 | 0.000925 |
| GPT-5-mini [evidence_first]: P6 follow-up vs preemptive | 579 | 1% | 15% | 4/84 | 1.58e-20 | 5.06e-19 |
| GPT-5-mini [resolve_first]: P1 follow-up vs preemptive | 585 | 0% | 2% | 2/9 | 0.0654 | 0.458 |
| GPT-5-mini [resolve_first]: P2 follow-up vs preemptive | 586 | 1% | 2% | 6/13 | 0.167 | 0.835 |
| GPT-5-mini [resolve_first]: P3 follow-up vs preemptive | 586 | 1% | 1% | 8/8 | 1 | 1 |
| GPT-5-mini [resolve_first]: P5 follow-up vs preemptive | 586 | 3% | 6% | 14/30 | 0.0226 | 0.204 |
| GPT-5-mini [resolve_first]: P6 follow-up vs preemptive | 585 | 1% | 17% | 4/97 | 3.36e-24 | 1.14e-22 |

## H6: does giving a reason change what the model does?

A = reasoned claim (P6), B = plain disagreement (P1), same questions and arm. The rationale is matched in length and tone for right and wrong claims, so a model that uses the reasoning should capitulate less to flawed reasoning than to a bare claim AND update more to correct reasoning.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: capitulation, P6 vs P1 | 501 | 29% | 23% | 89/61 | 0.0272 | 0.163 |
| GPT-4.1-nano: update, P6 vs P1 | 91 | 80% | 57% | 28/7 | 0.000508 | 0.00305 |
| GPT-4.1-nano [evidence_first]: capitulation, P6 vs P1 | 500 | 23% | 15% | 83/45 | 0.000996 | 0.00797 |
| GPT-4.1-nano [evidence_first]: update, P6 vs P1 | 76 | 70% | 53% | 21/8 | 0.0241 | 0.0965 |
| GPT-4.1-nano [resolve_first]: capitulation, P6 vs P1 | 493 | 26% | 20% | 82/53 | 0.0156 | 0.11 |
| GPT-4.1-nano [resolve_first]: update, P6 vs P1 | 79 | 82% | 59% | 24/6 | 0.00143 | 0.00715 |
| GPT-4o-mini: capitulation, P6 vs P1 | 524 | 7% | 6% | 25/19 | 0.451 | 0.688 |
| GPT-4o-mini: update, P6 vs P1 | 112 | 58% | 21% | 43/2 | 5.89e-11 | 5.3e-10 |
| GPT-4o-mini [evidence_first]: capitulation, P6 vs P1 | 518 | 2% | 1% | 7/3 | 0.344 | 0.688 |
| GPT-4o-mini [evidence_first]: update, P6 vs P1 | 106 | 33% | 8% | 30/4 | 6.16e-06 | 4.32e-05 |
| GPT-4o-mini [resolve_first]: capitulation, P6 vs P1 | 521 | 4% | 2% | 19/9 | 0.0872 | 0.281 |
| GPT-4o-mini [resolve_first]: update, P6 vs P1 | 111 | 43% | 11% | 39/3 | 5.63e-09 | 4.51e-08 |
| GPT-5-mini: capitulation, P6 vs P1 | 593 | 3% | 1% | 14/0 | 0.000122 | 0.0011 |
| GPT-5-mini: update, P6 vs P1 | 30 | 27% | 3% | 8/1 | 0.0391 | 0.117 |
| GPT-5-mini [evidence_first]: capitulation, P6 vs P1 | 579 | 1% | 0% | 6/0 | 0.0312 | 0.163 |
| GPT-5-mini [evidence_first]: update, P6 vs P1 | 27 | 15% | 11% | 4/3 | 1 | 1 |
| GPT-5-mini [resolve_first]: capitulation, P6 vs P1 | 585 | 1% | 0% | 7/1 | 0.0703 | 0.281 |
| GPT-5-mini [resolve_first]: update, P6 vs P1 | 32 | 25% | 12% | 5/1 | 0.219 | 0.438 |

## H5: does the model follow a claim more when it is right? (prefilled design)

Same questions, planted prior answer. A = adopts a CORRECT claim, B = adopts a WRONG claim. A > B means the model's response depends on the truth of the claim.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: P1 update vs capitulation | 502 | 98% | 21% | 390/4 | 4.95e-110 | 7.43e-109 |
| GPT-4.1-nano: P2 update vs capitulation | 502 | 99% | 58% | 209/3 | 4.83e-58 | 1.45e-57 |
| GPT-4.1-nano: P3 update vs capitulation | 502 | 99% | 32% | 336/1 | 2.41e-99 | 2.66e-98 |
| GPT-4.1-nano: P5 update vs capitulation | 502 | 99% | 70% | 152/3 | 2.72e-41 | 2.72e-41 |
| GPT-4.1-nano: P6 update vs capitulation | 501 | 93% | 27% | 342/8 | 4.6e-90 | 3.22e-89 |
| GPT-4.1-nano [evidence_first]: P1 update vs capitulation | 501 | 97% | 16% | 412/5 | 6.14e-115 | 1.04e-113 |
| GPT-4.1-nano [evidence_first]: P2 update vs capitulation | 501 | 97% | 34% | 318/2 | 4.81e-92 | 3.85e-91 |
| GPT-4.1-nano [evidence_first]: P3 update vs capitulation | 501 | 97% | 22% | 384/10 | 1.13e-99 | 1.35e-98 |
| GPT-4.1-nano [evidence_first]: P5 update vs capitulation | 501 | 99% | 45% | 275/4 | 5.16e-76 | 2.06e-75 |
| GPT-4.1-nano [evidence_first]: P6 update vs capitulation | 500 | 94% | 24% | 353/4 | 4.59e-99 | 4.59e-98 |
| GPT-4.1-nano [resolve_first]: P1 update vs capitulation | 494 | 98% | 14% | 419/4 | 1.23e-118 | 2.33e-117 |
| GPT-4.1-nano [resolve_first]: P2 update vs capitulation | 494 | 99% | 41% | 289/2 | 2.14e-83 | 1.07e-82 |
| GPT-4.1-nano [resolve_first]: P3 update vs capitulation | 494 | 99% | 29% | 351/4 | 1.79e-98 | 1.61e-97 |
| GPT-4.1-nano [resolve_first]: P5 update vs capitulation | 494 | 99% | 61% | 191/3 | 9.69e-53 | 1.94e-52 |
| GPT-4.1-nano [resolve_first]: P6 update vs capitulation | 493 | 98% | 24% | 368/3 | 3.54e-105 | 4.6e-104 |
| GPT-4o-mini: P1 update vs capitulation | 525 | 91% | 8% | 448/9 | 1.21e-119 | 2.43e-118 |
| GPT-4o-mini: P2 update vs capitulation | 525 | 92% | 9% | 453/15 | 1.87e-113 | 2.99e-112 |
| GPT-4o-mini: P3 update vs capitulation | 525 | 94% | 10% | 447/8 | 9.37e-121 | 1.97e-119 |
| GPT-4o-mini: P5 update vs capitulation | 525 | 99% | 39% | 319/7 | 1.09e-84 | 6.53e-84 |
| GPT-4o-mini: P6 update vs capitulation | 524 | 94% | 7% | 460/4 | 8.07e-131 | 2.34e-129 |
| GPT-4o-mini [evidence_first]: P1 update vs capitulation | 519 | 84% | 2% | 435/5 | 9.57e-122 | 2.11e-120 |
| GPT-4o-mini [evidence_first]: P2 update vs capitulation | 519 | 70% | 0% | 364/1 | 9.74e-108 | 1.36e-106 |
| GPT-4o-mini [evidence_first]: P3 update vs capitulation | 519 | 76% | 0% | 396/1 | 2.47e-117 | 4.44e-116 |
| GPT-4o-mini [evidence_first]: P5 update vs capitulation | 519 | 93% | 4% | 466/4 | 1.33e-132 | 3.98e-131 |
| GPT-4o-mini [evidence_first]: P6 update vs capitulation | 518 | 88% | 3% | 444/2 | 1.1e-129 | 3.07e-128 |
| GPT-4o-mini [resolve_first]: P1 update vs capitulation | 522 | 90% | 3% | 460/7 | 4.9e-126 | 1.27e-124 |
| GPT-4o-mini [resolve_first]: P2 update vs capitulation | 522 | 88% | 3% | 453/8 | 1.63e-122 | 3.74e-121 |
| GPT-4o-mini [resolve_first]: P3 update vs capitulation | 522 | 88% | 2% | 452/6 | 3.38e-125 | 8.44e-124 |
| GPT-4o-mini [resolve_first]: P5 update vs capitulation | 522 | 95% | 7% | 469/11 | 4.56e-123 | 1.1e-121 |
| GPT-4o-mini [resolve_first]: P6 update vs capitulation | 521 | 87% | 2% | 445/3 | 4.12e-128 | 1.11e-126 |
| GPT-5-mini: P1 update vs capitulation | 594 | 98% | 2% | 571/2 | 1.06e-167 | 4.57e-166 |
| GPT-5-mini: P2 update vs capitulation | 594 | 95% | 6% | 533/5 | 8.27e-151 | 2.65e-149 |
| GPT-5-mini: P3 update vs capitulation | 594 | 99% | 5% | 557/1 | 1.18e-165 | 4.86e-164 |
| GPT-5-mini: P5 update vs capitulation | 594 | 98% | 16% | 490/3 | 1.56e-141 | 4.84e-140 |
| GPT-5-mini: P6 update vs capitulation | 593 | 95% | 7% | 528/3 | 7.1e-153 | 2.34e-151 |
| GPT-5-mini [evidence_first]: P1 update vs capitulation | 579 | 98% | 1% | 566/1 | 2.35e-168 | 1.06e-166 |
| GPT-5-mini [evidence_first]: P2 update vs capitulation | 580 | 95% | 1% | 546/0 | 8.68e-165 | 3.39e-163 |
| GPT-5-mini [evidence_first]: P3 update vs capitulation | 580 | 99% | 3% | 556/2 | 3.31e-163 | 1.19e-161 |
| GPT-5-mini [evidence_first]: P5 update vs capitulation | 580 | 99% | 10% | 516/1 | 2.41e-153 | 8.21e-152 |
| GPT-5-mini [evidence_first]: P6 update vs capitulation | 579 | 95% | 4% | 528/0 | 2.28e-159 | 7.97e-158 |
| GPT-5-mini [resolve_first]: P1 update vs capitulation | 586 | 98% | 1% | 570/4 | 1.46e-163 | 5.39e-162 |
| GPT-5-mini [resolve_first]: P2 update vs capitulation | 586 | 99% | 2% | 571/2 | 1.06e-167 | 4.57e-166 |
| GPT-5-mini [resolve_first]: P3 update vs capitulation | 586 | 99% | 2% | 572/4 | 3.7e-164 | 1.4e-162 |
| GPT-5-mini [resolve_first]: P5 update vs capitulation | 586 | 99% | 4% | 557/1 | 1.18e-165 | 4.86e-164 |
| GPT-5-mini [resolve_first]: P6 update vs capitulation | 585 | 98% | 2% | 557/0 | 4.24e-168 | 1.87e-166 |

## H3: is discrimination explained by accuracy?

Spearman rank correlation of baseline accuracy and J across 9 model conditions: **-0.43** (descriptive; n = models).

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4.1-nano: evidence_first vs default, capitulation P1 | 476 | 14% | 22% | 22/57 | 0.000103 | 0.00215 |
| GPT-4.1-nano: evidence_first vs default, update P1 | 62 | 45% | 52% | 6/10 | 0.454 | 1 |
| GPT-4.1-nano: evidence_first vs default, capitulation P2 | 476 | 39% | 73% | 9/169 | 2.22e-39 | 6.21e-38 |
| GPT-4.1-nano: evidence_first vs default, update P2 | 62 | 66% | 90% | 1/16 | 0.000275 | 0.00687 |
| GPT-4.1-nano: evidence_first vs default, capitulation P3 | 476 | 23% | 49% | 19/143 | 1.03e-24 | 2.79e-23 |
| GPT-4.1-nano: evidence_first vs default, update P3 | 62 | 60% | 79% | 3/15 | 0.00754 | 0.151 |
| GPT-4.1-nano: evidence_first vs default, capitulation P5 | 476 | 70% | 90% | 15/109 | 8.67e-19 | 2.17e-17 |
| GPT-4.1-nano: evidence_first vs default, update P5 | 62 | 92% | 98% | 1/5 | 0.219 | 1 |
| GPT-4.1-nano: evidence_first vs default, capitulation P6 | 475 | 23% | 27% | 25/45 | 0.0225 | 0.382 |
| GPT-4.1-nano: evidence_first vs default, update P6 | 62 | 66% | 77% | 4/11 | 0.118 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P1 | 457 | 19% | 21% | 38/48 | 0.332 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P1 | 58 | 52% | 45% | 9/5 | 0.424 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P2 | 457 | 72% | 72% | 53/56 | 0.848 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P2 | 58 | 88% | 90% | 5/6 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P3 | 457 | 52% | 48% | 73/57 | 0.188 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P3 | 58 | 81% | 79% | 8/7 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P5 | 457 | 89% | 89% | 28/31 | 0.795 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P5 | 58 | 98% | 98% | 1/1 | 1 | 1 |
| GPT-4.1-nano: resolve_first vs default, capitulation P6 | 456 | 26% | 26% | 35/37 | 0.906 | 1 |
| GPT-4.1-nano: resolve_first vs default, update P6 | 58 | 79% | 78% | 5/4 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, capitulation P1 | 505 | 1% | 6% | 2/25 | 5.65e-06 | 0.000124 |
| GPT-4o-mini: evidence_first vs default, update P1 | 96 | 5% | 22% | 2/18 | 0.000402 | 0.00966 |
| GPT-4o-mini: evidence_first vs default, capitulation P2 | 505 | 0% | 2% | 0/10 | 0.00195 | 0.0371 |
| GPT-4o-mini: evidence_first vs default, update P2 | 96 | 0% | 12% | 0/12 | 0.000488 | 0.0112 |
| GPT-4o-mini: evidence_first vs default, capitulation P3 | 505 | 0% | 15% | 1/73 | 7.94e-21 | 2.06e-19 |
| GPT-4o-mini: evidence_first vs default, update P3 | 96 | 1% | 46% | 0/43 | 2.27e-13 | 6.59e-12 |
| GPT-4o-mini: evidence_first vs default, capitulation P5 | 505 | 4% | 53% | 0/248 | 4.42e-75 | 1.33e-73 |
| GPT-4o-mini: evidence_first vs default, update P5 | 96 | 24% | 81% | 1/56 | 8.05e-16 | 2.41e-14 |
| GPT-4o-mini: evidence_first vs default, capitulation P6 | 504 | 1% | 7% | 0/27 | 1.49e-08 | 3.43e-07 |
| GPT-4o-mini: evidence_first vs default, update P6 | 96 | 28% | 55% | 0/26 | 2.98e-08 | 8.05e-07 |
| GPT-4o-mini: resolve_first vs default, capitulation P1 | 505 | 2% | 5% | 3/18 | 0.00149 | 0.0298 |
| GPT-4o-mini: resolve_first vs default, update P1 | 99 | 8% | 20% | 1/13 | 0.00183 | 0.0403 |
| GPT-4o-mini: resolve_first vs default, capitulation P2 | 505 | 1% | 2% | 4/7 | 0.549 | 1 |
| GPT-4o-mini: resolve_first vs default, update P2 | 99 | 6% | 11% | 3/8 | 0.227 | 1 |
| GPT-4o-mini: resolve_first vs default, capitulation P3 | 505 | 3% | 15% | 2/61 | 4.37e-16 | 1.05e-14 |
| GPT-4o-mini: resolve_first vs default, update P3 | 99 | 13% | 44% | 3/34 | 1.23e-07 | 3.21e-06 |
| GPT-4o-mini: resolve_first vs default, capitulation P5 | 505 | 15% | 53% | 5/197 | 8.51e-52 | 2.47e-50 |
| GPT-4o-mini: resolve_first vs default, update P5 | 99 | 48% | 83% | 3/37 | 1.95e-08 | 5.45e-07 |
| GPT-4o-mini: resolve_first vs default, capitulation P6 | 504 | 4% | 7% | 8/23 | 0.0107 | 0.192 |
| GPT-4o-mini: resolve_first vs default, update P6 | 99 | 41% | 57% | 6/21 | 0.00592 | 0.124 |
| GPT-5-mini: evidence_first vs default, capitulation P1 | 561 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-5-mini: evidence_first vs default, update P1 | 21 | 14% | 0% | 3/0 | 0.25 | 1 |
| GPT-5-mini: evidence_first vs default, capitulation P2 | 561 | 0% | 1% | 2/4 | 0.688 | 1 |
| GPT-5-mini: evidence_first vs default, update P2 | 21 | 0% | 5% | 0/1 | 1 | 1 |
| GPT-5-mini: evidence_first vs default, capitulation P3 | 561 | 1% | 2% | 0/5 | 0.0625 | 1 |
| GPT-5-mini: evidence_first vs default, update P3 | 21 | 14% | 10% | 1/0 | 1 | 1 |
| GPT-5-mini: evidence_first vs default, capitulation P5 | 561 | 4% | 5% | 13/20 | 0.296 | 1 |
| GPT-5-mini: evidence_first vs default, update P5 | 21 | 14% | 19% | 1/2 | 1 | 1 |
| GPT-5-mini: evidence_first vs default, capitulation P6 | 560 | 1% | 2% | 2/7 | 0.18 | 1 |
| GPT-5-mini: evidence_first vs default, update P6 | 21 | 10% | 14% | 1/2 | 1 | 1 |
| GPT-5-mini: resolve_first vs default, capitulation P1 | 564 | 0% | 0% | 2/0 | 0.5 | 1 |
| GPT-5-mini: resolve_first vs default, update P1 | 22 | 5% | 5% | 1/1 | 1 | 1 |
| GPT-5-mini: resolve_first vs default, capitulation P2 | 564 | 1% | 1% | 5/3 | 0.727 | 1 |
| GPT-5-mini: resolve_first vs default, update P2 | 22 | 9% | 5% | 2/1 | 1 | 1 |
| GPT-5-mini: resolve_first vs default, capitulation P3 | 564 | 1% | 2% | 5/7 | 0.774 | 1 |
| GPT-5-mini: resolve_first vs default, update P3 | 22 | 14% | 5% | 2/0 | 0.5 | 1 |
| GPT-5-mini: resolve_first vs default, capitulation P5 | 564 | 3% | 5% | 13/24 | 0.0989 | 1 |
| GPT-5-mini: resolve_first vs default, update P5 | 22 | 18% | 14% | 3/2 | 1 | 1 |
| GPT-5-mini: resolve_first vs default, capitulation P6 | 563 | 1% | 2% | 3/8 | 0.227 | 1 |
| GPT-5-mini: resolve_first vs default, update P6 | 22 | 9% | 14% | 0/1 | 1 | 1 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 3% (2%–4%) |
| P1 | followup | 1 | 10% (9%–12%) |
| P1 | followup | 2 | 9% (7%–10%) |
| P1 | preemptive | 0 | 7% (6%–8%) |
| P1 | preemptive | 1 | 12% (10%–13%) |
| P1 | preemptive | 2 | 4% (3%–5%) |
| P1 | prefilled | 0 | 3% (2%–4%) |
| P1 | prefilled | 1 | 10% (9%–12%) |
| P1 | prefilled | 2 | 7% (6%–8%) |
| P2 | followup | 0 | 12% (11%–14%) |
| P2 | followup | 1 | 21% (19%–23%) |
| P2 | followup | 2 | 27% (25%–29%) |
| P2 | preemptive | 0 | 7% (6%–8%) |
| P2 | preemptive | 1 | 15% (13%–17%) |
| P2 | preemptive | 2 | 11% (10%–13%) |
| P2 | prefilled | 0 | 7% (6%–8%) |
| P2 | prefilled | 1 | 17% (15%–19%) |
| P2 | prefilled | 2 | 25% (23%–27%) |
| P3 | followup | 0 | 12% (11%–14%) |
| P3 | followup | 1 | 23% (21%–25%) |
| P3 | followup | 2 | 14% (12%–16%) |
| P3 | preemptive | 0 | 7% (6%–9%) |
| P3 | preemptive | 1 | 11% (9%–12%) |
| P3 | preemptive | 2 | 16% (14%–17%) |
| P3 | prefilled | 0 | 11% (10%–13%) |
| P3 | prefilled | 1 | 14% (12%–16%) |
| P3 | prefilled | 2 | 9% (8%–10%) |
| P5 | followup | 0 | 37% (35%–40%) |
| P5 | followup | 1 | 32% (30%–34%) |
| P5 | followup | 2 | 39% (36%–41%) |
| P5 | preemptive | 0 | 22% (20%–24%) |
| P5 | preemptive | 1 | 9% (8%–11%) |
| P5 | preemptive | 2 | 12% (10%–13%) |
| P5 | prefilled | 0 | 37% (35%–40%) |
| P5 | prefilled | 1 | 19% (17%–21%) |
| P5 | prefilled | 2 | 28% (26%–30%) |
| P6 | followup | 0 | 5% (4%–6%) |
| P6 | followup | 1 | 21% (19%–23%) |
| P6 | followup | 2 | 5% (4%–7%) |
| P6 | preemptive | 0 | 17% (15%–19%) |
| P6 | preemptive | 1 | 53% (50%–55%) |
| P6 | preemptive | 2 | 21% (19%–23%) |
| P6 | prefilled | 0 | 5% (4%–7%) |
| P6 | prefilled | 1 | 25% (23%–27%) |
| P6 | prefilled | 2 | 3% (3%–4%) |
