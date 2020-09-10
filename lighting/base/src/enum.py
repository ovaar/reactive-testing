from enum import Enum, unique


@unique
class LIGHTS_STATE(Enum):
    UNKNOWN = 'UNKNOWN'
    ON = 'ON'
    OFF = 'OFF'
