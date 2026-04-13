"""Model irradiation facility scheduling constraints."""
from __future__ import annotations
from dataclasses import dataclass

FACILITIES: dict[str, dict] = {
    "HFIR":     {"queue_months": 12,  "max_samples": 200, "spectrum": "fission",  "fidelity": 0.85, "cost_rel": 100.0},
    "ATR":      {"queue_months": 18,  "max_samples": 500, "spectrum": "fission",  "fidelity": 0.85, "cost_rel": 120.0},
    "BOR-60":   {"queue_months": 24,  "max_samples":  50, "spectrum": "fast",     "fidelity": 0.90, "cost_rel": 150.0},
    "BR2":      {"queue_months": 18,  "max_samples": 100, "spectrum": "fission",  "fidelity": 0.80, "cost_rel": 130.0},
    "ion_beam": {"queue_months":  1,  "max_samples":  20, "spectrum": "ion",      "fidelity": 0.30, "cost_rel":   1.0},
    "proton":   {"queue_months":  2,  "max_samples":  30, "spectrum": "proton",   "fidelity": 0.60, "cost_rel":  10.0},
}


@dataclass
class FacilityRecommendation:
    facility: str
    queue_months: int
    max_samples: int
    fidelity: float
    cost_relative: float
    rationale: str


def recommend_facility(
    timeline_months: int,
    n_samples: int,
    budget_relative: float = 1000.0,
    require_fusion_spectrum: bool = False,
) -> list[FacilityRecommendation]:
    """Recommend suitable facilities given experimental constraints."""
    recs = []
    for name, info in FACILITIES.items():
        if info["queue_months"] > timeline_months:
            continue
        if info["max_samples"] < n_samples:
            continue
        if info["cost_rel"] > budget_relative:
            continue
        if require_fusion_spectrum and info["spectrum"] in ("ion", "proton"):
            continue
        recs.append(FacilityRecommendation(
            facility=name,
            queue_months=info["queue_months"],
            max_samples=info["max_samples"],
            fidelity=info["fidelity"],
            cost_relative=info["cost_rel"],
            rationale=f"Queue: {info['queue_months']}mo, fidelity: {info['fidelity']:.0%}, cost: {info['cost_rel']:.0f}x",
        ))
    return sorted(recs, key=lambda r: -r.fidelity)
