import pytest
from glacial_cycles.state_model import ClimateStateModel

def test_initial_state_is_interglacial():
    '''
    The ClimateStateModel should always start in the interglacial ('i') state after initialization
    '''
    model = ClimateStateModel()
    assert model.state == "i"

def test_transition_to_glacial():
    '''
    The ClimateStateModel should transition from the interglacial to mild glacial when
    insolation < i0 and insolation_previous > i0
    '''
    model = ClimateStateModel(i0=0.5)  # ensure threshold is easy to trigger
    state = model.step(insolation=0.0, insolation_previous=1.0, insolation_previous_peak=0.1, dt=1000)
    assert state == "g"

def test_transition_to_full_glacial():
    '''
    The ClimateStateModel should transition from the mild to full glacial state when
    tc > tg and insolation < i2 and insolation_previous <= i2 and (insolation_previous_peak < i3 or insolation_previous_peak is None):
    '''
    model = ClimateStateModel(i2=0.0, i3=1.0, tg=0)
    # First push to mild glacial
    model.state = "g"
    model.tc = 40_000
    state = model.step(insolation=-1.0, insolation_previous=0.0, insolation_previous_peak=0.5, dt=1000)
    assert state == "G"

def test_transition_back_to_interglacial():
    '''
    The ClimateStateModel should transition from the full glacial to interglacial state when
    insolation > i1:
    '''
    model = ClimateStateModel(i1=-1.0)
    model.state = "G"
    state = model.step(insolation=0.0, insolation_previous=0, insolation_previous_peak=0, dt=1000)
    assert state == "i"

