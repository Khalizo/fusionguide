"""BayBE parameter space for V-4Cr-4Ti and related vanadium alloys."""
from __future__ import annotations
from baybe.parameters import NumericalContinuousParameter, CategoricalParameter


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
        CategoricalParameter(
            name="test_temperature_C",
            values=["25", "200", "400", "600"],
            encoding="OHE",
        ),
    ]
