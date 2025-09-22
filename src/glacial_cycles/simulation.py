# simulation.py
import numpy as np
from .models.base import BaseGlacialModel
from .utils import create_peaks_arr, find_latest_peak_idx

class GlacialSimulation:
    """
    Runs a climate state simulation given a model and insolation data.
    Agnostic to the specific model type (Strategy pattern).
    """
    def __init__(self, model: BaseGlacialModel, time_data: np.ndarray, insolation_data: np.ndarray, dt=1000):
        self.model = model
        self.time_data = time_data
        self.insolation_data = insolation_data
        self.dt = dt
        self.states = []

    def run(self):
        self.states = [self.model.get_state()]
        peak_ids, _ = create_peaks_arr(self.insolation_data)

        for t in range(1, len(self.time_data)):
            i = self.insolation_data[t]
            ip = self.insolation_data[t - 1]
            prev_peak_idx = find_latest_peak_idx(t, peak_ids)
            ipp = self.insolation_data[prev_peak_idx] if prev_peak_idx is not None else None

            new_state = self.model.step(
                insolation=i,
                insolation_previous=ip,
                insolation_previous_peak=ipp,
                dt=self.dt
            )
            self.states.append(new_state)

        return np.array(self.states)
