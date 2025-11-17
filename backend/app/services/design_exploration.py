"""Design Exploration Engine with state transition system."""

from enum import Enum
from typing import Any, Dict, Optional, Callable
from ..models.graphs import DEGraph
from ..models.de_components import (
    SIComponent, PIComponent, EIComponent,
    DIComponent, CBComponent, SAComponent
)


class State(str, Enum):
    """States in the design exploration process."""
    START = "Start"
    FACT = "Fact"
    SITUATION_ASSESSMENT = "SituationAssessment"
    PROBLEM_IDENTIFICATION = "ProblemIdentification"
    ESTABLISH_INTENTION = "EstablishIntention"
    SEARCHING = "Searching"
    DECOMPOSE_INTENTION = "DecomposeIntention"
    APPLYING_SOLUTION = "ApplyingSolution"
    SUBSYSTEM_FOUND = "SubSystemFound"
    END = "End"
    ASSESS_SIDE_EFFECT = "AssessSideEffect"
    SIDE_EFFECT_IDENTIFIED = "SideEffectIdentified"


class DesignExplorationEngine:
    """Design Exploration Engine.

    Guides the design process through state transitions and
    builds the DE graph.
    """

    def __init__(self, knowledge_base: Optional[Any] = None):
        """Initialize the design exploration engine.

        Args:
            knowledge_base: Optional knowledge base for queries
        """
        self.kb = knowledge_base
        self.current_state = State.START
        self.de_graph = DEGraph()
        self.current_system: Optional[Any] = None
        self.current_situation: Optional[Any] = None
        self.current_problem: Optional[Any] = None
        self.current_intention: Optional[Any] = None
        self.candidate_solutions: list = []
        self.component_counter = 0

    def _generate_component_id(self, prefix: str) -> str:
        """Generate unique component ID."""
        self.component_counter += 1
        return f"{prefix}_{self.component_counter}"

    def explore(
        self,
        initial_system: Any,
        interaction_handler: Optional[Callable] = None
    ) -> DEGraph:
        """Main exploration loop.

        Args:
            initial_system: The initial system to explore
            interaction_handler: Optional handler for designer interaction

        Returns:
            The constructed DE graph
        """
        self.current_system = initial_system
        self.current_state = State.FACT

        # For prototype, we'll do a simple linear exploration
        # In production, this would be an interactive loop
        self._execute_exploration_sequence()

        return self.de_graph

    def _execute_exploration_sequence(self):
        """Execute a sample exploration sequence."""
        # This is a simplified version for demonstration
        # In production, this would be interactive with the designer

        # Step 1: Situation Assessment
        si_comp = self.assess_situation(self.current_system, "obstacle detected")
        self.de_graph.add_component(si_comp)

        # Step 2: Problem Identification
        pi_comp = self.identify_problem(si_comp.system, "collision risk")
        self.de_graph.add_component(pi_comp)
        self.de_graph.add_edge(si_comp.id, pi_comp.id)

        # Step 3: Establish Intention
        ei_comp = self.establish_intention(
            si_comp.system,
            pi_comp.problem,
            "avoid collision"
        )
        self.de_graph.add_component(ei_comp)
        self.de_graph.add_edge(pi_comp.id, ei_comp.id)

        # Step 4: Decompose Intention
        di_comp = self.decompose_intention(
            ei_comp.system,
            ei_comp.intention,
            ["avoid by car", "avoid by driver"],
            ["auto_maneuvering_system", "human_maneuvering_system"]
        )
        self.de_graph.add_component(di_comp)
        self.de_graph.add_edge(ei_comp.id, di_comp.id)

        # Step 5: Solution Assignment (for one subsystem)
        sa_comp = self.apply_solution(
            "auto_maneuvering_system",
            "automatic_braking",
            "braking_subsystem"
        )
        self.de_graph.add_component(sa_comp)
        self.de_graph.add_edge(di_comp.id, sa_comp.id)

    def assess_situation(
        self,
        system: Any,
        situation: Optional[Any] = None
    ) -> SIComponent:
        """Execute situation assessment.

        Args:
            system: The system to assess
            situation: The situation (if None, query KB or designer)

        Returns:
            SIComponent instance
        """
        if situation is None and self.kb:
            situation = self.kb.query_situation(system)

        component = SIComponent(
            id=self._generate_component_id("SI"),
            system=system,
            situation=situation
        )

        self.current_system = system
        self.current_situation = situation

        return component

    def identify_problem(
        self,
        system: Any,
        problem: Optional[Any] = None
    ) -> PIComponent:
        """Execute problem identification.

        Args:
            system: The system with a problem
            problem: The problem (if None, query KB or designer)

        Returns:
            PIComponent instance
        """
        if problem is None and self.kb:
            problem = self.kb.query_problem(system, self.current_situation)

        component = PIComponent(
            id=self._generate_component_id("PI"),
            system=system,
            problem=problem
        )

        self.current_problem = problem

        return component

    def establish_intention(
        self,
        system: Any,
        problem: Any,
        intention: Optional[Any] = None
    ) -> EIComponent:
        """Execute intention establishment.

        Args:
            system: The current system
            problem: The problem to solve
            intention: The intention (if None, query KB or designer)

        Returns:
            EIComponent instance
        """
        if intention is None and self.kb:
            intention = self.kb.query_intention(problem)

        component = EIComponent(
            id=self._generate_component_id("EI"),
            system=system,
            problem=problem,
            intention=intention
        )

        self.current_intention = intention

        return component

    def decompose_intention(
        self,
        system: Any,
        intention: Any,
        sub_intentions: list,
        sub_systems: list
    ) -> DIComponent:
        """Execute intention decomposition.

        Args:
            system: The system to decompose
            intention: The intention to decompose
            sub_intentions: List of sub-intentions
            sub_systems: List of sub-systems

        Returns:
            DIComponent instance
        """
        component = DIComponent(
            id=self._generate_component_id("DI"),
            system=system,
            intention=intention,
            sub_intentions=sub_intentions,
            sub_systems=sub_systems
        )

        return component

    def conditional_branch(
        self,
        system: Any,
        intention: Any,
        situation: Any
    ) -> CBComponent:
        """Execute conditional branching.

        Args:
            system: The current system
            intention: The intention to focus
            situation: The condition

        Returns:
            CBComponent instance
        """
        component = CBComponent(
            id=self._generate_component_id("CB"),
            system=system,
            intention=intention,
            situation=situation
        )

        return component

    def apply_solution(
        self,
        system: Any,
        solution: Any,
        subsystem: Optional[Any] = None
    ) -> SAComponent:
        """Execute solution assignment.

        Args:
            system: The system to apply solution to
            solution: The solution to apply
            subsystem: The resulting subsystem

        Returns:
            SAComponent instance
        """
        if subsystem is None:
            subsystem = f"{system}_{solution}"

        component = SAComponent(
            id=self._generate_component_id("SA"),
            system=system,
            solution=solution,
            subsystem=subsystem
        )

        return component

    def get_graph(self) -> DEGraph:
        """Get the current DE graph."""
        return self.de_graph

    def reset(self):
        """Reset the engine state."""
        self.current_state = State.START
        self.de_graph = DEGraph()
        self.current_system = None
        self.current_situation = None
        self.current_problem = None
        self.current_intention = None
        self.candidate_solutions = []
        self.component_counter = 0
