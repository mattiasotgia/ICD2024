# International Cosmic Day — analysis tool (Voilà)

A two-tab web app for a cosmic-ray outreach activity:

* **Counting analysis** — enter (value, count) pairs, plot a histogram, fit
  a model to it (Gaussian / Moyal-Landau / Poisson presets).
* **Angular analysis** — enter (angle, count) pairs plus the number of
  individual measurements per angle and the angular uncertainty, plot
  counts vs. angle with error bars, fit `I0 * cos(theta)^n`.

Both tabs share the same layout: a data-entry column, a plot column, and a
column with a short explanation on top and a running log (messages + fit
results) on the bottom.

## Files

- `app.ipynb` — the notebook that Voilà renders as the web app. Cells:
  1. imports + Matplotlib style
  2. deployment switch (`ENABLE_FAKE_DATA`) + the `TEXTS` dictionary
  3. editable-table widget, logger, fit helpers, `FUNCTION_LIBRARY`
  4. `plot_counts` / `plot_angular`
  5. `build_analysis_tab` (shared by both tabs)
  6. final assembly (header, logos, tabs)
- `requirements.txt` — Python dependencies.
- `bin/` — the two header logos (`infn-ocra.png`, `unige.jpg`). The copies
  in this folder are 1×1 placeholders — replace them with your real logos
  before deploying (see `bin/README_LOGOS.txt`). The app also runs fine
  without this folder: a missing logo silently falls back to a tiny
  transparent placeholder instead of crashing.

## Run locally

```bash
pip install -r requirements.txt
voila app.ipynb
```

This opens the app in your browser with the code hidden — only the
widgets are shown. To edit/inspect the logic, open it as a normal notebook
with `jupyter notebook app.ipynb` (or `jupyter lab`).

## Run on Binder

1. Push this folder (`app.ipynb`, `requirements.txt`, `bin/`) to a GitHub
   repo.
2. Point Binder at your repo with the **URL to open** set to
   `voila/render/app.ipynb`, or use a link of the form:

   ```
   https://mybinder.org/v2/gh/<user>/<repo>/<branch>?urlpath=voila%2Frender%2Fapp.ipynb
   ```

3. Optional badge:

   ```markdown
   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/<branch>?urlpath=voila%2Frender%2Fapp.ipynb)
   ```

## New in this version

- **Fake-data injection**: each tab has a 🎲 **Fake data** button that
  fills the table with simulated data — Poisson-noised counts built from
  the function currently selected in the drop-down (for the angular tab,
  the "true" curve is the selected `I0*cos^n(theta)`-type formula; for the
  counting tab it's whichever preset — Gaussian, Moyal, Poisson — is
  selected) — and immediately plots it. **Set `ENABLE_FAKE_DATA = False`**
  in cell 2 before deploying for the real event to remove this button from
  both tabs entirely.
  - To give a function its own fake-data profile, add `fake_x` (the
    x-values to simulate at) and `fake_params` (comma-separated "true"
    parameters) to its entry in `FUNCTION_LIBRARY`.
- **1σ uncertainty band**: after a fit, a shaded band showing the fit's
  ±1σ uncertainty (propagated from the fit's covariance matrix via a
  numerical Jacobian — `fit_uncertainty_band()`) is drawn around the curve.
  A **"Show 1σ band"** checkbox next to the fit controls toggles it on/off
  instantly, without needing to re-fit.
- **Download buttons**: **⬇ PDF** and **⬇ JPG** buttons (enabled once a
  plot exists) export the current figure at high resolution (600 dpi).
  Clicking triggers a browser download automatically; if the browser
  blocks the auto-click, a plain link appears in the log to click manually.
- **Centralized text**: every user-facing string (labels, button text,
  tooltips, log messages, the two explanatory panels, titles) lives in the
  single `TEXTS` dictionary in cell 2 — edit it there rather than hunting
  through the widget-building code.

## Customising

- **Explanatory text / all labels & messages**: edit the `TEXTS`
  dictionary (cell 2).
- **Fit function**: each tab has a `Function` drop-down of presets, a
  LaTeX rendering of the chosen formula, and a `f(x,p) =` text field that
  is pre-filled from the preset but stays fully editable — write any model
  as a function of `x` and parameters `p0, p1, p2, ...` (numpy as `np`,
  plus bare `exp`/`cos`/`sin`/`round`, and `norm`/`poisson`/`moyal` from
  `scipy.stats`), plus an `Init. params` field with comma-separated
  starting values. This is meant for a presenter/demonstrator with trusted
  input, not an anonymous public form, since the expression is evaluated
  with `eval` (only the names above, no builtins).
- **Adding a new function**: add one entry to `FUNCTION_LIBRARY["count"]`
  or `["angular"]` (cell 3) — label, `expr`, `init`, `latex`, and
  optionally `fake_x` / `fake_params` for the fake-data button.
  - The "Moyal" preset is a standard analytic approximation to the Landau
    distribution (SciPy has no native Landau).
- **Table size**: `n_init` in `EditableTable(...)` sets the starting
  number of rows; visitors can add/remove rows regardless.
- **Plot style**: the `PlotStyle` dict + `cycler` import in cell 1 control
  colors/fonts/ticks globally via `plt.style.use(PlotStyle)`.

## Notes

- Pressing **Fit** before **Plot** shows an error in the log rather than
  fitting. Re-fitting replaces the previous fit line/band rather than
  stacking new ones.
- The log panel shows the newest message at the top, so older ones scroll
  out of view instead of being pushed down.
- The counting histogram uses bins of width 1 spanning the full min–max
  range of the values entered; any integer value without a row is shown
  with count 0.
- The layout tries to use the full height of the browser window; exact
  behaviour can depend a little on the Voila template/version.
- Download buttons use the standard Jupyter/Voila trick of an auto-clicked
  hidden link, since Voila has no native "save file" dialog.
