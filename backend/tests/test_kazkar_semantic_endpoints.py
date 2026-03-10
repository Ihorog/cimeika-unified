"""
Contract tests for Kazkar semantic legend API endpoints (strict mode).
Tests run without a real database — the semantic core is stdlib-only.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "ERROR"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_pass"

from fastapi.testclient import TestClient
from main import app
from app.modules.kazkar.semantic.state import legend_state

client = TestClient(app)
BASE = "/api/v1/kazkar"


@pytest.fixture(autouse=True)
def reset_legend_state():
    """Reset in-memory legend state before each test for isolation."""
    legend_state.reset()
    yield
    legend_state.reset()


# ---------------------------------------------------------------------------
# GET /legend/activate
# ---------------------------------------------------------------------------

def test_activate_returns_ok_structure():
    resp = client.get(f"{BASE}/legend/activate")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    result = data["result"]
    assert result["type"] == "legend_activated"


def test_activate_sets_current_node_prysutnist():
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    assert result["current_node"]["id"] == "prysutnist"
    assert result["current_node"]["nazva"] == "Присутність"


def test_activate_history_starts_with_prysutnist():
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    assert result["history"] == ["prysutnist"]


def test_activate_stats_nodes_equals_available_nodes():
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    assert result["stats"]["nodes"] == len(result["available_nodes"])
    assert result["stats"]["nodes"] == 10


def test_activate_available_nodes_contains_all_ids():
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    expected_ids = {
        "prysutnist", "tysha", "dostatnist", "moment", "spokiy",
        "pryynyattya", "chas", "balans", "mudrist", "tsykl",
    }
    assert set(result["available_nodes"]) == expected_ids


def test_activate_timestamp_is_int():
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    assert isinstance(result["timestamp"], int)
    assert result["timestamp"] > 0


def test_activate_idempotent_resets_history():
    client.get(f"{BASE}/legend/activate")
    client.get(f"{BASE}/legend/node/tysha")
    resp = client.get(f"{BASE}/legend/activate")
    result = resp.json()["result"]
    assert result["history"] == ["prysutnist"]


# ---------------------------------------------------------------------------
# GET /legend/node/{id} — before activation (strict mode)
# ---------------------------------------------------------------------------

def test_node_before_activate_returns_409():
    resp = client.get(f"{BASE}/legend/node/tysha")
    assert resp.status_code == 409


def test_node_before_activate_error_code():
    resp = client.get(f"{BASE}/legend/node/tysha")
    detail = resp.json()["detail"]
    assert detail["ok"] is False
    assert detail["error"]["code"] == "LEGEND_NOT_ACTIVE"


# ---------------------------------------------------------------------------
# GET /legend/node/{id} — after activation
# ---------------------------------------------------------------------------

def test_node_invalid_after_activate_returns_404():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/node/nonexistent_node_xyz")
    assert resp.status_code == 404


def test_node_invalid_after_activate_error_code():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/node/nonexistent_node_xyz")
    detail = resp.json()["detail"]
    assert detail["error"]["code"] == "NODE_NOT_FOUND"


def test_navigate_after_activate_returns_correct_node():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/node/tysha")
    assert resp.status_code == 200
    result = resp.json()["result"]
    assert result["type"] == "legend_navigated"
    assert result["current_node"]["id"] == "tysha"
    assert result["current_node"]["nazva"] == "Тиша"


def test_navigate_returns_linked_nodes():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/node/tysha")
    result = resp.json()["result"]
    linked_ids = {l["id"] for l in result["linked"]}
    # tysha is connected to prysutnist and spokiy
    assert "prysutnist" in linked_ids
    assert "spokiy" in linked_ids


def test_navigate_linked_nodes_have_required_fields():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/node/tysha")
    result = resp.json()["result"]
    for linked in result["linked"]:
        assert "id" in linked
        assert "nazva" in linked
        assert "hlybyna" in linked


def test_navigate_history_tail_grows():
    client.get(f"{BASE}/legend/activate")
    client.get(f"{BASE}/legend/node/tysha")
    resp = client.get(f"{BASE}/legend/node/spokiy")
    result = resp.json()["result"]
    tail = result["history_tail"]
    assert "prysutnist" in tail
    assert "tysha" in tail
    assert "spokiy" in tail


def test_navigate_history_tail_max_five():
    client.get(f"{BASE}/legend/activate")
    path = ["tysha", "spokiy", "pryynyattya", "mudrist", "balans", "dostatnist"]
    for node_id in path:
        client.get(f"{BASE}/legend/node/{node_id}")
    resp = client.get(f"{BASE}/legend/node/moment")
    result = resp.json()["result"]
    assert len(result["history_tail"]) <= 5


# ---------------------------------------------------------------------------
# GET /legend/export — strict mode
# ---------------------------------------------------------------------------

def test_export_before_activate_returns_409():
    resp = client.get(f"{BASE}/legend/export")
    assert resp.status_code == 409


def test_export_before_activate_error_code():
    resp = client.get(f"{BASE}/legend/export")
    detail = resp.json()["detail"]
    assert detail["error"]["code"] == "LEGEND_NOT_ACTIVE"


def test_export_after_activate_returns_ok():
    client.get(f"{BASE}/legend/activate")
    resp = client.get(f"{BASE}/legend/export")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_export_legend_count_nodes_correct():
    client.get(f"{BASE}/legend/activate")
    result = client.get(f"{BASE}/legend/export").json()["result"]
    assert result["legend"]["count_nodes"] == len(result["legend"]["nodes"])
    assert result["legend"]["count_nodes"] == 10


def test_export_graph_count_nodes_correct():
    client.get(f"{BASE}/legend/activate")
    result = client.get(f"{BASE}/legend/export").json()["result"]
    assert result["graph"]["count_nodes"] == len(result["graph"]["nodes"])


def test_export_graph_count_edges_correct():
    client.get(f"{BASE}/legend/activate")
    result = client.get(f"{BASE}/legend/export").json()["result"]
    assert result["graph"]["count_edges"] == len(result["graph"]["edges"])


def test_export_graph_edges_deduplicated():
    client.get(f"{BASE}/legend/activate")
    result = client.get(f"{BASE}/legend/export").json()["result"]
    edges = result["graph"]["edges"]
    seen = set()
    for e in edges:
        key = (min(e["source"], e["target"]), max(e["source"], e["target"]))
        assert key not in seen, f"Duplicate edge: {e}"
        seen.add(key)


def test_export_current_node_id_after_navigation():
    client.get(f"{BASE}/legend/activate")
    client.get(f"{BASE}/legend/node/tysha")
    result = client.get(f"{BASE}/legend/export").json()["result"]
    assert result["legend"]["current_node_id"] == "tysha"


# ---------------------------------------------------------------------------
# POST /legend/search
# ---------------------------------------------------------------------------

def test_search_returns_ok_structure():
    resp = client.post(f"{BASE}/legend/search", json={"query": "спокій"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    result = data["result"]
    assert result["type"] == "legend_search"


def test_search_count_equals_matches_len():
    resp = client.post(f"{BASE}/legend/search", json={"query": "а"})
    result = resp.json()["result"]
    assert result["count"] == len(result["matches"])


def test_search_finds_by_nazva():
    resp = client.post(f"{BASE}/legend/search", json={"query": "тиша"})
    result = resp.json()["result"]
    ids = [m["id"] for m in result["matches"]]
    assert "tysha" in ids


def test_search_finds_by_opys():
    resp = client.post(f"{BASE}/legend/search", json={"query": "усвідомлен"})
    result = resp.json()["result"]
    ids = [m["id"] for m in result["matches"]]
    assert "prysutnist" in ids


def test_search_finds_by_rezonansni_sensy():
    resp = client.post(f"{BASE}/legend/search", json={"query": "спіраль"})
    result = resp.json()["result"]
    ids = [m["id"] for m in result["matches"]]
    assert "tsykl" in ids


def test_search_sorting_hlybyna_then_id():
    resp = client.post(f"{BASE}/legend/search", json={"query": "а"})
    result = resp.json()["result"]
    matches = result["matches"]
    for i in range(len(matches) - 1):
        a = (matches[i]["hlybyna"], matches[i]["id"])
        b = (matches[i + 1]["hlybyna"], matches[i + 1]["id"])
        assert a <= b, f"Sort order violated: {a} > {b}"


def test_search_respects_limit():
    resp = client.post(f"{BASE}/legend/search", json={"query": "а", "limit": 2})
    result = resp.json()["result"]
    assert len(result["matches"]) <= 2


def test_search_empty_query_returns_422():
    resp = client.post(f"{BASE}/legend/search", json={"query": ""})
    assert resp.status_code == 422


def test_search_no_query_returns_422():
    resp = client.post(f"{BASE}/legend/search", json={})
    assert resp.status_code == 422


def test_search_no_match_returns_empty():
    resp = client.post(f"{BASE}/legend/search", json={"query": "zzz_no_match_xyz"})
    result = resp.json()["result"]
    assert result["count"] == 0
    assert result["matches"] == []


def test_search_query_preserved_in_response():
    resp = client.post(f"{BASE}/legend/search", json={"query": "  тиша  "})
    result = resp.json()["result"]
    assert result["query"] == "тиша"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
