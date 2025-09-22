from glacial_cycles.base_model import BaseGlacialModel
import numpy as np

# Function that calculates the truncation function for the forcing
def f(x, a = 1):
    f = 1/2 * (x + np.sqrt(4 * a**2 + x**2))
    return f

# differential function for use in RK4
def ice_vol_diff(F, vR, τR, τF, dt):
    def dvdt(v, t):
        return ((vR - v)/τR - F/τF) * dt
    return dvdt

def RK4_step(df, v, t, dt):
    k1 = df(v, t)
    k2 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k3 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k4 = df(v + dt*k2, t + dt)
    v = v + (1/6)*dt*(k1 + 2*k2 + 2*k3 + k4)
    return v

class GlacialIceVolumeModel(BaseGlacialModel):
    """
    Glacial model based on Paillard (1998)

    The insolation should be truncated
    using the function f(x) = 1/2 [x + sqrt(4a**2 + x**2)]
    and normalized before passed to this model
    """
    def __init__(self, model_number, **params):
        self.model_number = model_number
        self.i0 = params.get('i0')
        self.i1 = params.get('i1')
        self.v = params.get('v0', 0.0)
        self.vR = params.get('vR', 0.0)
        self.τR = params.get('τR', 10.0) 
        self.τF = params.get('τF', 25.0)
        self.vmax = params.get('vmax', 1.0)
        self.state = params.get('init_state', 'i')

    def update_state(self, insolation):
        # i to g transition is insolation is less than i0
        if self.state == 'i' and insolation < self.i0:
            self.state = 'g'

        # g to G transition if the ice volume larger than vmax
        elif self.state == 'g' and self.v > self.vmax:
            self.state = 'G'

        # G to i transition if the insolation is above i1
        elif self.state == 'G' and insolation > self.i1:
            self.state = 'i'
        return

    def step(self, **kwargs):
        insolation = kwargs['insolation'] 
        dt = kwargs.get('dt', 1)
        dvdt = ice_vol_diff(insolation, self.vR, self.τR, self.τF, dt)
        self.v = RK4_step(dvdt, self.v, 0, dt)
        self.update_state(insolation)
        return self.state

    def get_state(self):
        return self.state

