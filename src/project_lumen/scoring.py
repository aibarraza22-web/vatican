from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CorpusScore:
    corpus_id: str
    name: str
    score: float
    notes: str


WEIGHTS = {
    "impact_ceiling": 2.2,
    "description_gap": 1.3,
    "historical_value": 1.4,
    "network_value": 1.1,
    "novelty_potential": 1.5,
    "feasibility": 1.2,
    "evidentiary_tractability": 1.6,
    "comparison_material": 0.8,
    "rights_clarity": 1.0,
    "saturation_penalty": -1.2,
}


def rank_corpora(path: str | Path) -> list[CorpusScore]:
    ranked: list[CorpusScore] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw_score = sum(float(row[key]) * weight for key, weight in WEIGHTS.items())
            item_count = max(int(row["digitized_items"]), 1)
            scale_bonus = min(item_count, 2500) / 2500
            ranked.append(
                CorpusScore(
                    corpus_id=row["corpus_id"],
                    name=row["name"],
                    score=round(raw_score + scale_bonus, 2),
                    notes=row["notes"],
                )
            )
    return sorted(ranked, key=lambda item: item.score, reverse=True)
