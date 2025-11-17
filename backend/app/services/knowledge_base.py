"""Knowledge Base for design exploration."""

from typing import Any, Dict, List, Optional


class KnowledgeBase:
    """Knowledge base for storing domain knowledge and design patterns.

    This class provides queries for situations, problems, intentions,
    solutions, and decompositions during design exploration.
    """

    def __init__(self):
        """Initialize knowledge base with predefined data."""
        self._situations = {}
        self._problems = {}
        self._intentions = {}
        self._solutions = {}
        self._decompositions = {}

        # Load default knowledge
        self._load_collision_avoidance_knowledge()

    def _load_collision_avoidance_knowledge(self):
        """Load knowledge for collision avoidance system example."""

        # Situations
        self._situations = {
            "car_running": "obstacle_detected",
            "auto_maneuvering_system": "normal_driving",
            "human_maneuvering_system": "low_visibility",
        }

        # Problems
        self._problems = {
            ("car_running", "obstacle_detected"): "collision_risk",
            ("human_maneuvering_system", "low_visibility"): "visibility_impaired",
        }

        # Intentions
        self._intentions = {
            "collision_risk": "avoid_collision",
            "visibility_impaired": "support_driver_in_low_visibility",
        }

        # Decompositions
        self._decompositions = {
            ("car_running", "avoid_collision"): {
                "intentions": ["avoid_by_car", "avoid_by_driver"],
                "systems": ["auto_maneuvering_system", "human_maneuvering_system"]
            },
            ("human_maneuvering_system", "support_driver_in_low_visibility"): {
                "intentions": ["alarm_obstacle", "guide_maneuvering"],
                "systems": ["obstacle_alarming_system", "maneuvering_guiding_system"]
            },
        }

        # Solutions
        self._solutions = {
            "auto_maneuvering_system": ["automatic_braking", "automatic_steering"],
            "obstacle_alarming_system": ["visual_alarm", "audio_alarm"],
            "maneuvering_guiding_system": ["haptic_feedback", "visual_guidance"],
        }

    def query_situation(self, system: Any) -> Optional[str]:
        """Query situation for a given system.

        Args:
            system: The system to query

        Returns:
            Situation string or None
        """
        return self._situations.get(str(system))

    def query_problem(self, system: Any, situation: Any) -> Optional[str]:
        """Query problem for a given system and situation.

        Args:
            system: The system
            situation: The situation

        Returns:
            Problem string or None
        """
        key = (str(system), str(situation))
        return self._problems.get(key)

    def query_intention(self, problem: Any) -> Optional[str]:
        """Query intention for a given problem.

        Args:
            problem: The problem to solve

        Returns:
            Intention string or None
        """
        return self._intentions.get(str(problem))

    def query_decomposition(
        self,
        system: Any,
        intention: Any
    ) -> Optional[Dict[str, List[str]]]:
        """Query decomposition for a given system and intention.

        Args:
            system: The system to decompose
            intention: The intention to decompose

        Returns:
            Dictionary with 'intentions' and 'systems' lists
        """
        key = (str(system), str(intention))
        return self._decompositions.get(key)

    def query_solutions(self, intention: Any) -> List[str]:
        """Query available solutions for a given intention.

        Args:
            intention: The intention to solve

        Returns:
            List of solution strings
        """
        # Search through solutions to find matches
        for system, solutions in self._solutions.items():
            if str(intention).lower() in system.lower():
                return solutions
        return []

    def add_situation(self, system: str, situation: str):
        """Add a situation to the knowledge base."""
        self._situations[system] = situation

    def add_problem(self, system: str, situation: str, problem: str):
        """Add a problem to the knowledge base."""
        self._problems[(system, situation)] = problem

    def add_intention(self, problem: str, intention: str):
        """Add an intention to the knowledge base."""
        self._intentions[problem] = intention

    def add_decomposition(
        self,
        system: str,
        intention: str,
        sub_intentions: List[str],
        sub_systems: List[str]
    ):
        """Add a decomposition to the knowledge base."""
        self._decompositions[(system, intention)] = {
            "intentions": sub_intentions,
            "systems": sub_systems
        }

    def add_solutions(self, system: str, solutions: List[str]):
        """Add solutions to the knowledge base."""
        self._solutions[system] = solutions

    def get_all_systems(self) -> List[str]:
        """Get all known systems."""
        systems = set()
        systems.update(self._situations.keys())
        for decomp in self._decompositions.values():
            systems.update(decomp["systems"])
        systems.update(self._solutions.keys())
        return sorted(list(systems))

    def get_all_situations(self) -> List[str]:
        """Get all known situations."""
        return sorted(list(set(self._situations.values())))

    def get_all_problems(self) -> List[str]:
        """Get all known problems."""
        return sorted(list(set(self._problems.values())))

    def get_all_intentions(self) -> List[str]:
        """Get all known intentions."""
        intentions = set(self._intentions.values())
        for decomp in self._decompositions.values():
            intentions.update(decomp["intentions"])
        return sorted(list(intentions))

    def to_dict(self) -> Dict[str, Any]:
        """Export knowledge base as dictionary."""
        return {
            "situations": self._situations,
            "problems": {f"{k[0]},{k[1]}": v for k, v in self._problems.items()},
            "intentions": self._intentions,
            "decompositions": {
                f"{k[0]},{k[1]}": v for k, v in self._decompositions.items()
            },
            "solutions": self._solutions,
        }
