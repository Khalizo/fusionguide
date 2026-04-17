"""BayBE parameter space for V-4Cr-4Ti and related vanadium alloys."""
from __future__ import annotations
from baybe.parameters import NumericalContinuousParameter, CategoricalParameter

# Default fidelity scores encoding how representative each neutron spectrum
# is of actual DT fusion conditions.  Gives the GP a continuous dimension
# so that fission-fusion similarity is captured (instead of treating all
# spectra as orthogonal via one-hot encoding).
SPECTRUM_FIDELITY: dict[str, float] = {
    "DT_fusion": 1.0,
    "fission": 0.85,
    "ion_implantation": 0.30,
}


def VanadiumAlloySpace(
    dose_dpa_range: tuple[float, float] = (0.01, 50.0),
    temperature_range: tuple[float, float] = (200, 700),
) -> list:
    """Return BayBE parameters for vanadium alloy irradiation experiments."""
    return [
        NumericalContinuousParameter(
            name="dose_dpa",
            bounds=dose_dpa_range,
        ),
        NumericalContinuousParameter(
            name="irradiation_temperature_C",
            bounds=temperature_range,
        ),
        NumericalContinuousParameter(
            name="chromium_wt_pct",
            bounds=(3.0, 6.0),
        ),
        NumericalContinuousParameter(
            name="titanium_wt_pct",
            bounds=(2.0, 6.0),
        ),
        CategoricalParameter(
            name="neutron_spectrum",
            values=["fission", "DT_fusion", "ion_implantation"],
            encoding="OHE",
        ),
        NumericalContinuousParameter(
            name="spectrum_fidelity",
            bounds=(0.0, 1.0),
        ),
        CategoricalParameter(
            name="test_temperature_C",
            values=["25", "200", "400", "600"],
            encoding="OHE",
        ),
    ]
