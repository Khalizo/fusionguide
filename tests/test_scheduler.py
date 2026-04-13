import pytest
from fusionbal.facility_scheduler import recommend_facility, FacilityRecommendation


def test_recommend_excludes_long_queue():
    """Facilities with queue > timeline should be excluded."""
    recs = recommend_facility(timeline_months=6, n_samples=10, budget_relative=1000.0)
    for r in recs:
        assert r.queue_months <= 6


def test_recommend_excludes_insufficient_capacity():
    """Facilities with max_samples < n_samples should be excluded."""
    recs = recommend_facility(timeline_months=36, n_samples=100, budget_relative=1000.0)
    for r in recs:
        assert r.max_samples >= 100


def test_recommend_sorted_by_fidelity_descending():
    """Results should be sorted by fidelity, highest first."""
    recs = recommend_facility(timeline_months=36, n_samples=10, budget_relative=1000.0)
    if len(recs) > 1:
        fidelities = [r.fidelity for r in recs]
        assert fidelities == sorted(fidelities, reverse=True)


def test_recommend_require_fusion_spectrum_excludes_ion():
    """require_fusion_spectrum=True should exclude ion and proton facilities."""
    recs = recommend_facility(
        timeline_months=36, n_samples=10, budget_relative=1000.0,
        require_fusion_spectrum=True
    )
    for r in recs:
        assert r.facility not in ("ion_beam", "proton")


def test_recommend_returns_empty_for_impossible_constraints():
    """No facility can satisfy queue=0 months."""
    recs = recommend_facility(timeline_months=0, n_samples=10, budget_relative=1000.0)
    assert recs == []
