
from typing import Callable, Optional, Any
import paho.mqtt.client as mqtt

OnConnectCallback = Optional[Callable[[Any, Any, Any, Any], None]]
OnMessageCallback = Optional[Callable[[Any, Any, Any], None]]


class Client(object):
    _client: mqtt.Client

    def __init__(self, client_id: str):
        self._client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv311,
            transport="tcp")

    def set_on_connect(self, value: OnConnectCallback):
        self._client.on_connect = value

    def set_on_message(self, value: OnMessageCallback):
        self._client.on_message = value

    def subscribe(self, topic, qos=0, options=None, properties=None):
        self._client.subscribe(topic, qos, options, properties)

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self._client.publish(topic, payload, qos, retain, properties)

    def connect(self, host: str, port: int, keepalive: int = 30):
        self._client.connect(host, port, keepalive)

    def loop_start(self):
        self._client.loop_start()

    def loop_stop(self):
        self._client.loop_stop()

    def loop_forever(self, timeout=1.0, max_packets=1, retry_first_connection=False):
        self._client.loop_forever(timeout, max_packets, retry_first_connection)

    def disconnect(self):
        self._client.disconnect()
