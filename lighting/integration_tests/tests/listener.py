from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import re
import lighting.base.src.mqtt as Mqtt
import lighting.base.src.structs as Structs
import lighting.integration_tests.tests.data as Data

if TYPE_CHECKING:
    import paho.mqtt.client as mqtt

LIGHTS_STATE_RE = "lights/(.*?)/state"


class ReactiveListener(object):
    _mqttc: Mqtt.Client
    _test_context: Optional[Data.TestContext] = None

    def __init__(self, mqttc: Mqtt.Client):
        self._mqttc = mqttc
        self._mqttc.set_on_connect(self.on_connect)
        self._mqttc.set_on_message(self.on_message)

    def set_test_context(self, test_context: Optional[Data.TestContext]):
        self._test_context = test_context

    def on_connect(self, client, userdata, flags, rc) -> None:
        print("ReactiveListener::on_connect Connected with result code "+str(rc))
        self._mqttc.subscribe(f'lights/+/state')

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage) -> None:
        print(f"ReactiveListener::on_message topic={msg.topic} payload={msg.payload}")
        if self._test_context is None:
            raise RuntimeError('Undefined reference _test_context')

        if match := re.search(LIGHTS_STATE_RE,  msg.topic):
            light_id = match.group(1)
            data = Structs.s_lights_state.from_json(msg.payload)
            lightbulb: Data.Lightbulb = self._test_context.lightbulbs[light_id]
            lightbulb.light_state.on_next(data)
