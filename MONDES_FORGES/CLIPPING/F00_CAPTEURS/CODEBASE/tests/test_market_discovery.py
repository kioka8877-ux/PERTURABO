import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "libs"))

from market_discovery import allocate_angles, build_probe_queries, _deduplicate  # noqa: E402
from premium_evidence_guard import validate_premium_output  # noqa: E402


class MarketDiscoveryTests(unittest.TestCase):
    def test_probe_queries_are_only_search_probes(self):
        probes = build_probe_queries("US residents interested in Among Us")
        self.assertTrue(probes)
        self.assertTrue(all(isinstance(p, str) and p for p in probes))

    def test_duplicate_candidates_are_removed(self):
        items = [
            {"candidate_id": "a", "normalized_key": "among us impostor", "youtube_total_views": 100, "evidence_types": ["youtube"]},
            {"candidate_id": "b", "normalized_key": "among us impostor", "youtube_total_views": 10, "evidence_types": ["youtube"]},
        ]
        kept, removed = _deduplicate(items)
        self.assertEqual([x["candidate_id"] for x in kept], ["a"])
        self.assertEqual(removed[0]["duplicate_of"], "a")

    def test_angle_allocation_rejects_missing_candidates(self):
        candidates = [{"ocean": "blue"}, {"ocean": "red"}]
        allocation = allocate_angles(candidates, 4, blue=3, red=1)
        self.assertEqual(allocation["status"], "insufficient_candidates")

    def test_premium_cannot_add_unknown_url(self):
        payload = {"evidence": ["https://youtube.com/watch?v=known"]}
        output = {"sources": ["https://youtube.com/watch?v=unknown"]}
        result = validate_premium_output(output, payload)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["anti_invention"], "fail")


if __name__ == "__main__":
    unittest.main()
