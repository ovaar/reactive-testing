from enum import Enum, unique


@unique
class LIGHTS_STATE(Enum):
    UNKNOWN = 'unknown'
    ON = 'on'
    OFF = 'off'
