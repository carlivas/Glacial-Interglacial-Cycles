from .base import BaseGlacialModel
from ..utils import ice_vol_diff, RK4_step
            
class GlacialIceVolumeModel(BaseGlacialModel):
    """
    Glacial model based on Paillard (1998)

    The insolation should be truncated
    using the function f(x) = 1/2 [x + sqrt(4a**2 + x**2)]
    and normalized before passed to this model
    """
    def __init__(self, **params):
        self.i0 = params.get('i0')
        self.i1 = params.get('i1')
        self.vR = params.get('vR', 0.0)
        self.τR = params.get('τR', 10.0) 
        self.τF = params.get('τF', 25.0)
        self.vmax = params.get('vmax', 1.0)
        self.state = params.get('init_state', 'i')

    def update_state(self, insolation, v):
        # i to g transition if insolation is less than i0
        if self.state == 'i' and insolation < self.i0:
            self.state = 'g'

        # g to G transition if the ice volume larger than vmax
        elif self.state == 'g' and v > self.vmax:
            self.state = 'G'

        # G to i transition if the insolation is above i1
        elif self.state == 'G' and insolation > self.i1:
            self.state = 'i'
        return

    def step(self, **kwargs):
        insolation = kwargs['insolation'] 
        v = kwargs['v']
        dt = kwargs.get('dt', 1)
        dvdt = ice_vol_diff(insolation, self.vR, self.τR, self.τF, dt)
        v = RK4_step(dvdt, v, 0, dt)
        self.update_state(insolation, v)
        return self.state

    def get_state(self):
        return self.state

