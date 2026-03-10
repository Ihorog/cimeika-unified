"""
Kazkar Semantic Core — stdlib-only legend navigation engine.
"""
from .prostir_legendy import NODES, get_node, get_all_nodes
from .semantychnyi_graf import build_graph, get_edges
from .state import legend_state

__all__ = ["NODES", "get_node", "get_all_nodes", "build_graph", "get_edges", "legend_state"]
