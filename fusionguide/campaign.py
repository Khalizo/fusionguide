"""FusionCampaign — BayBE wrapper with fusion-domain features."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from baybe import Campaign as BaybeCampaign
from baybe.objectives import SingleTargetObjective
from baybe.searchspace import SearchSpace
from baybe.targets import NumericalTarget


class FusionCampaign:
    """Wrap BayBE Campaign with fusion-domain parameter spaces and utilities."""

    def __init__(
        self,
        name: str,
        parameters: list,
        target: NumericalTarget,
        prior_data: pd.DataFrame | None = None,
    ):
        self.name = name
        self._parameters = parameters
        self._target = target

        searchspace = SearchSpace.from_product(parameters=parameters)
        objective = SingleTargetObjective(target=target)
        self._campaign = BaybeCampaign(searchspace=searchspace, objective=objective)

        if prior_data is not None and len(prior_data) > 0:
            self._campaign.add_measurements(prior_data)

    @property
    def n_measurements(self) -> int:
        return len(self._campaign.measurements)

    def recommend(self, n: int = 1) -> pd.DataFrame:
        """Return n recommended parameter configurations as a DataFrame."""
        return self._campaign.recommend(batch_size=n)

    def add_measurement(self, df: pd.DataFrame) -> None:
        """Register measurement results. df must include target column."""
        self._campaign.add_measurements(df)

    def save(self, path: str) -> None:
        """Serialize campaign to JSON."""
        data = {
            "name": self.name,
            "campaign_json": self._campaign.to_json(),
        }
        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: str) -> "FusionCampaign":
        """Load campaign from JSON."""
        data = json.loads(Path(path).read_text())
        obj = cls.__new__(cls)
        obj.name = data["name"]
        obj._campaign = BaybeCampaign.from_json(data["campaign_json"])
        return obj
