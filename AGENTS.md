# AGENTS.md

## Project

**Fuzzy Guard** — a Flask + `scikit-fuzzy` email spam detector.

The UI is bilingual (English / Serbian). Code identifiers, comments and API
fields are Serbian. Do not Anglicize them.

## Academic context

This is coursework for **"Fazi logički sistemi i neuronske mreže"** (Master's),
and it is defended orally in front of the professor. Every design decision must
be explainable out loud.

- Membership functions MUST be triangular (`trimf`) or trapezoidal (`trapmf`).
  These are the two shapes taught in the course. No sigmoids, gaussians, bells
  or ad-hoc piecewise ramps.
- The spam score MUST come from fuzzy inference only (Mamdani + centroid
  defuzzification). Never add hand-weighted linear terms, magic multipliers or
  machine-learning components to the score. If a value cannot be traced back to
  a membership function, it does not belong in the score pipeline.
- The category MUST be derived from the same defuzzified value that is shown to
  the user. Do not hand-pick score thresholds.
- Never tune constants against the validation set. Be explicit about which
  emails were used for calibration.
- Every numeric constant in `fazi/skupovi.py` needs a comment explaining where
  it comes from (measurement, literature, or a design constraint). These will be
  questioned during the defense.
- When a limitation exists (for example, two different emails producing the same
  score), document it honestly instead of hiding it with a hack.

## Non-negotiable naming rule

**NEVER truncate the fuzzy identifiers.** No single-letter abbreviations and no
short aliases, not even as locals at the top of a function.

| NEVER write | ALWAYS write    |
| ----------- | --------------- |
| `k`         | `kljucne_reci`  |
| `l`         | `broj_linkova`  |
| `c`         | `caps_procenat` |
| `i`         | `interpunkcija` |

This applies everywhere, including inside `kontroler_spam_score`:

```python
# WRONG
k = mu["kljucne_reci"]
k["zanemarljive"]

# RIGHT
kljucne_reci = mu["kljucne_reci"]
kljucne_reci["zanemarljive"]
```

The same rule applies to membership-set names: write `caps_blago_povisen`, never
`caps_blago`; write `interpunkcija_umerena`, never `i["umerena"]`.

## Rule-base conventions

- Every rule is a tuple `(naziv, jacina, izlazni_skup, kategorija)`.
- Fuzzy AND is `min(...)`; fuzzy OR is `max(...)`.
- Every rule must add information. Delete a rule whose antecedent is a subset of
  another rule's antecedent when both have the same output set. (This is why
  `p15` was removed: `p12` already covers it via `max(...)`.)
- Expose per-rule activation strengths so tests can assert on them.

## Scoring invariants (enforced by tests)

1. `spam_score` stays inside `[0, 100]`.
2. `kategorija` always agrees with the category implied by `spam_score`.
3. No point of the input grid may leave the rule base with zero activated rules.
4. Two different feature vectors must not collapse to the same score unless the
   fuzzy sets genuinely cannot distinguish them.
5. Raising the cap percentage past 35% must not lower the score. (Regression for
   the old caps hole between `caps_poviseni` and `caps_agresivan`.)

## Neural network component

The course covers fuzzy systems **and** neural networks, so the project must
include a neural-network part.

- Keep the fuzzy system interpretable. The network must never turn the fuzzy
  rules into a black box; it may tune parameters or act as a second opinion.
- Any network work requires a real, labelled dataset. `primeri.txt` is **not**
  labelled — its `[EN]` / `[SR]` tags are language, not class. Do not train on
  unlabelled data.
- Never report accuracy on data used for tuning. Always report a held-out
  validation/test split with a confusion matrix, precision, recall and F1.
- Compare against the fuzzy system on identical features so the comparison is
  fair.
- State clearly which language the trained model covers. Serbian stays
  rule-based unless a labelled Serbian set exists.
- Document the architecture, hyperparameters and training procedure.

## Workflow

- Run `python -m pytest` before finishing.
- Update `README.md` whenever scores, membership sets or rules change.
- Keep the `primeri.txt` format: `[EN]` / `[SR]` tag on the first line, body
  after it, blocks separated by `---`.
