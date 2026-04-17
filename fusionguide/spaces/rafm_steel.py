"""BayBE parameter space for RAFM steels (e.g. EUROFER97)."""
from __future__ import annotations
from baybe.parameters import NumericalContinuousParameter, CategoricalParameter


def RAFMSteelSpace(
    dose_dpa_range: tuple[float, float] = (0.01, 80.0),
    temperature_range: tuple[float, float] = (200, 550),
) -> list:
    """Return BayBE parameters for RAFM steel irradiation experiments."""
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
            bounds=(7.5, 9.5),
        ),
        NumericalContinuousParameter(
            name="tungsten_wt_pct",
            bounds=(0.5, 2.0),
        ),
        CategoricalParameter(
            name="heat_treatment",
            values=["normalised_tempered", "ODS", "CNA"],
            encoding="OHE",
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
            values=["25", "200", "300", "400", "550"],
            encoding="OHE",
        ),
    ]
