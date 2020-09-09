

from typing import List
import os
import pytest
import asyncio
import lighting.base.src.mqtt as Mqtt
import lighting.integration_tests.tests.data as Data
import lighting.integration_tests.tests.simulator as Simulator
import lighting.integration_tests.tests.listener as Listener
from rx import Observable as RxObservable


@pytest.fixture(scope="session")
def loop():
    print('create: loop')
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    yield _loop
    _loop.close()
    print('exit: loop')


@pytest.fixture
def awaitables(loop):
    print('create: awaitables')
    _awaitables: List[RxObservable] = []
    yield _awaitables
    _awaitables.clear()
    print('after: awaitables')


@pytest.fixture()
def create_simulator():
    simulators: List[Simulator.LightbulbSimulator] = list()

    def _create_simulator() -> Simulator.LightbulbSimulator:
        print('create: simulator')
        _simulator = Simulator.LightbulbSimulator()
        simulators.append(_simulator)
        return _simulator

    yield _create_simulator

    for s in simulators:
        s.exit()


@pytest.fixture(scope="session")
def mqttc():
    _mqttc = Mqtt.Client("lighting.integration-test")
    host: str = os.getenv('MQTT_HOST', 'lighting-message-broker')
    port: int = int(os.getenv('MQTT_PORT', 1883))

    _mqttc.connect(host, port)
    _mqttc.loop_start()

    yield _mqttc

    _mqttc.loop_stop()
    _mqttc.disconnect()


@pytest.fixture(scope="session")
def listener(mqttc):
    return Listener.ReactiveListener(mqttc)


@pytest.fixture
def create_observables():
    observables: List[Data.Observables] = list()

    def _create_observables() -> Data.Observables:
        print('create: observables')
        _observables = Data.Observables()
        observables.append(_observables)
        return _observables

    yield _create_observables

    for o in observables:
        o.complete()
    print('exit: observables')


@pytest.fixture
def test_context(loop, listener, awaitables):
    """
    This fixtures needs to hold references to all session fixtures
    to ensure the lifetime of all objects throughout the test.
    >>>> DO NOT MODIFY PARAMETERS <<<<
    """
    test_context = Data.TestContext()
    listener.set_test_context(test_context)
    return test_context
