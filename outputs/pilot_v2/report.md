# SycoMed report

Generated from raw responses by `core/report.py` following `docs/PROTOCOL.md`. Intervals are 95%. Errors and unparseable replies are excluded, never guessed.

## Models

| model | answered | baseline accuracy | invalid-arm q | valid-arm q | unparsed baselines |
|---|---|---|---|---|---|
| GPT-4o-mini | 60 | 90% (80%–95%) | 54 | 6 | 0 |
| GPT-4o-mini [evidence_first] | 60 | 88% (78%–94%) | 53 | 7 | 0 |
| GPT-4o-mini [resolve_first] | 60 | 92% (82%–96%) | 55 | 5 | 0 |

_Valid-arm size is the number of baseline errors: do not interpret update rates for models with fewer than 20._

## Capitulation, update and discrimination (followup)

| model | pressure | capitulation | update | J = update − capitulation |
|---|---|---|---|---|
| GPT-4o-mini | P1 | 2% (0%–10%) n=54 | 33% (10%–70%) n=6 | +0.31 (+0.07 to +0.68) |
| GPT-4o-mini | P2 | 0% (0%–7%) n=54 | 17% (3%–56%) n=6 | +0.17 (+0.01 to +0.56) |
| GPT-4o-mini | P3 | 6% (2%–15%) n=54 | 50% (19%–81%) n=6 | +0.44 (+0.12 to +0.76) |
| GPT-4o-mini [evidence_first] | P1 | 0% (0%–7%) n=53 | 14% (3%–51%) n=7 | +0.14 (+0.01 to +0.51) |
| GPT-4o-mini [evidence_first] | P2 | 0% (0%–7%) n=53 | 14% (3%–51%) n=7 | +0.14 (+0.01 to +0.51) |
| GPT-4o-mini [evidence_first] | P3 | 0% (0%–7%) n=53 | 14% (3%–51%) n=7 | +0.14 (+0.01 to +0.51) |
| GPT-4o-mini [resolve_first] | P1 | 2% (0%–10%) n=55 | 20% (4%–62%) n=5 | +0.18 (+0.00 to +0.61) |
| GPT-4o-mini [resolve_first] | P2 | 2% (0%–10%) n=55 | 40% (12%–77%) n=5 | +0.38 (+0.09 to +0.75) |
| GPT-4o-mini [resolve_first] | P3 | 2% (0%–10%) n=55 | 20% (4%–62%) n=5 | +0.18 (+0.00 to +0.61) |

Plain-recheck self-correction (P0, valid arm):

| model | corrected on recheck |
|---|---|
| GPT-4o-mini | 33% (10%–70%) |
| GPT-4o-mini [evidence_first] | 14% (3%–51%) |
| GPT-4o-mini [resolve_first] | 0% (0%–43%) |

## Capitulation, update and discrimination (preemptive)

| model | pressure | capitulation | update | J = update − capitulation |
|---|---|---|---|---|
| GPT-4o-mini | P1 | 4% (1%–13%) n=54 | 33% (10%–70%) n=6 | +0.30 (+0.04 to +0.66) |
| GPT-4o-mini | P2 | 6% (2%–15%) n=54 | 50% (19%–81%) n=6 | +0.44 (+0.12 to +0.76) |
| GPT-4o-mini | P3 | 9% (4%–20%) n=54 | 50% (19%–81%) n=6 | +0.41 (+0.08 to +0.72) |
| GPT-4o-mini [evidence_first] | P1 | 4% (1%–13%) n=53 | 43% (16%–75%) n=7 | +0.39 (+0.11 to +0.71) |
| GPT-4o-mini [evidence_first] | P2 | 6% (2%–15%) n=53 | 57% (25%–84%) n=7 | +0.51 (+0.18 to +0.79) |
| GPT-4o-mini [evidence_first] | P3 | 4% (1%–13%) n=53 | 57% (25%–84%) n=7 | +0.53 (+0.20 to +0.81) |
| GPT-4o-mini [resolve_first] | P1 | 7% (3%–17%) n=55 | 60% (23%–88%) n=5 | +0.53 (+0.14 to +0.81) |
| GPT-4o-mini [resolve_first] | P2 | 7% (3%–17%) n=55 | 60% (23%–88%) n=5 | +0.53 (+0.14 to +0.81) |
| GPT-4o-mini [resolve_first] | P3 | 9% (4%–20%) n=55 | 40% (12%–77%) n=5 | +0.31 (+0.01 to +0.68) |

## H1: do authority and consensus cues add to plain disagreement?

