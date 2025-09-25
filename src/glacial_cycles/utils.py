"""
Utility functions for glacial cycle modeling.

Functions
---------
- f(x, a=1):
    Truncation function for forcing.
- ice_vol_diff(F, vR, τR, τF):
    Returns differential function for ice volume dynamics.
- RK4_step(df, v, t, dt):
    Single step of Runge-Kutta 4 integration.
- create_peaks_arr(data):
    Identify peaks in a time series.
- find_latest_peak_idx(t, peak_ids):
    Find the index of the most recent peak before time `t`.
"""
from scipy.signal import find_peaks
import numpy as np

def f(x, a=1):
    """
    Truncation function for forcing.

    Parameters
    ----------
    - x : float or np.ndarray
        Input value(s).
    - a : float, optional
        Parameter controlling truncation strength (default 1).

    Returns
    -------
    - float or np.ndarray
        Truncated value(s) according to f(x) = 0.5 * (x + sqrt(4a^2 + x^2)).
    """
    f = 1/2 * (x + np.sqrt(4 * a**2 + x**2))
    return f

# differential function for use in RK4
def ice_vol_diff(F, vR, τR, τF):
    """
    Create differential function for ice volume dynamics.

    Parameters
    ----------
    - F : float
        Insolation forcing.
    - vR : float
        Reference ice volume.
    - τR : float
        Relaxation time.
    - τF : float
        Forcing time scale.

    Returns
    -------
    - dvdt : callable
        Function dvdt(v, t) giving ice volume derivative.
    """
    def dvdt(v, t):
        return ((vR - v)/τR - F/τF)
    return dvdt

def RK4_step(df, v, t, dt):
    """
    Perform one Runge-Kutta 4 integration step.

    Parameters
    ----------
    - df : callable
        Differential function dv/dt(v, t).
    - v : float
        Current value.
    - t : float
        Current time.
    - dt : float
        Time step.

    Returns
    -------
    - float
        Updated value after one RK4 step.
    """
    k1 = df(v, t)
    k2 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k3 = df(v + 0.5*dt*k1, t + 0.5*dt)
    k4 = df(v + dt*k2, t + dt)
    v = v + (1/6)*dt*(k1 + 2*k2 + 2*k3 + k4)
    return v

def create_peaks_arr(data):
    """
    Identify peaks in a 1D array.

    Parameters
    ----------
    - data : np.ndarray
        Input data array.

    Returns
    -------
    - peak_ids : np.ndarray
        Indices of peaks.
    - peak_values : np.ndarray
        Values at the peak indices.
    """
    peak_ids = find_peaks(data)[0]
    return peak_ids, data[peak_ids]

def find_latest_peak_idx(t, peak_ids):
    """
    Find the index of the most recent peak before time t.

    Parameters
    ----------
    - t : int
        Current time index.
    - peak_ids : np.ndarray
        Array of peak indices.

    Returns
    -------
    - int or None
        Index of latest peak before t, or None if no previous peak exists.
    """
    ids = peak_ids[peak_ids < t]
    return ids[-1] if len(ids) else None
