"""Load historical data from FusionMatDB as BayBE prior measurements."""
from __future__ import annotations
import pandas as pd
from pathlib import Path


def load_prior_from_parquet(parquet_path: str, material_class: str | None = None) -> pd.DataFrame:
    """Load FusionMatDB Parquet export as prior measurements for BayBE."""
    path = Path(parquet_path)
    if not path.exists():
        raise FileNotFoundError(f"FusionMatDB export not found: {path}")
    df = pd.read_parquet(path)
    if material_class:
        df = df[df["material_class"] == material_class].copy()
    col_map = {
        "test_temp_c": "irradiation_temperature_C",
        "dose_dpa": "dose_dpa",
        "yield_strength_mpa_irradiated": "yield_strength_MPa",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    required = ["dose_dpa", "yield_strength_MPa"]
    df = df.dropna(subset=required)
    return df


def load_prior_synthetic_vanadium() -> pd.DataFrame:
    """Return synthetic V-4Cr-4Ti prior for testing (not real data).

    Includes all VanadiumAlloySpace parameter columns with representative defaults.
    """
    return pd.DataFrame([
        {"dose_dpa": 3.0,  "irradiation_temperature_C": 400.0, "chromium_wt_pct": 4.0, "titanium_wt_pct": 4.0, "neutron_spectrum": "fission", "test_temperature_C": "400", "yield_strength_MPa": 612.0},
        {"dose_dpa": 5.0,  "irradiation_temperature_C": 400.0, "chromium_wt_pct": 4.0, "titanium_wt_pct": 4.0, "neutron_spectrum": "fission", "test_temperature_C": "400", "yield_strength_MPa": 650.0},
        {"dose_dpa": 10.0, "irradiation_temperature_C": 400.0, "chromium_wt_pct": 4.0, "titanium_wt_pct": 4.0, "neutron_spectrum": "fission", "test_temperature_C": "400", "yield_strength_MPa": 680.0},
        {"dose_dpa": 3.0,  "irradiation_temperature_C": 600.0, "chromium_wt_pct": 4.0, "titanium_wt_pct": 4.0, "neutron_spectrum": "fission", "test_temperature_C": "600", "yield_strength_MPa": 580.0},
        {"dose_dpa": 5.0,  "irradiation_temperature_C": 600.0, "chromium_wt_pct": 4.0, "titanium_wt_pct": 4.0, "neutron_spectrum": "fission", "test_temperature_C": "600", "yield_strength_MPa": 610.0},
    ])
