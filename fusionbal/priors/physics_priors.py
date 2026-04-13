"""Physics-informed GP prior mean functions for fusion materials."""
from __future__ import annotations
import numpy as np


class RadiationHardeningPrior:
    """Dispersed Barrier Hardening (DBH) model as GP prior mean.

    Delta sigma_y ~ A * (1 - exp(-B * dpa)) * f(T)
    Reference: Orowan dispersed barrier hardening, calibrated to W literature.
    """
    A_MPa: float = 180.0
    B_inv_dpa: float = 0.5
    T_ref_C: float = 300.0

    def predict_delta_yield(self, dose_dpa: float, temperature_C: float) -> float:
        t_factor = max(0.1, 1.0 - (temperature_C - self.T_ref_C) / 1000.0)
        delta = self.A_MPa * (1.0 - np.exp(-self.B_inv_dpa * dose_dpa)) * t_factor
        return max(0.0, delta)

    def predict_yield_irradiated(
        self, dose_dpa: float, temperature_C: float, baseline_mpa: float = 500.0
    ) -> float:
        return baseline_mpa + self.predict_delta_yield(dose_dpa, temperature_C)
