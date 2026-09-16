import numpy as np
import pandas as pd
import plotly.graph_objects as go

import ipywidgets as widgets
from ipyaggrid import Grid

from IPython.display import display


class Analysis:
    def __init__(self):
        self.data = pd.DataFrame()

    # -------------------------
    # DATA HANDLING
    # -------------------------
    def set_data(self, df):
        self.data = df.copy()

    # -------------------------
    # ERROR MODELS
    # -------------------------
    def compute_x_error(self):
        if "angle" in self.data:
            self.data["angle_err"] = np.full(len(self.data), 1.0)  # example

    def compute_y_error(self):
        if "count" in self.data:
            self.data["count_err"] = np.sqrt(self.data["count"])

    # -------------------------
    # PLOTTING
    # -------------------------
    def plot_angular(self):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.data["angle"],
            y=self.data["count"],
            error_x=dict(array=self.data.get("angle_err", None)),
            error_y=dict(array=self.data.get("count_err", None)),
            mode='markers'
        ))

        fig.update_layout(
            title="Angular Analysis",
            xaxis_title="Angle",
            yaxis_title="Counts"
        )

        return fig

    def plot_counts(self):
        fig = go.Figure()


        fig.add_trace(go.Bar(
            x=self.data["bin"],
            y=self.data["count"]
        ))

        fig.update_layout(
            title="Count Analysis",
            xaxis_title="Bin",
            yaxis_title="Counts"
        )

        return fig