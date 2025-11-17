"""Graph structures for DE, LD, and SI graphs."""

from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import networkx as nx
from pydantic import BaseModel, Field


class LogicOperator(str, Enum):
    """Logic operators for LD graph."""
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


class GraphType(str, Enum):
    """Graph type enumeration."""
    DE = "DesignExploration"
    LD = "LogicalDependency"
    SI = "SystemsIntegration"


class Edge(BaseModel):
    """Edge representation."""
    source: str
    target: str
    logic: Optional[LogicOperator] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Node(BaseModel):
    """Node representation."""
    id: str
    data: Any
    node_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DEGraph:
    """Design Exploration Graph.

    Records the history of design exploration activities.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, Any] = {}

    def add_component(self, component: Any) -> None:
        """Add a DE component to the graph."""
        self.graph.add_node(component.id, component=component)
        self.components[component.id] = component

    def add_edge(self, source_id: str, target_id: str, **attrs) -> None:
        """Add an edge between components."""
        self.graph.add_edge(source_id, target_id, **attrs)

    def get_component(self, component_id: str) -> Optional[Any]:
        """Get a component by ID."""
        return self.components.get(component_id)

    def get_components(self) -> List[Any]:
        """Get all components."""
        return list(self.components.values())

    def get_edges(self) -> List[Tuple[str, str]]:
        """Get all edges."""
        return list(self.graph.edges())

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation."""
        nodes = []
        for node_id in self.graph.nodes():
            component = self.components[node_id]
            nodes.append(component.to_dict())

        edges = []
        for source, target in self.graph.edges():
            edge_data = self.graph[source][target]
            edges.append({
                "source": source,
                "target": target,
                **edge_data
            })

        return {
            "type": GraphType.DE.value,
            "nodes": nodes,
            "edges": edges
        }

    def __repr__(self) -> str:
        return f"DEGraph(nodes={len(self.graph.nodes())}, edges={len(self.graph.edges())})"


class LDGraph:
    """Logical Dependency Graph.

    Represents logical dependencies between systems and situations.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, data: Any = None, **attrs) -> None:
        """Add a node to the graph."""
        self.graph.add_node(node_id, data=data, **attrs)

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        logic: Optional[LogicOperator] = None,
        **attrs
    ) -> None:
        """Add an edge with optional logic operator."""
        self.graph.add_edge(source_id, target_id, logic=logic, **attrs)

    def get_node_data(self, node_id: str) -> Optional[Any]:
        """Get node data."""
        if node_id in self.graph.nodes():
            return self.graph.nodes[node_id].get('data')
        return None

    def get_nodes(self) -> List[str]:
        """Get all node IDs."""
        return list(self.graph.nodes())

    def get_edges(self) -> List[Dict[str, Any]]:
        """Get all edges with attributes."""
        edges = []
        for source, target in self.graph.edges():
            edge_data = self.graph[source][target]
            edges.append({
                "source": source,
                "target": target,
                **edge_data
            })
        return edges

    def get_in_edges(self, node_id: str) -> List[Dict[str, Any]]:
        """Get incoming edges for a node."""
        edges = []
        for source, target in self.graph.in_edges(node_id):
            edge_data = self.graph[source][target]
            edges.append({
                "source": source,
                "target": target,
                **edge_data
            })
        return edges

    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors of a node."""
        return list(self.graph.neighbors(node_id))

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation."""
        nodes = []
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            nodes.append({
                "id": node_id,
                **node_data
            })

        edges = self.get_edges()

        return {
            "type": GraphType.LD.value,
            "nodes": nodes,
            "edges": edges
        }

    def __repr__(self) -> str:
        return f"LDGraph(nodes={len(self.graph.nodes())}, edges={len(self.graph.edges())})"


class SIGraph:
    """Systems Integration Graph.

    Represents system hierarchy and subsystem relationships.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, Any] = {}
        self.hierarchies: Dict[str, List[str]] = {}  # level -> node_ids

    def add_component(self, component: Any, level: int = 0) -> None:
        """Add an SI component to the graph."""
        self.graph.add_node(component.id, component=component, level=level)
        self.components[component.id] = component

        # Track hierarchy
        level_key = f"Level_{level}"
        if level_key not in self.hierarchies:
            self.hierarchies[level_key] = []
        self.hierarchies[level_key].append(component.id)

    def add_root(self, node_id: str, level: int = 0) -> None:
        """Add a root node."""
        self.graph.add_node(node_id, level=level, is_root=True)

        level_key = f"Level_{level}"
        if level_key not in self.hierarchies:
            self.hierarchies[level_key] = []
        self.hierarchies[level_key].append(node_id)

    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        level: int = 0,
        **attrs
    ) -> None:
        """Add a dependency edge."""
        self.graph.add_edge(source_id, target_id, level=level, **attrs)

    def get_component(self, component_id: str) -> Optional[Any]:
        """Get a component by ID."""
        return self.components.get(component_id)

    def get_components(self) -> List[Any]:
        """Get all components."""
        return list(self.components.values())

    def get_hierarchy_level(self, level: int) -> List[str]:
        """Get all nodes at a specific hierarchy level."""
        level_key = f"Level_{level}"
        return self.hierarchies.get(level_key, [])

    def find_components_by_type(self, component_type: Any) -> List[Any]:
        """Find components by type."""
        return [
            comp for comp in self.components.values()
            if comp.type == component_type
        ]

    def replace_component(self, old_component: Any, new_component: Any) -> None:
        """Replace a component with another."""
        if old_component.id in self.components:
            # Get the level
            level = self.graph.nodes[old_component.id].get('level', 0)

            # Remove old component
            self.graph.remove_node(old_component.id)
            del self.components[old_component.id]

            # Add new component
            self.add_component(new_component, level)

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation."""
        nodes = []
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            component = self.components.get(node_id)

            if component:
                nodes.append({
                    **component.to_dict(),
                    "level": node_data.get('level', 0)
                })
            else:
                nodes.append({
                    "id": node_id,
                    **node_data
                })

        edges = []
        for source, target in self.graph.edges():
            edge_data = self.graph[source][target]
            edges.append({
                "source": source,
                "target": target,
                **edge_data
            })

        return {
            "type": GraphType.SI.value,
            "nodes": nodes,
            "edges": edges,
            "hierarchies": self.hierarchies
        }

    def __repr__(self) -> str:
        return f"SIGraph(nodes={len(self.graph.nodes())}, edges={len(self.graph.edges())}, levels={len(self.hierarchies)})"
