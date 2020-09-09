from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class s_lights_connected(DataClassJsonMixin):
    state: int


@dataclass
class s_lights_set(DataClassJsonMixin):
    value: bool


@dataclass
class s_lights_state(DataClassJsonMixin):
    newState: str
