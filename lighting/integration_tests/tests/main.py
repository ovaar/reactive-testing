import pytest
from pytest_bdd import scenarios, scenario


@scenario(
    feature_name='features/lighting.feature',
    scenario_name='The lights are controlled',
    example_converters=dict(
        light_id=str,
        light_begin_state=str,
        light_function=str,
        light_final_state=str
    ))
def test_turn_on_the_lights():
    pass
