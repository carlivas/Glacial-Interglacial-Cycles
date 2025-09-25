from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any

class GlacialState(Enum):
    """
    Enumeration of discrete glacial climate states.

    States
    ------
    - **INTERGLACIAL** (`int`, value=2): Warm interglacial state.
    - **MILD_GLACIAL** (`int`, value=1): Intermediate glacial state.
    - **FULL_GLACIAL** (`int`, value=0): Cold full-glacial state.

    Notes
    -----
    The `__str__` method maps states to short identifiers:
    - INTERGLACIAL → "i"
    - MILD_GLACIAL → "g"
    - FULL_GLACIAL → "G"
    """
    INTERGLACIAL = 2
    MILD_GLACIAL = 1
    FULL_GLACIAL = 0

    def __str__(self):
        return {2: "i", 1: "g", 0: "G"}[self.value]

class BaseGlacialModel(ABC):
    """
    Abstract base class for glacial cycle models.

    All concrete model classes must implement the abstract methods:
    - `step`
    - `get_data`
    - `set_state`

    Properties
    ----------
    state : GlacialState
        The current glacial state (read-only).
    """

    @property
    @abstractmethod
    def state(self) -> GlacialState:
        """Current state (read-only)."""
        pass

    @abstractmethod
    def set_state(self, new_state: GlacialState) -> None:
        """
        Protected method for subclasses to update state.
        Not intended for external use.
        """
        pass

    @abstractmethod
    def step(self, **kwargs) -> Dict[str, Any]:
        """Advance the model one time step and return its data."""
        pass

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """Return the current state and any additional outputs."""
        pass
