from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from project_lumen.db import (
    add_claim,
    add_source_and_document,
    audit_database,
    connect,
    init_db,
)
from project_lumen.scoring import rank_corpora
from project_lumen.survey import (
    aggregate_hits,
    parse_detail_profile,
    parse_search_results,
)


ROOT = Path(__file__).resolve().parents[1]


class DatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.database = Path(self.tempdir.name) / "test.db"
        init_db(self.database)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _document(self, connection: sqlite3.Connection) -> int:
        return add_source_and_document(
            connection,
            institution="Test Library",
            collection="Test Collection",
            shelfmark="Test.1",
            source_url="https://example.org/test.1",
        )

    def test_claim_requires_evidence(self) -> None:
        with connect(self.database) as connection:
            document_id = self._document(connection)
            with self.assertRaises(ValueError):
                add_claim(
                    connection,
                    document_id=document_id,
                    statement="Unsupported claim",
                    level="L1",
                    confidence="weak",
                    created_by="test",
                    evidence=[],
                    alternatives=[],
                )

    def test_hypothesis_requires_alternative(self) -> None:
        with connect(self.database) as connection:
            document_id = self._document(connection)
            with self.assertRaises(ValueError):
                add_claim(
                    connection,
                    document_id=document_id,
                    statement="Single-story hypothesis",
                    level="L2",
                    confidence="plausible",
                    created_by="test",
                    evidence=[
                        {
                            "type": "text",
                            "locator": "f.1r",
                            "description": "A phrase",
                        }
                    ],
                    alternatives=[],
                )

    def test_audit_flags_unreviewed_high_level_claim(self) -> None:
        with connect(self.database) as connection:
            document_id = self._document(connection)
            add_claim(
                connection,
                document_id=document_id,
                statement="Expert-level claim",
                level="L4",
                confidence="strong",
                created_by="test",
                evidence=[
                    {
                        "type": "text",
                        "locator": "f.1r",
                        "description": "A phrase",
                    }
                ],
                alternatives=["Another author"],
            )
            problems = audit_database(connection)
        self.assertTrue(any("lacks approving expert review" in p for p in problems))


class ScoringTests(unittest.TestCase):
    def test_registry_ranks_all_rows(self) -> None:
        rows = rank_corpora(ROOT / "data" / "corpus_registry.csv")
        self.assertEqual(len(rows), 10)
        self.assertGreaterEqual(rows[0].score, rows[-1].score)


class SurveyTests(unittest.TestCase):
    SAMPLE = """
    <div class="row-search-result-record mode-partial">
      <div class="block-search-result-record-header">
        <span class="block-search-result-record-title">
          <a href="/mss/detail/Vat.lat.1"
             class="link-search-result-record-view">Vat.lat.1</a>
        </span>
      </div>
      <div class="block-search-result-record-body">
        <span class="search-result-detail-label">General Data:</span>
        <div>Fragmentum anonymum with <mark>rasura</mark>.</div>
      </div>
    </div>
    <hr class="search-result-control-separator">
    """

    def test_parse_signal_hit(self) -> None:
        hits = parse_search_results(self.SAMPLE, term="rasura", signal_weight=7)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].shelfmark, "Vat.lat.1")
        self.assertEqual(hits[0].section, "General Data:")
        self.assertGreater(hits[0].score, 7)

    def test_aggregate_combines_signals(self) -> None:
        hit_one = parse_search_results(
            self.SAMPLE, term="rasura", signal_weight=7
        )[0]
        hit_two = parse_search_results(
            self.SAMPLE, term="fragmentum", signal_weight=7
        )[0]
        ranked = aggregate_hits([hit_one, hit_two])
        self.assertEqual(ranked[0]["signal_count"], 2)
        self.assertIn("fragmentum", ranked[0]["signals"])

    def test_detail_profile_counts_catalog_and_bibliography(self) -> None:
        page = """
        <div id="region-detail-body">
          <div class="block-detail-record x">Anonymous fragment</div>
          <div class="block-detail-record x">Second text</div>
          Bibliographic References:
          <div class="block-detail-record x">Study One</div>
          <div class="block-detail-record x">Study Two</div>
        </div></section>
        """
        profile = parse_detail_profile("Test.1", page)
        self.assertEqual(profile["content_entries"], 2)
        self.assertEqual(profile["bibliography_entries"], 2)
        self.assertEqual(profile["description_gap_score"], 4)


if __name__ == "__main__":
    unittest.main()
