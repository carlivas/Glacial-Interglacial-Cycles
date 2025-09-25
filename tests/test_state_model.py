from glacial_cycles.models.base import GlacialState
from glacial_cycles.models.state import GlacialStateModel

def test_state_model_initial_state_is_interglacial():
    '''
    The ClimateStateModel should always start in the interglacial ('i') state after initialization
    '''
    model = GlacialStateModel()
    assert model.state == GlacialState.INTERGLACIAL

def test_state_model_interglacial_to_mild_glacial():
    '''
    The ClimateStateModel should transition from the interglacial to mild glacial when
    insolation < i0 and insolation_previous > i0
    '''
    model = GlacialStateModel(i0=0.5)  # ensure threshold is easy to trigger
    _ = model.step(insolation=0.0, insolation_previous=1.0, insolation_previous_peak=0.1, dt=1000)
    assert model.state == GlacialState.MILD_GLACIAL

def test_state_model_mild_glacial_to_full_glacial():
    '''
    The ClimateStateModel should transition from the mild to full glacial state when
    tc > tg and insolation < i2 and insolation_previous <= i2 and (insolation_previous_peak < i3 or insolation_previous_peak is None):
    '''
    model = GlacialStateModel(i2=0.0, i3=1.0, tg=0, state = GlacialState.MILD_GLACIAL)
    # First push to mild glacial
    model.tc = 40_000
    _ = model.step(insolation=-1.0, insolation_previous=0.0, insolation_previous_peak=0.5, dt=1000)
    assert model.state == GlacialState.FULL_GLACIAL

def test_state_model_full_glacial_to_interglacial():
    '''
    The ClimateStateModel should transition from the full glacial to interglacial state when
    insolation > i1:
    '''
    model = GlacialStateModel(i1=-1.0, state = GlacialState.FULL_GLACIAL)
    _ = model.step(insolation=0.0, insolation_previous=0, insolation_previous_peak=0, dt=1000)
    assert model.state == GlacialState.INTERGLACIAL

