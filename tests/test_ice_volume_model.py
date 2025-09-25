from glacial_cycles.models.base import GlacialState
from glacial_cycles.models.ice_volume import GlacialIceVolumeModel

def test_ice_volume_model_initial_state_is_interglacial():
    '''
    The GlacialIceVolumeModel should always start in the interglacial ('i') state after initialization
    '''
    model = GlacialIceVolumeModel()
    assert model.state == GlacialState.INTERGLACIAL

def test_ice_volume_model_interglacial_to_glacial():
    '''
    The GlacialIceVolumeModel should transition from the interglacial to mild glacial when
    insolation < i0:
    '''
    model = GlacialIceVolumeModel(i0=0.5, v=0.0)  # ensure threshold is easy to trigger
    _ = model.step(insolation=0.0)
    assert model.state == GlacialState.MILD_GLACIAL

def test_ice_volume_model_mild_glacial_to_full_glacial():
    '''
    The GlacialIceVolumeModel should transition from the mild to full glacial state when
    v > vmax:
    '''
    model = GlacialIceVolumeModel(state = GlacialState.MILD_GLACIAL, vmax=1.0, v=2.0)
    # First push to mild glacial
    _ = model.step(insolation=0.0)
    assert model.state == GlacialState.FULL_GLACIAL

def test_ice_volume_model_full_glacial_to_interglacial():
    '''
    The GlacialIceVolumeModel should transition from the full glacial to interglacial state when
    insolation > i1
    '''
    model = GlacialIceVolumeModel(state = GlacialState.FULL_GLACIAL, i1=-1.0, v=0.0)
    _ = model.step(insolation=0.0)
    assert model.state == GlacialState.INTERGLACIAL

