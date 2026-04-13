"""BayBE parameter space for ceramic insulator irradiation."""
from baybe.parameters import NumericalContinuousParameter, CategoricalParameter


def CeramicInsulatorSpace(
    dose_dpa_range: tuple[float, float] = (0.001, 10.0),
) -> list:
    return [
        CategoricalParameter(
            name="ceramic_class",
            values=["Al2O3", "MgAl2O4", "AlN", "Si3N4", "SiC", "BN", "ZrO2"],
            encoding="OHE",
        ),
        NumericalContinuousParameter(
            name="additive_concentration_wt_pct",
            bounds=(0.0, 5.0),
        ),
        NumericalContinuousParameter(
            name="sintering_temperature_C",
            bounds=(1200, 2500),
        ),
        NumericalContinuousParameter(
            name="dose_dpa",
            bounds=dose_dpa_range,
        ),
        CategoricalParameter(
            name="test_temperature_C",
            values=["25", "200", "400", "600"],
            encoding="OHE",
        ),
    ]
