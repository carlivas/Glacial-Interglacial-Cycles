import numpy as np

class ClimateStateModel:
    def _init_(self, i0=-0.75, i1=0, i2=0, i3=1, tg=33_000):
        self.i0, self.i1, self.i2, self.i3, self.tg = i0, i1, i2, i3, tg
        self.tc = 0 # Time since last state change
        self.state = 'i' # Starts in interglacial


    def step(self, insolation, insolation_previous, insolation_previous_peak, dt=1000):
        i, ip, ip_max = insolation, insolation_previous, insolation_previous_peak
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
            
        


