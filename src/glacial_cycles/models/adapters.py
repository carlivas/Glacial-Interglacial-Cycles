from .base import BaseGlacialModel

class IceVolumeAdapter(BaseGlacialModel):
    """
    Adapter to make GlacialIceVolumeModel conform to the BaseGlacialModel interface.
    """
    def __init__(self, ice_model):
        self.ice_model = ice_model

    def step(self, **kwargs) -> str:
        return self.ice_model.step(insolation=kwargs['insolation'], dt=kwargs.get('dt', 1))

    def get_state(self) -> str:
        return self.ice_model.get_state()

