from .base import BaseGlacialModel, GlacialState
from ..utils import ice_vol_diff, RK4_step
import numpy as np
            
class GlacialIceVolumeModel(BaseGlacialModel):
    """
    Glacial model based on Paillard (1998)

    The insolation should be truncated
    using the function f(x) = 1/2 [x + sqrt(4a**2 + x**2)]
    and normalized before passed to this model
    """
    def __init__(self, **params):
        self.i0 = params.get('i0', -0.75)
        self.i1 = params.get('i1', 0.0)
        self.τF = params.get('τF', 25.0)
        self.vmax = params.get('vmax', 1.0)
        self.state_params = params.get('state_params', np.array([[50.0, 1.0],
                                                                 [50.0, 1.0],
                                                                 [10.0, 0.0]]))
        self.vR = params.get('vR', None)
        self.τR = params.get('τR', None)

        self.__v = params.get('v', 0.5)
        self._set_state(params.get('state', GlacialState.INTERGLACIAL))

        if not isinstance(self.__v, float):
            raise ValueError("GlacialIceVolumeModel ice volume is not of type float")
        if not isinstance(self.__state, GlacialState):
            raise ValueError("GlacialIceVolumeModel state is not of type GlacialState")

    @property
    def v(self) -> float:
        """Current ice volume (read-only)."""
        return self.__v

    @v.setter
    def v(self, value: float) -> None:
        if not isinstance(value, float):
            raise ValueError("Ice volume must be a float")
        # if value < 0:
        #     raise ValueError("Ice volume must be non-negative")
        self.__v = value

    @property
    def state(self) -> GlacialState:
        """Current state (read-only, managed internally)."""
        return self.__state

    def _set_state(self, new_state: GlacialState) -> None:
        """Protected method to update state internally."""
        self.τR, self.vR = self.state_params[new_state.value] 
        self.__state = new_state

    def update_state(self, insolation):
        # i to g transition if insolation is less than i0
        if self.state == GlacialState.INTERGLACIAL and insolation < self.i0:
            self._set_state(GlacialState.MILD_GLACIAL)

        # g to G transition if the ice volume larger than vmax
        elif self.state == GlacialState.MILD_GLACIAL and self.v > self.vmax:
            self._set_state(GlacialState.FULL_GLACIAL)

        # G to i transition if the insolation is above i1
        elif self.state == GlacialState.FULL_GLACIAL and insolation > self.i1:
            self._set_state(GlacialState.INTERGLACIAL)

    def step(self, **kwargs):
        insolation = kwargs['insolation'] 
        dvdt = ice_vol_diff(insolation, self.vR, self.τR, self.τF)
        self.v = RK4_step(dvdt, self.v, t=0, dt=1)
        self.update_state(insolation)
        return self.get_data()

    def get_data(self):
        return {"state": self.state, "ice_volume": self.v} 
    
    def print_state(self):
        info = dict(state=str(self.state), ice_vol=f'{self.v:.8f}')
        for key, val in info.items():
            print(f'{key}: {val}', end = ', ')
        print()
