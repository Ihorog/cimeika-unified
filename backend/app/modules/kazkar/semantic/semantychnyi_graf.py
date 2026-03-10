"""
Semantychnyi Graf — graph edge extraction and deduplication for the legend space.
"""
from typing import Dict, List, Set, Tuple
from .prostir_legendy import NODES


def build_graph() -> Dict:
    """
    Build a deduplicated graph dict with nodes and edges.
    Edges are represented as undirected: each A-B pair appears only once.
    """
    seen: Set[Tuple[str, str]] = set()
    edges: List[Dict] = []

    for node in NODES:
        src = node["id"]
        for tgt in node.get("zv_yazani_vuzly", []):
            key: Tuple[str, str] = (min(src, tgt), max(src, tgt))
            if key not in seen:
                seen.add(key)
                edges.append({"source": key[0], "target": key[1]})

    graph_nodes = [{"id": n["id"]} for n in NODES]
    return {
        "nodes": graph_nodes,
        "edges": edges,
        "count_nodes": len(graph_nodes),
        "count_edges": len(edges),
    }


def get_edges() -> List[Dict]:
    return build_graph()["edges"]
