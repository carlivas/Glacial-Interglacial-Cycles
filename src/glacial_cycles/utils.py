from scipy.signal import find_peaks
import numpy as np

# Function that calculates the truncation function for the forcing
def f(x, a = 1):
    f = 1/2 * (x + np.sqrt(4 * a**2 + x**2))
    return f

# differential function for use in RK4
def ice_vol_diff(F, vR, τR, τF):
    def dvdt(v, t):
        return ((vR - v)/τR - F/τF)
    return dvdt

def RK4_step(df, v, t, dt):
    k1 = df(v, t)
    k2 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k3 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k4 = df(v + dt*k2, t + dt)
    v = v + (1/6)*dt*(k1 + 2*k2 + 2*k3 + k4)
    return v

def create_peaks_arr(data):
    peak_ids = find_peaks(data)[0]
    return peak_ids, data[peak_ids]

def find_latest_peak_idx(t, peak_ids):
    ids = peak_ids[peak_ids < t]
    return ids[-1] if len(ids) else None
