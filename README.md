<p align="center">
  <h1 align="center">🧭 FusionGuide</h1>
</p>

<p align="center">
  <strong>AI experiment planner for fusion materials.</strong><br>
  Tells you which irradiation experiments to run next — with the fewest possible reactor slots.
</p>

<p align="center">
  <a href="https://github.com/Khalizo/fusionguide"><img src="https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/Khalizo/fusionguide"><img src="https://img.shields.io/badge/tests-19%20passed-brightgreen?style=for-the-badge" alt="Tests"></a>
  <a href="https://github.com/Khalizo/fusionguide"><img src="https://img.shields.io/badge/engine-BayBE%200.14-orange?style=for-the-badge" alt="BayBE"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License"></a>
</p>

<p align="center">
  <a href="#the-problem">Problem</a> · <a href="#quick-start">Quick Start</a> · <a href="#how-it-works">How It Works</a> · <a href="#facility-scheduler">Facilities</a> · <a href="https://github.com/Khalizo/fusionmatdb">FusionMatDB</a> · <a href="https://github.com/Khalizo/fusionuq">FusionUQ</a>
</p>

---

## The Problem

A slot at HFIR costs ~$500k and has an 18-month queue. You have 15 experiment budget slots to characterise V-4Cr-4Ti yield strength across dose and temperature.

**Random sampling**: needs ~25 experiments to reach 15 MPa uncertainty threshold.
**FusionGuide**: reaches the same threshold in **~9 experiments**.

That's the [Digilab Bristol result](https://www.digilab.co.uk/) for vanadium alloys — and this tool replicates it with open-source code.

---

## Quick Start

```bash
pip install -e .

# Get experiment recommendations for a vanadium alloy campaign
fusionguide recommend --material vanadium_alloy --n 3

# What facilities can take 20 samples within 12 months?
fusionguide facilities --timeline 12 --samples 20

# Load real data from FusionMatDB as prior
fusionguide recommend --material vanadium_alloy --n 3 \
  --prior-parquet ../fusionmatdb/data/export.parquet
```

---

## How It Works

Built on [BayBE](https://github.com/emdgroup/baybe) (Merck, Apache 2.0) + [BoTorch](https://github.com/pytorch/botorch) (Meta). The fusion-domain adaptation is the novel contribution:

```python
from fusionguide.campaign import FusionCampaign
from fusionguide.spaces import VanadiumAlloySpace
from fusionguide.targets import YieldStrengthTarget

# Start a campaign with physics-informed prior
campaign = FusionCampaign(
    name="V-4Cr-4Ti characterisation",
    parameters=VanadiumAlloySpace(dose_dpa_range=(0.1, 20.0)),
    target=YieldStrengthTarget(),
)

# Get recommendation — tells you which dose/temp/spectrum to test
rec = campaign.recommend(n=1)
# → dose_dpa=8.3, irradiation_temperature_C=412, neutron_spectrum=fission

# Report result, update the GP
measurement = rec.copy()
measurement["yield_strength_MPa"] = 647.0
campaign.add_measurement(measurement)

# Save and resume later
campaign.save("campaign.json")
```

### What FusionGuide adds on top of BayBE

| Feature | BayBE | FusionGuide |
|---|---|---|
| Fusion parameter spaces (V-4Cr-4Ti, ceramics) | ❌ | ✅ |
| Irradiation facility scheduler | ❌ | ✅ |
| Physics prior (DBH radiation hardening model) | ❌ | ✅ |
| FusionMatDB prior loader | ❌ | ✅ |
| Uncertainty map visualisation | ❌ | ✅ |

---

## Pre-configured Spaces

| Space | Material | Parameters |
|---|---|---|
| `VanadiumAlloySpace` | V-4Cr-4Ti | dose_dpa, temperature, Cr/Ti wt%, neutron spectrum, test temp |
| `CeramicInsulatorSpace` | Al₂O₃, MgAl₂O₄, AlN, SiC, BN, ZrO₂ | ceramic class, additive wt%, sintering temp, dose, test temp |

---

## Facility Scheduler

```python
from fusionguide.facility_scheduler import recommend_facility

recs = recommend_facility(timeline_months=12, n_samples=20, budget_relative=200.0)
# → HFIR (fidelity=85%, queue=12mo), ion_beam (fidelity=30%, queue=1mo)
```

| Facility | Queue | Fidelity | Spectrum |
|---|---|---|---|
| HFIR | 12 mo | 85% | Fission |
| ATR | 18 mo | 85% | Fission |
| BOR-60 | 24 mo | 90% | Fast |
| BR2 | 18 mo | 80% | Fission |
| Ion beam | 1 mo | 30% | Ion |
| Proton | 2 mo | 60% | Proton |

---

## Physics Prior

The `RadiationHardeningPrior` encodes the Dispersed Barrier Hardening (DBH) model as a GP prior mean:

```
Δσ_y = A × (1 − exp(−B × dpa)) × f(T)
```

The GP starts with known physics and learns corrections — far more data-efficient than a black-box GP.

---

## Related Projects

| | |
|---|---|
| ⚛️ [FusionMatDB](https://github.com/Khalizo/fusionmatdb) | The database — provides GP prior data |
| 🧭 [FusionGuide](https://github.com/Khalizo/fusionguide) | This repo — experiment planning |
| 🔬 [FusionUQ](https://github.com/Khalizo/fusionuq) | Uncertainty quantification for ML potentials |
