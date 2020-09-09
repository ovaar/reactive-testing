import pytest
from pytest_bdd import scenarios, scenario


@scenario(
    feature_name='features/lighting.feature',
    scenario_name='The lights are turned on',
    example_converters=dict(
        light_id=str,
        light_state=str
    ))
def test_turn_on_the_lights():
    pass
