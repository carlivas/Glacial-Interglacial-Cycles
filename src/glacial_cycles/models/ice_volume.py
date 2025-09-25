from typing import Dict, Any, Optional
import numpy as np
from .base import BaseGlacialModel, GlacialState
from ..utils import ice_vol_diff, RK4_step

class GlacialIceVolumeModel(BaseGlacialModel):
    """
    Glacial cycle model with explicit ice volume dynamics (Paillard, 1998).

    The model evolves ice volume using a relaxation scheme with thresholds 
    on insolation and ice volume that govern transitions between glacial states.

    Notes
    -----
    - Insolation forcing should be preprocessed before input:
        - Truncate with `f(x) = 0.5 [x + sqrt(4a² + x²)]` and normalize.
    - Dynamics are integrated using a 4th-order Runge–Kutta (RK4) scheme.
    """
    i0: float
    """Insolation threshold for INTERGLACIAL → MILD_GLACIAL transition (default=-0.75)."""
    i1: float
    """Insolation threshold for FULL_GLACIAL → INTERGLACIAL transition (default=0.0)."""
    τF: float
    """Relaxation timescale for ice volume dynamics (default=25.0)."""
    vmax: float
    """Ice volume threshold for MILD_GLACIAL → FULL_GLACIAL transition (default=1.0)."""
    state_params: np.ndarray
    """State-dependent parameters `[τR, vR]` for each glacial state (shape=(3,2))."""
    vR: Optional[float]
    """Equilibrium ice volume (set by state if not provided)."""
    τR: Optional[float]
    """Relaxation timescale (set by state if not provided)."""
    v: float
    """Current ice volume."""
    @property
    def state(self) -> GlacialState:
        """Current glacial state (read-only)."""
        return self.__state


    def __init__(self, **params: Any):
        self.i0 = params.get("i0", -0.75)
        self.i1 = params.get("i1", 0.0)
        self.τF = params.get("τF", 25.0)
        self.vmax = params.get("vmax", 1.0)
        self.state_params = params.get(
            "state_params", np.array([[50.0, 1.0], [50.0, 1.0], [10.0, 0.0]])
        )
        self.vR = params.get("vR")
        self.τR = params.get("τR")
        self.v = params.get("v", 0.5)
        self.set_state(params.get("state", GlacialState.INTERGLACIAL))

        if not isinstance(self.v, float):
            raise ValueError("Ice volume must be a float")
        if not isinstance(self.__state, GlacialState):
            raise ValueError("State must be of type GlacialState")

    def set_state(self, new_state: GlacialState) -> None:
        """Updates the state and corresponding parameters."""
        self.τR, self.vR = self.state_params[new_state.value]
        self.__state = new_state

    def update_state(self, insolation: float) -> None:
        """
        Update the model state based on current insolation and ice volume.

        Parameters
        ----------
        - insolation : float
            Current insolation value at this time step.
        """
        if self.state == GlacialState.INTERGLACIAL and insolation < self.i0:
            self.set_state(GlacialState.MILD_GLACIAL)
        elif self.state == GlacialState.MILD_GLACIAL and self.v > self.vmax:
            self.set_state(GlacialState.FULL_GLACIAL)
        elif self.state == GlacialState.FULL_GLACIAL and insolation > self.i1:
            self.set_state(GlacialState.INTERGLACIAL)

    def step(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Advance the model by one time step.

        Parameters
        ----------
        - insolation : float
            Insolation forcing at this step (passed via kwargs).

        Returns
        -------
        - data : dict
            Current state and ice volume.
        """
        insolation = kwargs["insolation"]
        dvdt = ice_vol_diff(insolation, self.vR, self.τR, self.τF)
        self.v = RK4_step(dvdt, self.v, t=0, dt=1)
        self.update_state(insolation)
        return self.get_data()

    def get_data(self) -> Dict[str, Any]:
        """Return current state and ice volume."""
        return {"state": self.state, "ice_volume": self.v}

    def print_state(self) -> None:
        """Print a concise summary of the current state and ice volume."""
        info = {"state": str(self.state), "ice_vol": f"{self.v:.8f}"}
        for key, val in info.items():
            print(f"{key}: {val}", end=", ")
        print()
