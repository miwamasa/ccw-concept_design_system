"""Design Exploration (DE) Components."""

from typing import Any, Dict, List, Optional
from pydantic import Field
from .component import Component, ComponentType, Port, PortDirection


class SIComponent(Component):
    """Situation Assessment component."""

    type: ComponentType = ComponentType.SI
    system: Any
    situation: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        # Define ports
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="evaluated_system", data_type="tuple", direction=PortDirection.OUTPUT))

    def execute(self) -> tuple:
        """Execute situation assessment."""
        return (self.system, self.situation)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "situation": self.situation,
            "metadata": self.metadata
        }


class PIComponent(Component):
    """Problem Identification component."""

    type: ComponentType = ComponentType.PI
    system: Any
    problem: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="problem", data_type="Any", direction=PortDirection.OUTPUT))

    def execute(self) -> Any:
        """Execute problem identification."""
        return self.problem

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "problem": self.problem,
            "metadata": self.metadata
        }


class EIComponent(Component):
    """Establish Intention component."""

    type: ComponentType = ComponentType.EI
    system: Any
    problem: Any
    intention: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_input_port(Port(name="problem", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="intention", data_type="Any", direction=PortDirection.OUTPUT))

    def execute(self) -> Any:
        """Execute intention establishment."""
        return self.intention

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "problem": self.problem,
            "intention": self.intention,
            "metadata": self.metadata
        }


class DIComponent(Component):
    """Decompose Intention component."""

    type: ComponentType = ComponentType.DI
    system: Any
    intention: Any
    sub_intentions: List[Any] = Field(default_factory=list)
    sub_systems: List[Any] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_input_port(Port(name="intention", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="sub_intentions", data_type="List", direction=PortDirection.OUTPUT))
        self.add_output_port(Port(name="sub_systems", data_type="List", direction=PortDirection.OUTPUT))

    def execute(self) -> tuple:
        """Execute intention decomposition."""
        return (self.sub_intentions, self.sub_systems)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "intention": self.intention,
            "sub_intentions": self.sub_intentions,
            "sub_systems": self.sub_systems,
            "metadata": self.metadata
        }


class CBComponent(Component):
    """Conditional Branch component."""

    type: ComponentType = ComponentType.CB
    system: Any
    intention: Any
    situation: Any

    def __init__(self, **data):
        super().__init__(**data)
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_input_port(Port(name="intention", data_type="Any", direction=PortDirection.INPUT))
        self.add_input_port(Port(name="situation", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="focused_intention", data_type="tuple", direction=PortDirection.OUTPUT))

    def execute(self) -> tuple:
        """Execute conditional branching."""
        return (self.intention, self.situation)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "intention": self.intention,
            "situation": self.situation,
            "metadata": self.metadata
        }


class SAComponent(Component):
    """Solution Assignment component."""

    type: ComponentType = ComponentType.SA
    system: Any
    solution: Any
    subsystem: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.add_input_port(Port(name="system", data_type="Any", direction=PortDirection.INPUT))
        self.add_input_port(Port(name="solution", data_type="Any", direction=PortDirection.INPUT))
        self.add_output_port(Port(name="subsystem", data_type="Any", direction=PortDirection.OUTPUT))

    def execute(self) -> Any:
        """Execute solution assignment."""
        return self.subsystem

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "system": self.system,
            "solution": self.solution,
            "subsystem": self.subsystem,
            "metadata": self.metadata
        }
