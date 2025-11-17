"""Systems Integration (SI) Components."""

from typing import Any, Dict, List, Optional
from pydantic import Field
from .component import Component, ComponentType, Port, PortDirection


class CNDComponent(Component):
    """Condition component - role division based on situations."""

    type: ComponentType = ComponentType.CND
    subsystems: List[Any] = Field(default_factory=list)
    situations: List[Any] = Field(default_factory=list)
    parent: Optional[Any] = None


    def execute(self) -> Any:
        """Execute conditional integration."""
        return self.parent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "subsystems": self.subsystems,
            "situations": self.situations,
            "parent": self.parent,
            "metadata": self.metadata
        }


class BUPComponent(Component):
    """Backup component - backup relationship between subsystems."""

    type: ComponentType = ComponentType.BUP
    primary: Any
    backups: List[Any] = Field(default_factory=list)
    parent: Optional[Any] = None


    def execute(self) -> Any:
        """Execute backup integration."""
        return self.parent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "primary": self.primary,
            "backups": self.backups,
            "parent": self.parent,
            "metadata": self.metadata
        }


class COLComponent(Component):
    """Collaboration component - subsystems work together."""

    type: ComponentType = ComponentType.COL
    subsystems: List[Any] = Field(default_factory=list)
    parent: Optional[Any] = None


    def execute(self) -> Any:
        """Execute collaboration integration."""
        return self.parent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "subsystems": self.subsystems,
            "parent": self.parent,
            "metadata": self.metadata
        }


class ALTComponent(Component):
    """Alternative component - multiple options available."""

    type: ComponentType = ComponentType.ALT
    subsystems: List[Any] = Field(default_factory=list)
    parent: Optional[Any] = None


    def execute(self) -> Any:
        """Execute alternative integration."""
        return self.parent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "subsystems": self.subsystems,
            "parent": self.parent,
            "metadata": self.metadata
        }


class EXOComponent(Component):
    """Exclusive component - exactly one option must be chosen."""

    type: ComponentType = ComponentType.EXO
    subsystems: List[Any] = Field(default_factory=list)
    parent: Optional[Any] = None


    def execute(self) -> Any:
        """Execute exclusive integration."""
        return self.parent

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "subsystems": self.subsystems,
            "parent": self.parent,
            "metadata": self.metadata
        }
