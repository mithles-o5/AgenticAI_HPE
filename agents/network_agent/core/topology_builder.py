"""Topology builder — constructs a NetworkX graph from LLDP/CDP neighbor data.

Completely protocol-agnostic: works on the normalized neighbor list that any
adapter's discover_neighbors() returns.
"""

from __future__ import annotations
from typing import Any, Dict, List

try:
    import networkx as nx
    _HAS_NETWORKX = True
except ImportError:
    _HAS_NETWORKX = False


class TopologyBuilder:
    """Builds and queries a device topology graph from neighbor discovery data."""

    def __init__(self) -> None:
        if _HAS_NETWORKX:
            self._graph = nx.Graph()
        else:
            self._graph = None   # graceful degradation if networkx not installed
        self._nodes: Dict[str, Dict[str, Any]] = {}

    def add_device(self, device_id: str, metadata: Dict[str, Any] = None) -> None:
        self._nodes[device_id] = metadata or {}
        if self._graph is not None:
            self._graph.add_node(device_id, **(metadata or {}))

    def add_neighbors(self, device_id: str, neighbors: List[Dict[str, Any]]) -> None:
        """
        Add edges from device_id to each neighbor.
        Each neighbor dict must contain "neighbor_id" and optionally "local_port", "neighbor_port".
        """
        for n in neighbors:
            neighbor_id = n.get("neighbor_id", "unknown")
            if self._graph is not None:
                self._graph.add_edge(
                    device_id,
                    neighbor_id,
                    local_port=n.get("local_port", ""),
                    neighbor_port=n.get("neighbor_port", ""),
                )
            self._nodes.setdefault(neighbor_id, {})

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the graph to a JSON-compatible dict."""
        nodes = [{"id": nid, **meta} for nid, meta in self._nodes.items()]
        if self._graph is not None:
            edges = [
                {"source": u, "target": v, **data}
                for u, v, data in self._graph.edges(data=True)
            ]
        else:
            edges = []
        return {"nodes": nodes, "edges": edges}

    def to_oasf_topology(self) -> List[Dict[str, Any]]:
        """Return a list of TopologyNode-compatible dicts for the TaskResponse."""
        result = []
        for node_id, meta in self._nodes.items():
            neighbors = []
            if self._graph is not None and node_id in self._graph:
                neighbors = list(self._graph.neighbors(node_id))
            result.append({
                "node_id":     node_id,
                "hostname":    meta.get("hostname", node_id),
                "device_type": meta.get("device_type", "unknown"),
                "interfaces":  meta.get("interfaces", []),
                "neighbors":   neighbors,
            })
        return result
