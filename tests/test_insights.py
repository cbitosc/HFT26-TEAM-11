import json
from src.insights.summary import fallback_summary

def test_fallback_states_limits():
    agg = json.load(open("src/dashboard/data/aggregates.json"))
    out = fallback_summary(agg)
    assert "What we cannot conclude" in out and "opossum" in out
