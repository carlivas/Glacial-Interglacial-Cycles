from .base import BaseGlacialModel

class GlacialStateModel(BaseGlacialModel):
    '''
    Glacial state model based on Paillard (1998).

    States:
        - i: interglacial
        - g: mild glacial
        - G: full glacial

    Transitions follow threshold rules depending on insolation and time since last change.
    '''
    def __init__(self, i0=-0.75, i1=0.0, i2=0.0, i3=1.0, tg=33_000):
        self.i0, self.i1, self.i2, self.i3, self.tg = i0, i1, i2, i3, tg
        self.tc = 0
        self.state = 'i'  # interglacial

    def update_state(self, insolation, insolation_previous, insolation_previous_peak):
        i = insolation
        ip = insolation_previous
        ipp = insolation_previous_peak

        if self.state == 'i' and i < self.i0 and ip > self.i0:
            self.state, self.tc = 'g', 0
        elif self.state == 'g' and self.tc > self.tg and i < self.i2 and ip <= self.i2 and (ipp is None or ipp < self.i3):
            self.state, self.tc = 'G', 0
        elif self.state == 'G' and i > self.i1:
            self.state, self.tc = 'i', 0
        return


    def step(self, **kwargs) -> str:
        i = kwargs['insolation']
        ip = kwargs.get('insolation_previous', i)
        ipp = kwargs.get('insolation_previous_peak', None)
        dt = kwargs.get('dt', 1000)
        self.tc += dt
    
        self.update_state(i, ip, ipp)

        return self.state

    def get_state(self) -> str:
        return self.state
