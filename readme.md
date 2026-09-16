# Outreach analysis tool (Voilà)

A small two-tab web app for a public-outreach lab activity:

* **Counting analysis** — enter (value, count) pairs, plot a histogram, fit
  a model to it (Gaussian by default).
* **Angular analysis** — enter (angle, count) pairs plus the number of
  individual measurements per angle and the angular uncertainty, plot the
  rate vs. angle with error bars, fit a model to it.

Both tabs share the same layout: a data-entry column, a plot column, and a
column with a short explanation on top and a running log (messages + fit
results) on the bottom.

## Files

- `app.ipynb` — the notebook that Voilà renders as the web app. All the
  logic (editable table, plotting, fitting) lives here, organised in a few
  cells: setup, explanatory texts, the editable-table/log helpers, the
  plotting functions, the shared tab builder, and the final assembly.
- `requirements.txt` — Python dependencies.

## Run locally

```bash
pip install -r requirements.txt
voila app.ipynb
```

This opens the app in your browser with the code hidden — only the
widgets are shown.

If you just want to edit/inspect the logic first, open it as a normal
notebook with `jupyter notebook app.ipynb` (or `jupyter lab`).

## Run on Binder

Run here [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mattiasotgia/ICD2024/main?urlpath=voila%2Frender%2Fapp.ipynb)

1. Push this folder (`app.ipynb` + `requirements.txt`) to a GitHub repo.
2. Go to <https://mybinder.org>, point it at your repo, and set the
   **URL to open** (under "Launch" / "advanced options") to:

   ```
   voila/render/app.ipynb
   ```

   or use a Binder link of the form:

   ```
   https://mybinder.org/v2/gh/<user>/<repo>/<branch>?urlpath=voila%2Frender%2Fapp.ipynb
   ```

3. Optionally add a badge to your repo's README:

   ```markdown
   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/<branch>?urlpath=voila%2Frender%2Fapp.ipynb)
   ```

## Customising

- **Explanatory text**: edit `COUNT_STD_TEXT` / `ANGULAR_STD_TEXT` (second
  cell) — plain HTML.
- **Fit function**: each tab has a `Function` drop-down of presets, a
  LaTeX rendering of the chosen formula, and a `f(x,p) =` text field that
  is pre-filled from the preset but stays fully editable — write any
  model as a function of `x` and parameters `p0, p1, p2, ...` (numpy
  available as `np`, plus `norm`, `poisson`, `moyal` from `scipy.stats`),
  plus an `Init. params` field with comma-separated starting values. This
  is meant to be run by a presenter/demonstrator with trusted input, not
  exposed to arbitrary anonymous internet users, since the expression is
  evaluated with `eval` (only the names above, no builtins).
- **Adding a new function to a drop-down**: add one entry to
  `FUNCTION_LIBRARY["count"]` or `FUNCTION_LIBRARY["angular"]` (third
  cell) — a label, an `expr`, a comma-separated `init`, and a `latex`
  string. Nothing else needs to change.
  - The "Landau" preset actually uses `scipy.stats.moyal`, a standard
    analytic approximation to the Landau distribution (SciPy has no
    native Landau).
- **Table size**: `n_init` in `EditableTable(...)` sets the number of rows
  shown at start; visitors can add/remove rows with the `+ row` / `x`
  buttons regardless.
- **Angular errors**: currently Poisson (`sqrt(count)/N`, floored at 1
  count) on the rate and a constant user-supplied error on the angle —
  adjust `plot_angular()` if you need a different convention.
- **Angular model**: the two presets are `I0*cos(theta)` (pick this if
  column 1 holds `theta`) and `I0*x` (pick this if column 1 already holds
  `cos(theta)`) — choose the one matching how you filled in the table.

## Notes

- Pressing **Fit** before **Plot** (or after changing the data without
  re-plotting) shows an error message in the log panel rather than
  fitting.
- The fit line is overlaid on the existing plot; re-fitting replaces the
  previous fit line rather than stacking new ones.
- The log panel shows the newest message at the top, so older ones
  scroll out of view instead of pushing new ones down.
- The counting histogram always uses bins of width 1 spanning the full
  min–max range of the values you entered; any integer value you didn't
  give a row for is shown with count 0.
- The layout tries to use the full height of the browser window (flexible
  columns, scrolling table/log panels) rather than fixed pixel heights;
  exact behaviour can depend a little on the Voila template/version.
