from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import asyncio
import lighting.base.src.enum as Enum
import lighting.base.src.mqtt as Mqtt
import lighting.base.src.structs as Structs
import lighting.integration_tests.tests.data as Data

if TYPE_CHECKING:
    import paho.mqtt.client as mqtt


class LightbulbSimulator(object):
    _mqttc: Mqtt.Client
    _lightbulb: Data.Lightbulb
    _future_connected: asyncio.Future

    def on_connect(self, client, userdata, flags, rc) -> None:
        print("LightbulbSimulator::Connected with result code "+str(rc))
        self._mqttc.subscribe(f'lights/{self._lightbulb.uuid}/state/get')
        self._mqttc.subscribe(f'lights/{self._lightbulb.uuid}/function/on')
        self._mqttc.subscribe(f'lights/{self._lightbulb.uuid}/function/off')

        data = Structs.s_lights_connected(1)
        self._mqttc.publish(f'lights/connect/{self._lightbulb.uuid}', payload=data.to_json(), qos=1, retain=True)
        self._future_connected.set_result(rc)
        print(f'LightbulbSimulator:: Lightbulb={self._lightbulb.uuid} connected')

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage) -> None:
        print(f"LightbulbSimulator::on_message topic={msg.topic} payload={msg.payload}")
        if msg.topic == f'lights/{self._lightbulb.uuid}/state/get':
            payload = Structs.s_lights_state(self._lightbulb.state or 'unknown')
            self._mqttc.publish(f'lights/{self._lightbulb.uuid}/state', payload.to_json())
        elif msg.topic == f'lights/{self._lightbulb.uuid}/function/on':
            self._lightbulb.state = Enum.LIGHTS_STATE.ON.value
            payload = Structs.s_lights_state(self._lightbulb.state)
            self._mqttc.publish(f'lights/{self._lightbulb.uuid}/state', payload.to_json())
        elif msg.topic == f'lights/{self._lightbulb.uuid}/function/off':
            self._lightbulb.state = Enum.LIGHTS_STATE.OFF.value
            payload = Structs.s_lights_state(self._lightbulb.state)
            self._mqttc.publish(f'lights/{self._lightbulb.uuid}/state', payload.to_json())

    async def connect_as(self,
                         host: str,
                         port: int,
                         lightbulb: Data.Lightbulb) -> None:
        self._lightbulb = lightbulb

        self._mqttc = Mqtt.Client(self._lightbulb.uuid)
        self._future_connected = asyncio.Future()
        self._mqttc.set_on_connect(self.on_connect)
        self._mqttc.set_on_message(self.on_message)

        print(f"LightbulbSimulator::connect_as {self._lightbulb.uuid} to {host}:{port}")
        self._mqttc.connect(host, port)
        self._mqttc.loop_start()
        await asyncio.wait_for(self._future_connected, timeout=10.0)

    def exit(self):
        self._mqttc.loop_stop()
        self._mqttc.disconnect()
