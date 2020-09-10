Feature: The lights must be able to be turned on and off

    Scenario: The lights are controlled
        Given I have a light with the id <light_id>
        And the light <light_id> is turned <light_begin_state>
        And I expect the final state of light <light_id> to be <light_final_state>
        When the lights are connected
        Then I use <light_function> to control the lights
        And I await the result

        Examples: Vertical
            | light_id          | lightbulb-1 | lightbulb-2 |
            | light_begin_state | OFF         | ON          |
            | light_function    | on          | off         |
            | light_final_state | ON          | OFF         |
