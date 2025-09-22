from abc import ABC, abstractmethod

class BaseGlacialModel(ABC):
    """
    Abstract base class for glacial cycle models.
    All models must implement `step` and optionally provide state info.
    """

    @abstractmethod
    def step(self, **kwargs):
        """
        Advance the model one time step.
        Returns the current state (e.g., 'i', 'g', 'G' or 0/1/2).
        """
        pass

    @abstractmethod
    def get_state(self):
        """
        Return the current state of the model.
        """
        pass

