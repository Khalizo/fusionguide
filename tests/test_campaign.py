import pytest
import pandas as pd
from fusionguide.campaign import FusionCampaign
from fusionguide.spaces.vanadium_alloy import VanadiumAlloySpace
from fusionguide.targets.mechanical import YieldStrengthTarget


def test_campaign_can_recommend():
    """Campaign.recommend() returns a DataFrame with parameter columns."""
    campaign = FusionCampaign(
        name="test_vanadium",
        parameters=VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0), temperature_range=(200, 600)),
        target=YieldStrengthTarget(),
    )
    rec = campaign.recommend(n=2)
    assert isinstance(rec, pd.DataFrame)
    assert len(rec) == 2
    assert "dose_dpa" in rec.columns
    assert "irradiation_temperature_C" in rec.columns


def test_campaign_add_measurement_increments_count():
    """After adding a measurement, n_measurements increases."""
    campaign = FusionCampaign(
        name="test_vanadium",
        parameters=VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0), temperature_range=(200, 600)),
        target=YieldStrengthTarget(),
    )
    assert campaign.n_measurements == 0
    rec = campaign.recommend(n=1)
    measurement = rec.copy()
    measurement["yield_strength_MPa"] = 620.0
    campaign.add_measurement(measurement)
    assert campaign.n_measurements == 1


def test_campaign_serializes_to_json(tmp_path):
    """Campaign can be saved and loaded from JSON."""
    campaign = FusionCampaign(
        name="test_save",
        parameters=VanadiumAlloySpace(),
        target=YieldStrengthTarget(),
    )
    save_path = str(tmp_path / "campaign.json")
    campaign.save(save_path)

    loaded = FusionCampaign.load(save_path)
    assert loaded.name == "test_save"


def test_physics_prior_predicts_positive_hardening():
    from fusionguide.priors.physics_priors import RadiationHardeningPrior
    prior = RadiationHardeningPrior()
    delta = prior.predict_delta_yield(dose_dpa=5.0, temperature_C=300.0)
    assert delta > 0

def test_physics_prior_higher_dose_higher_hardening():
    from fusionguide.priors.physics_priors import RadiationHardeningPrior
    prior = RadiationHardeningPrior()
    delta_low = prior.predict_delta_yield(dose_dpa=1.0, temperature_C=300.0)
    delta_high = prior.predict_delta_yield(dose_dpa=10.0, temperature_C=300.0)
    assert delta_high > delta_low


def test_synthetic_vanadium_prior_has_correct_columns():
    from fusionguide.priors.fusionmatdb import load_prior_synthetic_vanadium
    df = load_prior_synthetic_vanadium()
    assert "dose_dpa" in df.columns
    assert "irradiation_temperature_C" in df.columns
    assert "yield_strength_MPa" in df.columns
    assert len(df) >= 5


def test_campaign_with_synthetic_prior():
    """Campaign should accept synthetic vanadium prior without error."""
    from fusionguide.priors.fusionmatdb import load_prior_synthetic_vanadium
    prior = load_prior_synthetic_vanadium()
    campaign = FusionCampaign(
        name="test_prior",
        parameters=VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0), temperature_range=(200, 600)),
        target=YieldStrengthTarget(),
        prior_data=prior,
    )
    assert campaign.n_measurements == 5
    rec = campaign.recommend(n=1)
    assert isinstance(rec, pd.DataFrame)


def test_vanadium_prior_lower_baseline_than_tungsten():
    from fusionguide.priors.physics_priors import RadiationHardeningPrior
    w = RadiationHardeningPrior.tungsten()
    v = RadiationHardeningPrior.vanadium_alloy()
    assert v.baseline_mpa < w.baseline_mpa


def test_rafm_prior_higher_amplitude_than_vanadium():
    from fusionguide.priors.physics_priors import RadiationHardeningPrior
    rafm = RadiationHardeningPrior.rafm_steel()
    v = RadiationHardeningPrior.vanadium_alloy()
    assert rafm.A_MPa > v.A_MPa


def test_custom_prior_parameters():
    from fusionguide.priors.physics_priors import RadiationHardeningPrior
    prior = RadiationHardeningPrior(
        A_MPa=100.0, B_inv_dpa=0.3, T_ref_C=250.0, baseline_mpa=400.0
    )
    assert prior.A_MPa == 100.0
    assert prior.B_inv_dpa == 0.3
    assert prior.T_ref_C == 250.0
    assert prior.baseline_mpa == 400.0
    y = prior.predict_yield_irradiated(dose_dpa=5.0, temperature_C=250.0)
    assert y > 400.0
