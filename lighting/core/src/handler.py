from __future__ import annotations
from typing import TYPE_CHECKING, List

import lighting.base.src.enum as Enum
import lighting.base.src.structs as Structs

if TYPE_CHECKING:
    import lighting.core.src.context as Context
    import lighting.base.src.mqtt as Mqtt


class MessageHandler(object):
    _context: Context.ApplicationContext
    _mqttc: Mqtt.Client

    def __init__(self, context: Context.ApplicationContext, mqttc: Mqtt.Client):
        self._context = context
        self._mqttc = mqttc

    def on_lights_connected(self, topic: str, payload: str, args: List[str]) -> None:
        data = Structs.s_lights_connected.from_json(payload)
        key: str = args[0]
        if data.state == 0:  # Disconnected from the MQTT broker
            del self._context.lights[key]
        if data.state == 1:  # Connected
            self._context.lights[key] = Enum.LIGHTS_STATE.OFF
            print(f'MessageHandler::on_lights_connected publish lights/{key}/state/get')
            self._mqttc.publish(f'lights/{key}/state/get', payload=None, qos=1, retain=True)

    def on_lights_state(self, topic: str, payload: str, args: List[str]) -> None:
        data = Structs.s_lights_state.from_json(payload)
        key: str = args[0]
        self._context.lights[key] = Enum.LIGHTS_STATE(data.newState)
        print(f'MessageHandler::on_lights_state newState={self._context.lights[key]}')

    def on_lights_function_on(self, topic: str, payload: str, args: List[str]) -> None:
        # Set the state
        state = Enum.LIGHTS_STATE.ON.value.lower()
        for light_id in self._context.lights.keys():
            # Publish state change
            print(f'MessageHandler::on_lights_function_on publish topic=lights/{light_id}/function/{state}')
            self._mqttc.publish(f'lights/{light_id}/function/{state}', payload=None, qos=1, retain=True)

    def on_lights_function_off(self, topic: str, payload: str, args: List[str]) -> None:
        # Set the state
        state = Enum.LIGHTS_STATE.OFF.value.lower()
        for light_id in self._context.lights.keys():
            # Publish state change
            print(f'MessageHandler::on_lights_function_off publish topic=lights/{light_id}/function/{state}')
            self._mqttc.publish(f'lights/{light_id}/function/{state}', payload=None, qos=1, retain=True)
