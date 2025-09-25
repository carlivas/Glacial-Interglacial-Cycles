from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any

class GlacialState(Enum):
    INTERGLACIAL = 2
    MILD_GLACIAL = 1
    FULL_GLACIAL = 0

    def __str__(self):
        return {2: "i", 1: "g", 0: "G"}[self.value]

class BaseGlacialModel(ABC):
    """
    Abstract base class for glacial cycle models.
    All models must implement `step`, `get_data`, and `print_state`.
    """

    @property
    @abstractmethod
    def state(self) -> GlacialState:
        """Current state (read-only)."""
        ...

    @abstractmethod
    def _set_state(self, new_state: GlacialState) -> None:
        """
        Protected method for subclasses to update state.
        Not intended for external use.
        """
        ...

    @abstractmethod
    def step(self, **kwargs) -> Dict[str, Any]:
        """Advance the model one time step and return its data."""
        ...

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """Return the current state and any additional outputs."""
        ...