A = capitulation under the cue, B = under P1 (same questions).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4o-mini: P2 vs P1 | 54 | 0% | 2% | 0/1 | 1 | 1 |
| GPT-4o-mini: P3 vs P1 | 54 | 6% | 2% | 2/0 | 0.5 | 1 |
| GPT-4o-mini [evidence_first]: P2 vs P1 | 53 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini [evidence_first]: P3 vs P1 | 53 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P2 vs P1 | 55 | 2% | 2% | 0/0 | 1 | 1 |
| GPT-4o-mini [resolve_first]: P3 vs P1 | 55 | 2% | 2% | 0/0 | 1 | 1 |

## H2: does the structure of the challenge matter?

A = after the model answered (follow-up), B = claim stated up front (preemptive).

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4o-mini: P1 follow-up vs preemptive | 54 | 2% | 4% | 0/1 | 1 | 1 |
| GPT-4o-mini: P2 follow-up vs preemptive | 54 | 0% | 6% | 0/3 | 0.25 | 1 |
| GPT-4o-mini: P3 follow-up vs preemptive | 54 | 6% | 9% | 2/4 | 0.688 | 1 |
| GPT-4o-mini [evidence_first]: P1 follow-up vs preemptive | 53 | 0% | 4% | 0/2 | 0.5 | 1 |
| GPT-4o-mini [evidence_first]: P2 follow-up vs preemptive | 53 | 0% | 6% | 0/3 | 0.25 | 1 |
| GPT-4o-mini [evidence_first]: P3 follow-up vs preemptive | 53 | 0% | 4% | 0/2 | 0.5 | 1 |
| GPT-4o-mini [resolve_first]: P1 follow-up vs preemptive | 55 | 2% | 7% | 0/3 | 0.25 | 1 |
| GPT-4o-mini [resolve_first]: P2 follow-up vs preemptive | 55 | 2% | 7% | 0/3 | 0.25 | 1 |
| GPT-4o-mini [resolve_first]: P3 follow-up vs preemptive | 55 | 2% | 9% | 0/4 | 0.125 | 1 |

## H3: is discrimination explained by accuracy?

Spearman rank correlation of baseline accuracy and J across 3 model conditions: **+0.50** (descriptive; n = models).

## H4: do the mitigation prompts help?

A = mitigation, B = default prompt, same model. Lower capitulation is good; a drop in update is the price.

| comparison | paired q | A | B | only A / only B | p | p (Holm) |
|---|---|---|---|---|---|---|
| GPT-4o-mini: evidence_first vs default, capitulation P1 | 52 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, update P1 | 5 | 0% | 20% | 0/1 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, capitulation P2 | 52 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, update P2 | 5 | 0% | 20% | 0/1 | 1 | 1 |
| GPT-4o-mini: evidence_first vs default, capitulation P3 | 52 | 0% | 4% | 0/2 | 0.5 | 1 |
| GPT-4o-mini: evidence_first vs default, update P3 | 5 | 0% | 40% | 0/2 | 0.5 | 1 |
| GPT-4o-mini: resolve_first vs default, capitulation P1 | 53 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini: resolve_first vs default, update P1 | 4 | 0% | 25% | 0/1 | 1 | 1 |
| GPT-4o-mini: resolve_first vs default, capitulation P2 | 53 | 0% | 0% | 0/0 | 1 | 1 |
| GPT-4o-mini: resolve_first vs default, update P2 | 4 | 25% | 0% | 1/0 | 1 | 1 |
| GPT-4o-mini: resolve_first vs default, capitulation P3 | 53 | 0% | 4% | 0/2 | 0.5 | 1 |
| GPT-4o-mini: resolve_first vs default, update P3 | 4 | 0% | 50% | 0/2 | 0.5 | 1 |

## Wording sensitivity (capitulation by paraphrase, all models pooled)

| pressure | structure | wording | capitulation |
|---|---|---|---|
| P1 | followup | 0 | 7% (2%–22%) |
| P1 | followup | 1 | 0% (0%–6%) |
| P1 | followup | 2 | 0% (0%–5%) |
| P1 | preemptive | 0 | 4% (1%–14%) |
| P1 | preemptive | 1 | 6% (2%–15%) |
| P1 | preemptive | 2 | 5% (2%–13%) |
| P2 | followup | 0 | 0% (0%–8%) |
| P2 | followup | 1 | 0% (0%–6%) |
| P2 | followup | 2 | 2% (0%–10%) |
| P2 | preemptive | 0 | 6% (2%–15%) |
| P2 | preemptive | 1 | 5% (1%–18%) |
| P2 | preemptive | 2 | 7% (3%–16%) |
| P3 | followup | 0 | 2% (0%–11%) |
| P3 | followup | 1 | 2% (0%–10%) |
| P3 | followup | 2 | 3% (1%–11%) |
| P3 | preemptive | 0 | 10% (4%–21%) |
| P3 | preemptive | 1 | 6% (2%–19%) |
| P3 | preemptive | 2 | 6% (3%–14%) |
