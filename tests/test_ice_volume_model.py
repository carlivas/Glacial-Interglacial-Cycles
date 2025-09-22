from glacial_cycles.ice_volume_model import GlacialIceVolumeModel

def test_initial_state_is_interglacial():
    '''
    The GlacialIceVolumeModel should always start in the interglacial ('i') state after initialization
    '''
    model = GlacialIceVolumeModel()
    assert model.state == "i"

def test_transition_to_glacial():
    '''
    The GlacialIceVolumeModel should transition from the interglacial to mild glacial when
    insolation < i0:
    '''
    model = GlacialIceVolumeModel(i0=0.5)  # ensure threshold is easy to trigger
    state = model.step(insolation=0.0, v=0.0)
    assert state == "g"

def test_transition_to_full_glacial():
    '''
    The GlacialIceVolumeModel should transition from the mild to full glacial state when
    v > vmax:
    '''
    model = GlacialIceVolumeModel(vmax=1.0)
    # First push to mild glacial
    model.state = "g"
    state = model.step(insolation=0.0, v=2.0)
    assert state == "G"

def test_transition_back_to_interglacial():
    '''
    The GlacialIceVolumeModel should transition from the full glacial to interglacial state when
    insolation > i1
    '''
    model = GlacialIceVolumeModel(i1=-1.0)
    model.state = "G"
    state = model.step(insolation=0.0, v=0.0)
    assert state == "i"

