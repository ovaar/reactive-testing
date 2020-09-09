Feature: The lights must be able to be turned on and off

    Scenario: The lights are turned on
        Given I have a light with the id <light_id>
        And the light <light_id> is turned off
        And I expect the light <light_id> state to be <light_state>
        When the lights are connected
        Then I turn on the lights
        And I await the result

        Examples: Vertical
            | light_id    | lightbulb-1 |
            | light_state | on          |
