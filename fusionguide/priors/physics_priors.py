"""Physics-informed GP prior mean functions for fusion materials."""
from __future__ import annotations
import numpy as np


class RadiationHardeningPrior:
    """Dispersed Barrier Hardening (DBH) model as GP prior mean.

    Delta sigma_y ~ A * (1 - exp(-B * dpa)) * f(T)

    Reference: Orowan dispersed barrier hardening model.

    Parameters can be set directly via the constructor or by using one of the
    material-specific presets:

    - ``RadiationHardeningPrior.tungsten()`` -- W (A=180, B=0.5, baseline=500)
    - ``RadiationHardeningPrior.vanadium_alloy()`` -- V-4Cr-4Ti (A=120, B=0.4, baseline=330)
    - ``RadiationHardeningPrior.rafm_steel()`` -- RAFM steel (A=200, B=0.35, baseline=550)
    """

    def __init__(
        self,
        A_MPa: float = 180.0,
        B_inv_dpa: float = 0.5,
        T_ref_C: float = 300.0,
        baseline_mpa: float = 500.0,
    ) -> None:
        self.A_MPa = A_MPa
        self.B_inv_dpa = B_inv_dpa
        self.T_ref_C = T_ref_C
        self.baseline_mpa = baseline_mpa

    @classmethod
    def tungsten(cls) -> "RadiationHardeningPrior":
        """Preset for tungsten (W)."""
        return cls(A_MPa=180.0, B_inv_dpa=0.5, T_ref_C=300.0, baseline_mpa=500.0)

    @classmethod
    def vanadium_alloy(cls) -> "RadiationHardeningPrior":
        """Preset for V-4Cr-4Ti vanadium alloy."""
        return cls(A_MPa=120.0, B_inv_dpa=0.4, T_ref_C=300.0, baseline_mpa=330.0)

    @classmethod
    def rafm_steel(cls) -> "RadiationHardeningPrior":
        """Preset for Reduced-Activation Ferritic/Martensitic (RAFM) steel."""
        return cls(A_MPa=200.0, B_inv_dpa=0.35, T_ref_C=300.0, baseline_mpa=550.0)

    def predict_delta_yield(self, dose_dpa: float, temperature_C: float) -> float:
        t_factor = max(0.1, 1.0 - (temperature_C - self.T_ref_C) / 1000.0)
        delta = self.A_MPa * (1.0 - np.exp(-self.B_inv_dpa * dose_dpa)) * t_factor
        return max(0.0, delta)

    def predict_yield_irradiated(
        self, dose_dpa: float, temperature_C: float, baseline_mpa: float | None = None
    ) -> float:
        if baseline_mpa is None:
            baseline_mpa = self.baseline_mpa
        return baseline_mpa + self.predict_delta_yield(dose_dpa, temperature_C)
