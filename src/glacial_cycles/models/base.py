from abc import ABC, abstractmethod

class BaseGlacialModel(ABC):
    """
    Abstract base class for glacial cycle models.
    All models must implement `step` and `get_state`.
    """

    @abstractmethod
    def step(self, **kwargs) -> str:
        """
        Advance the model one time step.
        Returns the current state ('i', 'g', or 'G').
        """
        pass

    @abstractmethod
    def get_state(self) -> str:
        """
        Return the current state of the model.
        """
        pass

