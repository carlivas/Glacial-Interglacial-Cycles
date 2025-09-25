from typing import Optional, Dict, Any
from .base import BaseGlacialModel, GlacialState

class GlacialStateModel(BaseGlacialModel):
    """
    Threshold-based glacial cycle model (Paillard, 1998).

    This model tracks only the **discrete glacial state** and evolves it
    based on thresholds applied to insolation and the time since the last
    transition.

    Notes
    -----
    - The `update_state` method evaluates thresholds at each step.
    - The model tracks the time since the last transition (`tc`).

    States
    ------
    - "i" : Interglacial
    - "g" : Mild glacial
    - "G" : Full glacial
    """

    i0: float
    """Threshold for INTERGLACIAL → MILD_GLACIAL transition (default=-0.75)."""
    i1: float
    """Threshold for FULL_GLACIAL → INTERGLACIAL transition (default=0.0)."""
    i2: float
    """Threshold for MILD_GLACIAL → FULL_GLACIAL transition (default=0.0)."""
    i3: float
    """Peak insolation threshold for blocking MILD_GLACIAL → FULL_GLACIAL transitions (default=1.0)."""
    tc: float
    """Counter for time since last transition (default=0.0)."""
    tg: float
    """Minimum duration before FULL_GLACIAL can be entered (default=33)."""
    @property
    def state(self) -> GlacialState:
        """Current glacial state (read-only, set with set_state())."""
        return self.__state


    def __init__(self, **params: Any):
        self.i0 = params.get('i0', -0.75)
        self.i1 = params.get('i1', 0.0)
        self.i2 = params.get('i2', 0.0)
        self.i3 = params.get('i3', 1.0)
        self.tc = params.get('tc', 0.0)
        self.tg = params.get('tg', 33)

        self.__state = GlacialState.INTERGLACIAL
        self.set_state(params.get('state', GlacialState.INTERGLACIAL))

    def set_state(self, new_state: GlacialState) -> None:
        """Protected method to update the glacial state internally."""
        self.__state = new_state

    def update_state(
        self,
        insolation: float,
        insolation_previous: float,
        insolation_previous_peak: Optional[float] = None
    ) -> None:
        """
        Update the glacial state based on insolation thresholds and timing.

        Parameters
        ----------
        - insolation : float
            Current insolation.
        - insolation_previous : float
            Insolation at previous time step.
        - insolation_previous_peak : float, optional
            Value of last insolation peak.
        """
        i, ip, ipp = insolation, insolation_previous, insolation_previous_peak or float('-inf')

        if self.state == GlacialState.INTERGLACIAL and i < self.i0 and ip > self.i0:
            self.set_state(GlacialState.MILD_GLACIAL)
            self.tc = 0
        elif self.state == GlacialState.MILD_GLACIAL and self.tc > self.tg and i < self.i2 and ip <= self.i2 and ipp < self.i3:
            self.set_state(GlacialState.FULL_GLACIAL)
            self.tc = 0
        elif self.state == GlacialState.FULL_GLACIAL and i > self.i1:
            self.set_state(GlacialState.INTERGLACIAL)
            self.tc = 0

    def step(self, **kwargs: Any) -> Dict[str, GlacialState]:
        """
        Advance the model one step.

        Parameters
        ----------
        - insolation : float
            Current insolation (required).
        - insolation_previous : float, optional
            Insolation at previous time step.
        - insolation_previous_peak : float, optional
            Value of last insolation peak.

        Returns
        -------
        - dict
            Current state.
        """
        i = kwargs['insolation']
        ip = kwargs.get('insolation_previous', i)
        ipp = kwargs.get('insolation_previous_peak', None)
        self.tc += 1

        self.update_state(i, ip, ipp)
        return self.get_data()

    def get_data(self) -> Dict[str, GlacialState]:
        """Return current glacial state."""
        return {"state": self.state}

    def print_state(self) -> None:
        """Print a concise summary of the current state."""
        print(f"state: {str(self.state)}")
