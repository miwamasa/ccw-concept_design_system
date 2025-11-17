"""Graph Conversion Engine for transforming DE -> LD -> SI graphs."""

from typing import List, Dict, Any, Optional
from ..models.graphs import DEGraph, LDGraph, SIGraph, LogicOperator
from ..models.de_components import (
    SIComponent, PIComponent, EIComponent,
    DIComponent, CBComponent, SAComponent
)
from ..models.si_components import (
    CNDComponent, BUPComponent, COLComponent,
    ALTComponent, EXOComponent
)
from ..models.component import ComponentType


class GraphConversionEngine:
    """Engine for converting between graph types.

    Performs the transformation: DE Graph -> LD Graph -> SI Graph
    """

    def __init__(self):
        self.component_counter = 0

    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        self.component_counter += 1
        return f"{prefix}_{self.component_counter}"

    def convert_de_to_ld(self, de_graph: DEGraph) -> LDGraph:
        """Convert DE graph to LD graph.

        Args:
            de_graph: Design Exploration graph

        Returns:
            Logical Dependency graph
        """
        ld_graph = LDGraph()

        for component in de_graph.get_components():
            if isinstance(component, SIComponent):
                # SI: System -> (System, Situation)
                sys_id = str(component.system)
                eval_sys_id = f"{component.system}_{component.situation}"

                ld_graph.add_node(sys_id, data=component.system)
                ld_graph.add_node(
                    eval_sys_id,
                    data=(component.system, component.situation)
                )
                ld_graph.add_edge(sys_id, eval_sys_id)

            elif isinstance(component, PIComponent):
                # PI: System -> Problem
                sys_id = str(component.system)
                prob_id = str(component.problem)

                ld_graph.add_node(sys_id, data=component.system)
                ld_graph.add_node(prob_id, data=component.problem)
                ld_graph.add_edge(sys_id, prob_id)

            elif isinstance(component, EIComponent):
                # EI: (System, Problem) -> Intention
                sys_prob_id = f"{component.system}_{component.problem}"
                int_id = str(component.intention)

                ld_graph.add_node(
                    sys_prob_id,
                    data=(component.system, component.problem)
                )
                ld_graph.add_node(int_id, data=component.intention)
                ld_graph.add_edge(
                    sys_prob_id,
                    int_id,
                    logic=LogicOperator.AND
                )

            elif isinstance(component, DIComponent):
                # DI: (System, Intention) -> {(Intentionk, Systemk)}
                source_id = f"{component.system}_{component.intention}"
                ld_graph.add_node(
                    source_id,
                    data=(component.system, component.intention)
                )

                for sub_int, sub_sys in zip(
                    component.sub_intentions,
                    component.sub_systems
                ):
                    target_id = f"{sub_int}_{sub_sys}"
                    ld_graph.add_node(target_id, data=(sub_int, sub_sys))
                    ld_graph.add_edge(
                        source_id,
                        target_id,
                        logic=LogicOperator.AND
                    )

            elif isinstance(component, CBComponent):
                # CB: (System, Intention, Situation) -> (Intention, Situation)
                source_id = f"{component.system}_{component.intention}_{component.situation}"
                target_id = f"{component.intention}_{component.situation}"

                ld_graph.add_node(
                    source_id,
                    data=(component.system, component.intention, component.situation)
                )
                ld_graph.add_node(
                    target_id,
                    data=(component.intention, component.situation)
                )
                ld_graph.add_edge(source_id, target_id)

            elif isinstance(component, SAComponent):
                # SA: (System, Solution) -> SubSystem
                source_id = f"{component.system}_{component.solution}"
                target_id = str(component.subsystem)

                ld_graph.add_node(
                    source_id,
                    data=(component.system, component.solution)
                )
                ld_graph.add_node(target_id, data=component.subsystem)
                ld_graph.add_edge(source_id, target_id)

        return ld_graph

    def simplify_ld_graph(self, ld_graph: LDGraph) -> LDGraph:
        """Simplify LD graph by removing intermediate nodes.

        Args:
            ld_graph: Logical Dependency graph

        Returns:
            Simplified LD graph
        """
        simplified = LDGraph()

        # Extract system and situation nodes only
        for node_id in ld_graph.get_nodes():
            node_data = ld_graph.get_node_data(node_id)

            # Check if it's a system or situation node
            if self._is_system_or_situation(node_data):
                simplified.add_node(node_id, data=node_data)

        # Reconstruct edges with logic preserved
        for edge in ld_graph.get_edges():
            source_data = ld_graph.get_node_data(edge['source'])
            target_data = ld_graph.get_node_data(edge['target'])

            if (self._is_system_or_situation(source_data) and
                    self._is_system_or_situation(target_data)):
                simplified.add_edge(
                    edge['source'],
                    edge['target'],
                    logic=edge.get('logic')
                )

        return simplified

    def _is_system_or_situation(self, data: Any) -> bool:
        """Check if data represents a system or situation."""
        # Simple heuristic - in production, would use proper type checking
        if data is None:
            return False
        if isinstance(data, tuple):
            return True
        if isinstance(data, str):
            # Check if it looks like a system name
            return not any(keyword in str(data).lower()
                           for keyword in ['problem', 'intention', 'solution'])
        return True

    def extract_hierarchies(self, ld_graph: LDGraph) -> Dict[str, List[str]]:
        """Extract hierarchical structure from LD graph.

        Args:
            ld_graph: Logical Dependency graph

        Returns:
            Dictionary mapping level names to node lists
        """
        hierarchies = {}

        # Simple topological sort for hierarchy levels
        visited = set()
        level = 0

        # Start with nodes that have no incoming edges (roots)
        roots = []
        for node_id in ld_graph.get_nodes():
            if len(ld_graph.get_in_edges(node_id)) == 0:
                roots.append(node_id)

        if roots:
            hierarchies[f"Level_{level}"] = roots
            visited.update(roots)
            level += 1

        # Process remaining nodes level by level
        current_level = roots
        while current_level:
            next_level = []
            for node_id in current_level:
                for neighbor in ld_graph.get_neighbors(node_id):
                    if neighbor not in visited:
                        next_level.append(neighbor)
                        visited.add(neighbor)

            if next_level:
                hierarchies[f"Level_{level}"] = list(set(next_level))
                level += 1
                current_level = next_level
            else:
                current_level = []

        return hierarchies

    def extract_si_components(
        self,
        ld_graph: LDGraph,
        hierarchies: Dict[str, List[str]]
    ) -> SIGraph:
        """Extract SI components from LD graph.

        Args:
            ld_graph: Logical Dependency graph
            hierarchies: Hierarchical structure

        Returns:
            Systems Integration graph
        """
        si_graph = SIGraph()

        for level_name, node_ids in hierarchies.items():
            level_num = int(level_name.split('_')[1])

            for node_id in node_ids:
                in_edges = ld_graph.get_in_edges(node_id)

                if len(in_edges) == 0:
                    # Root node
                    si_graph.add_root(node_id, level_num)

                elif len(in_edges) == 1:
                    # Simple dependency
                    edge = in_edges[0]
                    si_graph.add_dependency(
                        edge['source'],
                        node_id,
                        level_num
                    )

                else:
                    # Multiple inputs - determine SI component type
                    logic = self._determine_logic(in_edges)
                    subsystems = [e['source'] for e in in_edges]

                    if logic == LogicOperator.AND:
                        # Collaboration
                        comp = COLComponent(
                            id=self._generate_id("COL"),
                            subsystems=subsystems,
                            parent=node_id
                        )
                    elif logic == LogicOperator.OR:
                        # Alternative
                        comp = ALTComponent(
                            id=self._generate_id("ALT"),
                            subsystems=subsystems,
                            parent=node_id
                        )
                    elif logic == LogicOperator.XOR:
                        # Exclusive
                        comp = EXOComponent(
                            id=self._generate_id("EXO"),
                            subsystems=subsystems,
                            parent=node_id
                        )
                    else:
                        # Default to collaboration
                        comp = COLComponent(
                            id=self._generate_id("COL"),
                            subsystems=subsystems,
                            parent=node_id
                        )

                    si_graph.add_component(comp, level_num)

        return si_graph

    def _determine_logic(self, edges: List[Dict[str, Any]]) -> LogicOperator:
        """Determine logic operator from edges."""
        logics = [e.get('logic') for e in edges]

        if all(l == LogicOperator.AND for l in logics if l):
            return LogicOperator.AND
        elif all(l == LogicOperator.OR for l in logics if l):
            return LogicOperator.OR
        elif all(l == LogicOperator.XOR for l in logics if l):
            return LogicOperator.XOR
        else:
            # Default to OR for mixed or unspecified
            return LogicOperator.OR

    def convert_de_to_si(self, de_graph: DEGraph) -> SIGraph:
        """Full conversion pipeline from DE to SI graph.

        Args:
            de_graph: Design Exploration graph

        Returns:
            Systems Integration graph
        """
        # Step 1: Convert DE to LD
        ld_graph = self.convert_de_to_ld(de_graph)

        # Step 2: Simplify LD graph
        simplified_ld = self.simplify_ld_graph(ld_graph)

        # Step 3: Extract hierarchies
        hierarchies = self.extract_hierarchies(simplified_ld)

        # Step 4: Extract SI components
        si_graph = self.extract_si_components(simplified_ld, hierarchies)

        return si_graph
