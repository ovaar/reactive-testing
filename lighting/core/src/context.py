from typing import Dict
import lighting.base.src.enum as Enum


class ApplicationContext(object):
    lights: Dict[str, Enum.LIGHTS_STATE]

    def __init__(self):
        self.lights = dict()
