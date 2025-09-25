import numpy as np
from typing import Dict, List, Optional, Callable, Any
from .models.base import BaseGlacialModel
from .utils import create_peaks_arr, find_latest_peak_idx

class GlacialSimulation:
    """
    Simulation engine for glacial cycle models.
    Simulate a glacial model, with given time and insolation data and parameter schedules.

    Notes
    -----
    - Simulation is agnostic to the specific glacial model (Strategy pattern).
    - `param_schedules` allows dynamic modification of model parameters during the run.
    """
    model : BaseGlacialModel
    """The glacial model to simulate."""
    time_data : np.ndarray
    """Array of time points."""
    insolation_data : np.ndarray
    """Insolation values corresponding to `time_data`."""
    param_schedules: Optional[Dict[str, Callable[[int], Any]]]
    """Dictionary of time-dependent parameter functions."""
    results : List[Dict[str, Any]] 
    """Array of model outputs at each time step."""

    def __init__(
        self,
        model: BaseGlacialModel,
        time_data: np.ndarray,
        insolation_data: np.ndarray,
        param_schedules: Optional[Dict[str, Callable[[int], Any]]] = None
    ):
        self.model = model
        self.time_data = time_data
        self.insolation_data = insolation_data
        self.results = []
        self.param_schedules = param_schedules or {}

    def run(self, verbose:Optional[bool] = None):
        """Run the simulation over the time and insolation data.

        Parameters
        ----------
        - verbose : Optional[bool]
            If True, print model state after each step."""
       
        self.results.append(self.model.get_data())
        peak_ids, _ = create_peaks_arr(self.insolation_data)
        param_schedules = self.param_schedules or {}
        verbose = verbose or False
        if verbose: print(self.model.get_data())

        for t in range(1, len(self.time_data)):
            i = self.insolation_data[t]
            ip = self.insolation_data[t - 1]
            prev_peak_idx = find_latest_peak_idx(t, peak_ids)
            ipp = self.insolation_data[prev_peak_idx] if prev_peak_idx is not None else None

            step_result = self.model.step(
                insolation=i,
                insolation_previous=ip,
                insolation_previous_peak=ipp,
            )
            self.results.append(step_result)
            if verbose: print(self.model.get_data())
            
            for param, fn in param_schedules.items():
                if hasattr(self.model, param):
                    setattr(self.model, param, fn(t))
                else:
                    raise ValueError(f"GlacialSimulation.run(): {type(self.model)} doesn't have attribute {param} in GlacialSimulation param_schedules.")


        return np.array(self.results)
