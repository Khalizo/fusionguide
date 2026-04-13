"""BayBE targets for fusion materials mechanical properties."""
from baybe.targets import NumericalTarget


def YieldStrengthTarget() -> NumericalTarget:
    """Target: maximise yield strength."""
    return NumericalTarget(name="yield_strength_MPa", minimize=False)


def DielectricStrengthTarget() -> NumericalTarget:
    """Target: maximise dielectric strength retention after irradiation."""
    return NumericalTarget(name="dielectric_strength_MV_m", minimize=False)


def YieldStrengthDeltaTarget() -> NumericalTarget:
    """Target: minimise irradiation hardening delta."""
    return NumericalTarget(name="yield_strength_delta_MPa", minimize=True)
