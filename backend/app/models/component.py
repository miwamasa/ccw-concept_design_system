"""Component base classes and types for the Concept Design Support System."""

from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ComponentType(str, Enum):
    """Component type enumeration."""

    # DE Components (Design Exploration)
    SI = "SituationAssessment"
    PI = "ProblemIdentification"
    EI = "EstablishIntention"
    DI = "DecomposeIntention"
    CB = "ConditionalBranch"
    SA = "SolutionAssignment"

    # SI Components (Systems Integration)
    CND = "Condition"
    BUP = "Backups"
    COL = "Collaboration"
    ALT = "Alternative"
    EXO = "Exclusive"


class PortDirection(str, Enum):
    """Port direction enumeration."""
    INPUT = "input"
    OUTPUT = "output"


class Port(BaseModel):
    """Port class for component connections."""

    name: str
    data_type: str = "Any"
    direction: PortDirection
    connection: Optional[str] = None  # Connected port ID

    def connect(self, other_port_id: str) -> None:
        """Connect to another port."""
        self.connection = other_port_id


class Component(BaseModel):
    """Base component class."""

    id: str
    type: ComponentType
    input_ports: Dict[str, Port] = Field(default_factory=dict)
    output_ports: Dict[str, Port] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True

    def add_input_port(self, port: Port) -> None:
        """Add an input port."""
        self.input_ports[port.name] = port

    def add_output_port(self, port: Port) -> None:
        """Add an output port."""
        self.output_ports[port.name] = port

    def execute(self) -> Any:
        """Execute the component logic. Override in subclasses."""
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        return self.model_dump(exclude_none=True)

    def __repr__(self) -> str:
        return f"{self.type}(id={self.id})"
