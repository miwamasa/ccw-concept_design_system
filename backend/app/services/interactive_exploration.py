"""Interactive Design Exploration Service."""

from typing import Any, Dict, List, Optional
from enum import Enum
from ..models.graphs import DEGraph
from ..models.de_components import (
    SIComponent, PIComponent, EIComponent,
    DIComponent, CBComponent, SAComponent
)
from .knowledge_base import KnowledgeBase


class ExplorationStep(str, Enum):
    """Steps in the design exploration process."""
    INIT = "init"
    SITUATION_ASSESSMENT = "situation_assessment"
    PROBLEM_IDENTIFICATION = "problem_identification"
    ESTABLISH_INTENTION = "establish_intention"
    CHOOSE_PATH = "choose_path"  # Decompose or Apply Solution
    DECOMPOSE_INTENTION = "decompose_intention"
    APPLY_SOLUTION = "apply_solution"
    COMPLETED = "completed"


class InteractiveExplorationEngine:
    """Interactive design exploration engine.

    Provides step-by-step guidance for design exploration,
    allowing users to make decisions at each step.
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        """Initialize the interactive exploration engine.

        Args:
            knowledge_base: Optional knowledge base for suggestions
        """
        self.kb = knowledge_base or KnowledgeBase()
        self.de_graph = DEGraph()
        self.current_step = ExplorationStep.INIT
        self.component_counter = 0

        # Current context
        self.current_system: Optional[str] = None
        self.current_situation: Optional[str] = None
        self.current_problem: Optional[str] = None
        self.current_intention: Optional[str] = None
        self.pending_subsystems: List[str] = []

    def _generate_component_id(self, prefix: str) -> str:
        """Generate unique component ID."""
        self.component_counter += 1
        return f"{prefix}_{self.component_counter}"

    def start_exploration(self, initial_system: str) -> Dict[str, Any]:
        """Start a new design exploration.

        Args:
            initial_system: The initial system to explore

        Returns:
            Dictionary with next step information
        """
        self.de_graph = DEGraph()
        self.current_system = initial_system
        self.current_step = ExplorationStep.SITUATION_ASSESSMENT
        self.component_counter = 0
        self.pending_subsystems = []

        # Get suggested situation from KB
        suggested_situation = self.kb.query_situation(initial_system)

        return {
            "step": self.current_step.value,
            "system": self.current_system,
            "suggested_situation": suggested_situation,
            "available_situations": self.kb.get_all_situations(),
            "message": f"Assess the situation for system: {initial_system}",
            "graph": self.de_graph.to_dict()
        }

    def assess_situation(self, situation: str) -> Dict[str, Any]:
        """Execute situation assessment step.

        Args:
            situation: The situation to assess

        Returns:
            Dictionary with next step information
        """
        # Create SI component
        si_comp = SIComponent(
            id=self._generate_component_id("SI"),
            system=self.current_system,
            situation=situation
        )
        self.de_graph.add_component(si_comp)
        self.current_situation = situation

        # Move to problem identification
        self.current_step = ExplorationStep.PROBLEM_IDENTIFICATION

        # Get suggested problem from KB
        suggested_problem = self.kb.query_problem(
            self.current_system,
            situation
        )

        return {
            "step": self.current_step.value,
            "system": self.current_system,
            "situation": situation,
            "suggested_problem": suggested_problem,
            "available_problems": self.kb.get_all_problems(),
            "message": f"Identify problems for system in situation: {situation}",
            "graph": self.de_graph.to_dict()
        }

    def identify_problem(self, problem: str) -> Dict[str, Any]:
        """Execute problem identification step.

        Args:
            problem: The identified problem

        Returns:
            Dictionary with next step information
        """
        # Create PI component
        pi_comp = PIComponent(
            id=self._generate_component_id("PI"),
            system=self.current_system,
            problem=problem
        )
        self.de_graph.add_component(pi_comp)

        # Add edge from previous component
        prev_components = self.de_graph.get_components()
        if len(prev_components) > 1:
            self.de_graph.add_edge(prev_components[-2].id, pi_comp.id)

        self.current_problem = problem

        # Move to intention establishment
        self.current_step = ExplorationStep.ESTABLISH_INTENTION

        # Get suggested intention from KB
        suggested_intention = self.kb.query_intention(problem)

        return {
            "step": self.current_step.value,
            "problem": problem,
            "suggested_intention": suggested_intention,
            "available_intentions": self.kb.get_all_intentions(),
            "message": f"Establish intention to solve problem: {problem}",
            "graph": self.de_graph.to_dict()
        }

    def establish_intention(self, intention: str) -> Dict[str, Any]:
        """Execute intention establishment step.

        Args:
            intention: The established intention

        Returns:
            Dictionary with next step information
        """
        # Create EI component
        ei_comp = EIComponent(
            id=self._generate_component_id("EI"),
            system=self.current_system,
            problem=self.current_problem,
            intention=intention
        )
        self.de_graph.add_component(ei_comp)

        # Add edge from previous component
        prev_components = self.de_graph.get_components()
        if len(prev_components) > 1:
            self.de_graph.add_edge(prev_components[-2].id, ei_comp.id)

        self.current_intention = intention

        # Check if decomposition is available
        decomposition = self.kb.query_decomposition(
            self.current_system,
            intention
        )

        # Check if solutions are available
        solutions = self.kb.query_solutions(self.current_system)

        # Move to path choice
        self.current_step = ExplorationStep.CHOOSE_PATH

        return {
            "step": self.current_step.value,
            "intention": intention,
            "can_decompose": decomposition is not None,
            "can_apply_solution": len(solutions) > 0,
            "suggested_decomposition": decomposition,
            "available_solutions": solutions,
            "message": f"Choose next step: decompose intention or apply solution?",
            "graph": self.de_graph.to_dict()
        }

    def decompose_intention(
        self,
        sub_intentions: List[str],
        sub_systems: List[str]
    ) -> Dict[str, Any]:
        """Execute intention decomposition step.

        Args:
            sub_intentions: List of sub-intentions
            sub_systems: List of sub-systems

        Returns:
            Dictionary with next step information
        """
        # Create DI component
        di_comp = DIComponent(
            id=self._generate_component_id("DI"),
            system=self.current_system,
            intention=self.current_intention,
            sub_intentions=sub_intentions,
            sub_systems=sub_systems
        )
        self.de_graph.add_component(di_comp)

        # Add edge from previous component
        prev_components = self.de_graph.get_components()
        if len(prev_components) > 1:
            self.de_graph.add_edge(prev_components[-2].id, di_comp.id)

        # Add subsystems to pending list for further exploration
        self.pending_subsystems = sub_systems.copy()

        # If there are subsystems to explore, start with the first one
        if self.pending_subsystems:
            next_system = self.pending_subsystems.pop(0)
            self.current_system = next_system
            self.current_step = ExplorationStep.SITUATION_ASSESSMENT

            suggested_situation = self.kb.query_situation(next_system)

            return {
                "step": self.current_step.value,
                "system": next_system,
                "suggested_situation": suggested_situation,
                "available_situations": self.kb.get_all_situations(),
                "pending_subsystems": self.pending_subsystems,
                "message": f"Explore subsystem: {next_system}",
                "graph": self.de_graph.to_dict()
            }
        else:
            self.current_step = ExplorationStep.COMPLETED
            return {
                "step": self.current_step.value,
                "message": "Design exploration completed!",
                "graph": self.de_graph.to_dict()
            }

    def apply_solution(self, solution: str) -> Dict[str, Any]:
        """Execute solution application step.

        Args:
            solution: The solution to apply

        Returns:
            Dictionary with next step information
        """
        subsystem = f"{self.current_system}_{solution}"

        # Create SA component
        sa_comp = SAComponent(
            id=self._generate_component_id("SA"),
            system=self.current_system,
            solution=solution,
            subsystem=subsystem
        )
        self.de_graph.add_component(sa_comp)

        # Add edge from previous component
        prev_components = self.de_graph.get_components()
        if len(prev_components) > 1:
            self.de_graph.add_edge(prev_components[-2].id, sa_comp.id)

        # Check if there are more pending subsystems
        if self.pending_subsystems:
            next_system = self.pending_subsystems.pop(0)
            self.current_system = next_system
            self.current_step = ExplorationStep.SITUATION_ASSESSMENT

            suggested_situation = self.kb.query_situation(next_system)

            return {
                "step": self.current_step.value,
                "system": next_system,
                "suggested_situation": suggested_situation,
                "available_situations": self.kb.get_all_situations(),
                "pending_subsystems": self.pending_subsystems,
                "message": f"Explore subsystem: {next_system}",
                "graph": self.de_graph.to_dict()
            }
        else:
            self.current_step = ExplorationStep.COMPLETED
            return {
                "step": self.current_step.value,
                "message": "Design exploration completed!",
                "graph": self.de_graph.to_dict()
            }

    def get_current_state(self) -> Dict[str, Any]:
        """Get current exploration state.

        Returns:
            Dictionary with current state information
        """
        return {
            "step": self.current_step.value,
            "system": self.current_system,
            "situation": self.current_situation,
            "problem": self.current_problem,
            "intention": self.current_intention,
            "pending_subsystems": self.pending_subsystems,
            "graph": self.de_graph.to_dict()
        }

    def get_graph(self) -> DEGraph:
        """Get the current DE graph."""
        return self.de_graph

    def reset(self):
        """Reset the exploration state."""
        self.de_graph = DEGraph()
        self.current_step = ExplorationStep.INIT
        self.component_counter = 0
        self.current_system = None
        self.current_situation = None
        self.current_problem = None
        self.current_intention = None
        self.pending_subsystems = []
