# FusionBAL

**Bayesian Active Learning for fusion materials experiment planning.** Tells you which irradiation experiments to run next to characterise a material with the fewest possible reactor slots.

Built on BayBE (Merck, Apache 2.0) + BoTorch (Meta). The fusion-domain adaptation — parameter spaces, facility scheduling, physics priors — is the novel contribution.

---

## The problem it solves

A slot at HFIR costs ~$500k and has an 18-month queue. You have 15 experiment budget slots to characterise V-4Cr-4Ti yield strength across dose and temperature. Random sampling needs ~25 experiments to reach 15 MPa uncertainty. FusionBAL reaches it in ~9. That's the Digilab Bristol result for vanadium alloys — 30 samples → 9.

---

## Install

```bash
cd fusionbal
pip install -e .
```

Requires Python 3.10+. BayBE and BoTorch install automatically.

---

## Usage

### Get experiment recommendations

```bash
# Vanadium alloy irradiation campaign
fusionbal recommend --material vanadium_alloy --n 3

# Ceramic insulator (Helion programme)
fusionbal recommend --material ceramic_insulator --n 3

# Load prior data from FusionMatDB to warm-start the GP
fusionbal recommend --material vanadium_alloy --n 3 --prior-parquet ../fusionmatdb/fusionmatdb_export.parquet
```

### Find the right facility

```bash
# What facilities can take 20 samples within 12 months for £200k?
fusionbal facilities --timeline 12 --samples 20 --budget 200
```

### Python API

```python
from fusionbal import FusionCampaign
from fusionbal.spaces import VanadiumAlloySpace
from fusionbal.targets import YieldStrengthTarget
from fusionbal.priors import load_prior_synthetic_vanadium

# Start a campaign — warm-start with FusionMatDB prior
campaign = FusionCampaign(
    name="V-4Cr-4Ti characterisation",
    parameters=VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0), temperature_range=(200, 600)),
    target=YieldStrengthTarget(),
    prior_data=load_prior_synthetic_vanadium(),  # replace with real FusionMatDB data
)

# Get next recommended experiment
rec = campaign.recommend(n=1)
print(rec)
# dose_dpa=8.3, irradiation_temperature_C=412, neutron_spectrum=fission, ...

# Report result, update model
measurement = rec.copy()
measurement["yield_strength_MPa"] = 647.0
campaign.add_measurement(measurement)

# Save and resume later
campaign.save("v4crti_campaign.json")
campaign = FusionCampaign.load("v4crti_campaign.json")
```

---

## Pre-configured parameter spaces

| Space | Material | Parameters |
|---|---|---|
| `VanadiumAlloySpace` | V-4Cr-4Ti | dose_dpa, temperature, Cr/Ti wt%, neutron spectrum, test temp |
| `CeramicInsulatorSpace` | Al₂O₃, MgAl₂O₄, AlN, SiC, BN, ZrO₂ | ceramic class, additive wt%, sintering temp, dose, test temp |

Add more in `fusionbal/spaces/`.

---

## Physics priors

The `RadiationHardeningPrior` encodes the Dispersed Barrier Hardening (DBH) model as a GP prior mean function:

```
Δσ_y = A × (1 − exp(−B × dpa)) × f(T)
```

This means the GP isn't learning radiation hardening from scratch — it starts with known physics and learns corrections. Far more data-efficient than a black-box GP.

---

## Facility scheduler

```python
from fusionbal.facility_scheduler import recommend_facility

recs = recommend_facility(timeline_months=12, n_samples=20, budget_relative=200.0)
# Returns: HFIR (fidelity=85%, queue=12mo), ion_beam (fidelity=30%, queue=1mo), ...
```

Facilities modelled: HFIR, ATR, BOR-60, BR2, ion_beam, proton.

---

## Uncertainty map

```python
from fusionbal.visualise.uncertainty_map import plot_uncertainty_map

# Shows where the GP is most uncertain — where to experiment next
plot_uncertainty_map(campaign, output_path="uncertainty_map.html")
```

---

## How it connects to the platform

- **Input**: loads FusionMatDB Parquet as prior data (historical measurements warm-start the GP)
- **Output**: experiment recommendations feed Helion/Tokamak Energy lab planning
- **Loop**: after each experiment, `campaign.add_measurement()` updates the GP and tightens uncertainty

This is the active learning flywheel: more experiments → better GP → fewer experiments needed.

---

## BayBE version note

Uses BayBE v0.14.3+. Target API changed in v0.14: use `NumericalTarget(minimize=False)` not `mode="MAX"`.
