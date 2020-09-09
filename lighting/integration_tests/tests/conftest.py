import pytest
from lighting.integration_tests.tests.fixtures import *  # noqa # pylint: disable=unused-wildcard-import
from lighting.integration_tests.tests.steps.lights import *  # noqa # pylint: disable=unused-wildcard-import


# -- Debugging - -
# import debugpy

# # Allow other computers to attach to debugpy at this IP address and port.
# debugpy.listen(("0.0.0.0", 5678))

# # Pause the program until a remote debugger is attached
# print("Waiting for debugger to attach on ::5678")
# debugpy.wait_for_client()
# -- Debugging --


def pytest_runtest_setup(item):
    """ Called to perform the setup phase for a test item. """
    print(f"pytest::before {item}")


def pytest_runtest_teardown(item):
    """ Called to perform the teardown phase for a test item. """
    print(f"pytest::after {item}")


@pytest.mark.trylast
def pytest_bdd_before_scenario(request, feature, scenario):
    print(f'Scenario::before: {scenario.name}')


@pytest.mark.trylast
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'FAILED Step: {step.name}')


@pytest.mark.trylast
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print(f'PASSED Step: {step.name}')
