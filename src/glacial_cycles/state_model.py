from glacial_cycles.base_model import BaseGlacialModel

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
        self.tc = 0 # Time since last state change in yrs
        self.state = 'i' # Starts in interglacial

    def step(self, **kwargs): 
        i = kwargs['insolation']
        ip = kwargs.get('insolation_previous', i)
        ip_max = kwargs.get('insolation_previous_peak', None)
        dt = kwargs.get('dt', 1000)
        self.tc += dt

        # i to g transition if insolation is less than i0 and the previous insolation was greater than i0
        if self.state == 'i' and i < self.i0 and ip > self.i0:
            self.state = 'g'; self.tc = 0
        
        # g to G transition if the time since last state change is greater than ice sheet growth time tg AND if the insolation is less than i2
        elif self.state == 'g' and self.tc > self.tg and i < self.i2 and ip <= self.i2 and (ip_max < self.i3 or ip_max is None):
            self.state = 'G'; self.tc = 0

        # G to i transition if the insolation is above i1
        elif self.state == 'G' and i > self.i1:
            self.state = 'i'; self.tc = 0

        return self.state

    def get_state(self):
        return self.state
            
        


