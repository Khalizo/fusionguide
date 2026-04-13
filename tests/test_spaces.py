import pytest
from fusionbal.spaces.vanadium_alloy import VanadiumAlloySpace
from fusionbal.spaces.ceramic_insulator import CeramicInsulatorSpace


def test_vanadium_alloy_space_returns_list():
    params = VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0), temperature_range=(200, 600))
    assert isinstance(params, list)
    assert len(params) > 0


def test_vanadium_alloy_space_has_dose_and_temp():
    params = VanadiumAlloySpace(dose_dpa_range=(0.1, 50.0), temperature_range=(200, 700))
    names = [p.name for p in params]
    assert "dose_dpa" in names
    assert "irradiation_temperature_C" in names


def test_ceramic_insulator_space_has_ceramic_class():
    params = CeramicInsulatorSpace()
    names = [p.name for p in params]
    assert "ceramic_class" in names
    assert "dose_dpa" in names


def test_vanadium_alloy_dose_bounds():
    from baybe.parameters import NumericalContinuousParameter
    params = VanadiumAlloySpace(dose_dpa_range=(0.5, 30.0))
    dose_param = next(p for p in params if p.name == "dose_dpa")
    assert isinstance(dose_param, NumericalContinuousParameter)
    # BayBE stores bounds in a Bounds object — check via to_dict or bounds attribute
    # Access the lower/upper via the bounds object
    assert dose_param.bounds.lower == 0.5
    assert dose_param.bounds.upper == 30.0


def test_yield_strength_target_minimizes_false():
    from fusionbal.targets.mechanical import YieldStrengthTarget
    target = YieldStrengthTarget()
    assert target.minimize is False


def test_yield_strength_delta_target_minimizes_true():
    from fusionbal.targets.mechanical import YieldStrengthDeltaTarget
    target = YieldStrengthDeltaTarget()
    assert target.minimize is True


def test_dielectric_strength_target_minimizes_false():
    from fusionbal.targets.mechanical import DielectricStrengthTarget
    target = DielectricStrengthTarget()
    assert target.minimize is False
