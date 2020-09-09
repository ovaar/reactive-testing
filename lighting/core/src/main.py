from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Callable, List, Optional
import os
import re
import signal
import lighting.base.src.mqtt as Mqtt
import lighting.base.src.structs as Structs
import lighting.core.src.handler as Handler
import lighting.core.src.context as Context

if TYPE_CHECKING:
    import paho.mqtt.client as mqtt


def main():
    client = Mqtt.Client('lights-core')
    context = Context.ApplicationContext()
    message_handler = Handler.MessageHandler(context, client)
    dict_topic_callback: Dict[str, Callable[[str, str, List[str]], None]] = {
        'lights/connect/+': message_handler.on_lights_connected,
        'lights/+/state': message_handler.on_lights_state,
        'lights/function/on': message_handler.on_lights_function_on
    }
    list_topics: List[str] = dict_topic_callback.keys()

    def to_regex(topic: str) -> str:
        return f"^{topic.replace('+', '(.*?)')}$"

    list_re_topics: List[str] = list(map(to_regex, list_topics))

    def signal_handler(sig: int, frame):
        client.loop_stop()
        client.disconnect()

    def on_connect(client, userdata, flags, rc):
        print("Core::on_connect Connected with result code "+str(rc))
        # Subscribe to lights topics
        for topic in list_topics:
            print(f'Core::Subscribe to topic={topic}')
            client.subscribe(topic, qos=1)

    def on_message(client, userdata, msg: mqtt.MQTTMessage) -> None:
        print(f"Core::on_message topic={msg.topic} payload={msg.payload}")
        regex: str = ''
        index: int = 0
        try:
            for re_topic in list_re_topics:
                if re.match(re_topic, msg.topic) is not None:
                    regex = re_topic
                    break
                index += 1

            callback = list(dict_topic_callback.values())[index]
            match = re.search(regex, msg.topic)

            if (match is None):
                callback(msg.topic, msg.payload, [])
                return

            args: List[str] = list(match.groups())
            callback(msg.topic, msg.payload, args)
        except Exception as e:
            print(f'Exception: {str(e)}')

    host: str = os.getenv('MQTT_HOST', 'lighting-message-broker')
    port: int = int(os.getenv('MQTT_PORT', 1883))

    client.set_on_connect(on_connect)
    client.set_on_message(on_message)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    print(f'Core::main connecting to: {host}:{port}')
    client.connect(host, port, 60)
    client.loop_forever()


if __name__ == "__main__":
    print("Lighting::main")
    main()
