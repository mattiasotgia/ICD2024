import numpy as np
import pandas as pd
import plotly.graph_objects as go

import ipywidgets as widgets
import ipysheet

from IPython.display import display

from .analysis import Analysis

class Interface:
    def __init__(self):
        self.analysis = Analysis()

        self.mode = widgets.ToggleButtons(
            options=["Angular", "Count"],
            description="Mode:"
        )

        self.output_plot = widgets.Output()

        self._build_widgets()
        self._layout()

        self.mode.observe(self._on_mode_change, names='value')

    # -------------------------
    # WIDGET SETUP
    # -------------------------
    def _build_widgets(self):
        self._build_table()
        
        self.add_row_btn = widgets.Button(description="Add Row")
        self.add_row_btn.on_click(self._add_row)

        self.fill_x_err_btn = widgets.Button(description="Auto X Error")
        self.fill_x_err_btn.on_click(self._fill_x_err)

        self.fill_y_err_btn = widgets.Button(description="Auto Y Error")
        self.fill_y_err_btn.on_click(self._fill_y_err)

        self.plot_btn = widgets.Button(description="Update Plot")
        self.plot_btn.on_click(self._update_plot)

        self.download_btn = widgets.Button(description="Download Plot")
        self.download_btn.on_click(self._download_plot)

        self.sidebar = widgets.HTML(
            "<h3>Analysis Tool</h3><p>Insert your description here.</p>"
        )

    def _build_table(self):
        if self.mode.value == "Angular":
            angles = np.arange(0, 91, 15)

            self.df = pd.DataFrame({
                "angle": angles,
                "count": np.zeros(len(angles)),
                "angle_err": np.zeros(len(angles)),
                "count_err": np.zeros(len(angles)),
            })

        else:
            self.df = pd.DataFrame({
                "bin": [],
                "count": []
            })

        self._create_sheet_from_df()

    def _create_sheet_from_df(self):
        rows, cols = self.df.shape

        self.sheet = ipysheet.sheet(rows=rows, columns=cols)

        self.cells = {}

        for j, col in enumerate(self.df.columns):
            cell = ipysheet.column(
                j,
                self.df[col].tolist(),
                label=col
            )
            self.cells[col] = cell

        # 🔴 IMPORTANT: explicitly attach cells to sheet
        self.sheet.cells = list(self.cells.values())
    
    def _get_df_from_sheet(self):
        data = {}
        for col, cell in self.cells.items():
            data[col] = cell.value

        return pd.DataFrame(data)

    # -------------------------
    # CALLBACKS
    # -------------------------
    def _on_mode_change(self, change):
        self._build_table()
        self._refresh_layout()

    def _add_row(self, b):
        df = self._get_df_from_sheet()

        new_row = {col: 0 for col in df.columns}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        self.df = df
        self._create_sheet_from_df()
        self._refresh_layout()

    def _fill_x_err(self, b):
        df = self._get_df_from_sheet()
        self.analysis.set_data(df)
        self.analysis.compute_x_error()

        self.df = self.analysis.data
        self._create_sheet_from_df()
        self._refresh_layout()

    def _fill_y_err(self, b):
        df = self._get_df_from_sheet()
        self.analysis.set_data(df)
        self.analysis.compute_y_error()

        self.df = self.analysis.data
        self._create_sheet_from_df()
        self._refresh_layout()

    def _update_plot(self, b):
        df = self._get_df_from_sheet()
        self.analysis.set_data(df)

        with self.output_plot:
            self.output_plot.clear_output()

            if self.mode.value == "Angular":
                fig = self.analysis.plot_angular()
            else:
                fig = self.analysis.plot_counts()

            fig.show()

        self.current_fig = fig

    def _download_plot(self, b):
        if hasattr(self, "current_fig"):
            self.current_fig.write_image("plot.png")

    # -------------------------
    # LAYOUT
    # -------------------------
    def _layout(self):
        self.controls = widgets.VBox([
            self.mode,
            self.add_row_btn,
            self.fill_x_err_btn,
            self.fill_y_err_btn,
            self.plot_btn,
            self.download_btn
        ])

        self.main = widgets.VBox([
            self.sheet,
            self.output_plot
        ])

        self.ui = widgets.HBox([
            self.sidebar,
            widgets.VBox([self.controls, self.main])
        ])

    def _refresh_layout(self):
        self.main.children = [self.sheet, self.output_plot]

    def display(self):
        display(self.ui)