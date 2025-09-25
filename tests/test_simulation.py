import numpy as np
from glacial_cycles.simulation import GlacialSimulation 
from glacial_cycles.models.base import GlacialState
from glacial_cycles.models.state import GlacialStateModel
from glacial_cycles.models.ice_volume import GlacialIceVolumeModel

def test_simulation_state_model():
    time = np.arange(0, 5)  # 5 steps
    insolation = np.array([1.0, 0.6, -1.0, -1.0, 1.0])  # should cause transitions

    model = GlacialStateModel(i0=0.0, i1=0.0, i2=-0.5, i3=1.0, tg=0)
    sim = GlacialSimulation(model, time, insolation)

    results = sim.run(verbose=True)
    states = [r["state"] for r in results]
    assert len(states) == len(time)
    assert states[0] == GlacialState.INTERGLACIAL # initial
    assert GlacialState.MILD_GLACIAL in states    # at least one transition
    assert GlacialState.FULL_GLACIAL in states    # at least one transition


def test_simulation_ice_volume_model():
    time = np.arange(0, 5) # 5 steps
    insolation = np.array([0.0, -10.0, -2.0, 0.0, 1.0, 0.0])  # should cause transitions

    model = GlacialIceVolumeModel(i0=-0.75, i1=0.0, v=0.75, vmax = 1.0)
    sim = GlacialSimulation(model, time, insolation)

    results = sim.run(verbose=True)
    states = [r["state"] for r in results]
    assert len(states) == len(time)
    assert states[0] == GlacialState.INTERGLACIAL  # initial
    assert GlacialState.MILD_GLACIAL in states
    assert GlacialState.FULL_GLACIAL in states  # at least one transition
