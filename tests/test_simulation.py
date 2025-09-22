from glacial_cycles.simulation import GlacialSimulation, create_peaks_arr, find_latest_peak_idx
from glacial_cycles.models.state import GlacialStateModel
from glacial_cycles.models.ice_volume import GlacialIceVolumeModel
import numpy as np


def test_create_peak_arr():
    '''
        the create_peaks_arr() functions should find peaks in the data and give the correct indices and values of the peaks
    '''
    data = np.array([0.0,0.5,1.0,0.5,0.0, 0.0,0.3,0.6,0.9,0.6,0.3,0.0, 0.0,0.1,0.2,0.1,0.0])
    peak_ids = np.array([2, 8, 14])
    peak_vals = np.array([1.0, 0.9, 0.2])
    
    peak_ids_test, peak_vals_test = create_peaks_arr(data) 
    assert np.all(peak_ids == peak_ids_test)
    assert np.all(peak_vals == peak_vals_test)

def test_find_latest_peak_idx():
    '''
        The find_latest_peak_idx() function should find the index of the most recent peak given a time in the data excluding the time given
    '''
    data = np.array([0.0,0.5,1.0,0.5,0.0, 0.0,0.3,0.6,0.9,0.6,0.3,0.0, 0.0,0.1,0.2,0.1,0.0])
    peak_ids = np.array([2, 8, 14])
    peak_vals = np.array([1.0, 0.9, 0.2])
    
    peak_ids_test, _ = create_peaks_arr(data) 
   
    test_times = np.array([3, 11, 16])
   
    for i in range(3):
        latest_peak_idx = peak_ids[i]
        latest_peak_val = peak_vals[i]
        t = test_times[i]

        latest_peak_idx_test = find_latest_peak_idx(t, peak_ids_test)
        latest_peak_val_test = data[latest_peak_idx_test] if latest_peak_idx_test is not None else None
        assert latest_peak_idx == latest_peak_idx_test
        assert latest_peak_val == latest_peak_val_test

def test_simulation_runs_and_collects_states():
    time = np.arange(0, 5000, 1000)   # 5 steps
    insolation = np.array([1.0, 0.6, -1.0, -1.0, 1.0])  # should cause transitions

    model = GlacialStateModel(i0=0.0, i1=0.0, i2=-0.5, tg=0)
    sim = GlacialSimulation(model, time, insolation, dt=1000)

    states = sim.run()
    assert len(states) == len(time)
    assert states[0] == "i"  # initial
    assert "g" in states or "G" in states  # at least one transition
