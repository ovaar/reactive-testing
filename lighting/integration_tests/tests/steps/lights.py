from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

import os
import pytest
from pytest_bdd import scenarios, scenario, parsers, given, when, then
import asyncio
import rx.operators as RxOp
from rx.scheduler.eventloop import AsyncIOScheduler
from rx import Observable as RxObservable
import lighting.base.src.enum as Enum
import lighting.integration_tests.tests.data as Data
import lighting.integration_tests.tests.simulator as Simulator


if TYPE_CHECKING:
    import lighting.base.src.structs as Structs
    import lighting.base.src.mqtt as Mqtt


@given('I have a light with the id <light_id>')
def create_light(light_id: str, test_context: Data.TestContext, create_observables):
    assert isinstance(light_id, str)
    observables: Data.Observables = create_observables()
    lightbulb = Data.Lightbulb(light_id, observables)
    test_context.lightbulbs[light_id] = lightbulb


@given('the light <light_id> is turned <light_begin_state>')
def light_is_turned_off(light_id: str,
                        light_begin_state: str,
                        test_context: Data.TestContext):
    assert isinstance(light_id, str)
    assert isinstance(light_begin_state, str)

    lightbulb: Data.Lightbulb = test_context.lightbulbs[light_id]
    lightbulb.state = Enum.LIGHTS_STATE(light_begin_state).value


@when('the lights are connected')
def connect_lights(
        test_context: Data.TestContext,
        create_simulator,
        loop: asyncio.AbstractEventLoop):
    host: str = os.getenv('MQTT_HOST', 'lighting-message-broker')
    port: int = int(os.getenv('MQTT_PORT', 1883))

    # Connect the simulators
    for lightbulb in test_context.lightbulbs.values():
        simulator: Simulator.LightbulbSimulator = create_simulator()

        async def wait_for_connected():
            try:
                await simulator.connect_as(host, port, lightbulb)
            except Exception as e:
                print(str(e))

        loop.run_until_complete(wait_for_connected())


@then('I use <light_function> to control the lights')
def lights_function(light_function: str, mqttc: Mqtt.Client):
    assert isinstance(light_function, str)
    mqttc.publish(f'lights/function/{light_function}')


@given('I expect the final state of light <light_id> to be <light_final_state>')
def light_state_equals(light_id: str,
                       light_final_state: str,
                       test_context: Data.TestContext,
                       loop: asyncio.AbstractEventLoop,
                       awaitables: List[RxObservable]):
    assert isinstance(light_id, str)
    assert isinstance(light_final_state, str)

    def take_while_state(payload: Structs.s_lights_state) -> bool:
        return payload.newState != light_final_state

    timeout_sec = 10.0
    lightbulb: Data.Lightbulb = test_context.lightbulbs[light_id]

    observable: RxObservable = lightbulb.observables.light_state.pipe(
        RxOp.timeout(timeout_sec),
        RxOp.observe_on(scheduler=AsyncIOScheduler(loop)),
        RxOp.take_while(take_while_state, inclusive=True),
    )

    observable.subscribe(
        on_next=lambda i: print(f"on_next: {i}"),
        on_error=lambda e: print(f"on_error: {e}"),
        on_completed=lambda: print("on_completed"),
        scheduler=AsyncIOScheduler(loop)
    )

    awaitables.append(observable)


@then('I await the result')
def await_the_result(awaitables: List[RxObservable], loop: asyncio.AbstractEventLoop):
    if len(awaitables) == 0:
        print('Nothing to await, continuing... ')
        return

    print(f'Awaiting tasks, count={len(awaitables)}')

    async def main():
        await asyncio.gather(*awaitables)

    try:
        print('start: run_until_complete')
        loop.run_until_complete(main())
        awaitables.clear()
    except:
        awaitables.clear()
        raise
