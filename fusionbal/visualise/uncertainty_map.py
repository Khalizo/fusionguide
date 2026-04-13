"""2D uncertainty heatmap: dose_dpa vs irradiation_temperature_C."""
from __future__ import annotations
import numpy as np


def plot_uncertainty_map(
    campaign,
    n_dose: int = 20,
    n_temp: int = 20,
    dose_range: tuple[float, float] = (0.1, 30.0),
    temp_range: tuple[float, float] = (200, 700),
    output_path: str | None = None,
):
    """Generate a 2D heatmap of predicted uncertainty over the parameter space."""
    import pandas as pd
    import plotly.graph_objects as go

    dose_vals = np.linspace(dose_range[0], dose_range[1], n_dose)
    temp_vals = np.linspace(temp_range[0], temp_range[1], n_temp)

    Z = np.zeros((n_temp, n_dose))
    inner_campaign = getattr(campaign, "_campaign", None)
    measurements = getattr(inner_campaign, "measurements", None)

    for i, t in enumerate(temp_vals):
        for j, d in enumerate(dose_vals):
            nearby = 0
            if measurements is not None and len(measurements) > 0:
                dose_col = measurements.get("dose_dpa", pd.Series(dtype=float))
                temp_col = measurements.get("irradiation_temperature_C", pd.Series(dtype=float))
                nearby = int(((dose_col - d).abs() < 2.0) & ((temp_col - t).abs() < 100).sum())
            Z[i, j] = np.sqrt(d) / (1.0 + nearby)

    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=dose_vals.tolist(),
        y=temp_vals.tolist(),
        colorscale="Viridis",
        colorbar={"title": "Uncertainty (proxy)"},
    ))

    if measurements is not None and len(measurements) > 0:
        measured_doses = measurements.get("dose_dpa", pd.Series()).tolist()
        measured_temps = measurements.get("irradiation_temperature_C", pd.Series()).tolist()
        fig.add_scatter(
            x=measured_doses,
            y=measured_temps,
            mode="markers",
            marker={"size": 10, "color": "white", "symbol": "x"},
            name="Measured",
        )

    fig.update_layout(
        title="Uncertainty Map — Dose vs Temperature",
        xaxis_title="Dose (dpa)",
        yaxis_title="Irradiation Temperature (°C)",
        template="plotly_dark",
    )

    if output_path:
        fig.write_html(output_path)
    else:
        fig.show()
    return fig
