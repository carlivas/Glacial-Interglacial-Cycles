from .base import BaseGlacialModel, GlacialState

class GlacialStateModel(BaseGlacialModel):
    '''
    Glacial state model based on Paillard (1998).

    States:
        - i: interglacial
        - g: mild glacial
        - G: full glacial

    Transitions follow threshold rules depending on insolation and time since last change.
    '''
    def __init__(self, **params):
        self.i0 = params.get('i0', -0.75)
        self.i1 = params.get('i1', 0.0)
        self.i2 = params.get('i2', 0.0)
        self.i3 = params.get('i3', 1.0) 
        self.tc = params.get('tc', 0.0)
        self.tg = params.get('tg', 33)
        
        self.__state = GlacialState.INTERGLACIAL
        self._set_state(params.get('state', GlacialState.INTERGLACIAL))

    @property
    def state(self) -> GlacialState:
        """Current state (read-only, managed internally)."""
        return self.__state

    def _set_state(self, new_state: GlacialState) -> None:
        """Protected method to update state internally."""
        if not isinstance(self.__state, GlacialState):
            raise ValueError("GlacialIceVolumeModel state is not of type GlacialState")
        self.__state = new_state

    def update_state(self, insolation, insolation_previous, insolation_previous_peak):
        i = insolation
        ip = insolation_previous
        ipp = insolation_previous_peak or float('-inf')

        if self.state == GlacialState.INTERGLACIAL and i < self.i0 and ip > self.i0:
            self._set_state(GlacialState.MILD_GLACIAL)
            self.tc = 0
        elif self.state == GlacialState.MILD_GLACIAL and self.tc > self.tg and i < self.i2 and ip <= self.i2 and ipp < self.i3:
            self._set_state(GlacialState.FULL_GLACIAL)
            self.tc = 0
        elif self.state == GlacialState.FULL_GLACIAL and i > self.i1:
            self._set_state(GlacialState.INTERGLACIAL)
            self.tc = 0
        return


    def step(self, **kwargs):
        i = kwargs['insolation']
        ip = kwargs.get('insolation_previous', i)
        ipp = kwargs.get('insolation_previous_peak', None)
        self.tc += 1
    
        self.update_state(i, ip, ipp)

        return self.get_data() 

    def get_data(self):
        return {"state": self.state}

    def print_state(self) -> None:
        info = dict(state=str(self.state))
        for key, val in info.items():
            print(f'{key}: {val}', end = ', ')
        print()
        return
