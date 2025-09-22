import numpy as np
from glacial_cycles.base_model import BaseGlacialModel
from scipy.signal import find_peaks

def create_peaks_arr(data):
    peak_ids = find_peaks(data)[0]
    peak_vals = data[peak_ids]
    peak_ids = peak_ids
    peak_vals = peak_vals
    peaks_arr = np.array([peak_ids, peak_vals])
    return peaks_arr

def find_latest_peak_idx(t, peaks_arr):
    peak_ids = peaks_arr[0]
    ids = peak_ids - t
    N = np.where(ids < 0)
    if len(ids[N]) != 0:
        prev_peak_idx = int(ids[N][-1]) + t
    else:
        prev_peak_idx = None
    return prev_peak_idx

class GlacialSimulation:
    """
    Runs a climate state simulation given a model and insolation data.
    """
    def __init__(self, model: BaseGlacialModel, time_data: np.ndarray, insolation_data: np.ndarray, dt=1000):
        self.model = model
        self.time_data = time_data
        self.insolation_data = insolation_data
        self.dt = dt
        self.states = []

    def run(self):
        self.states = [self.model.get_state()]  # initial state
        peaks_arr = create_peaks_arr(self.insolation_data)  # assuming you have this helper

        for t in range(1, len(self.time_data)):
            i = self.insolation_data[t]
            ip = self.insolation_data[t - 1]
            prev_peak_idx = find_latest_peak_idx(t, peaks_arr)
            ip_max = self.insolation_data[prev_peak_idx]

            new_state = self.model.step(i, ip, ip_max, dt=self.dt)
            self.states.append(new_state)

        return np.array(self.states)

