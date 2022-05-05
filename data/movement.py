# Terminology
#   WALK   - movespeed 3
#   SPRINT - movespeed 4
#   DASH   - movespeed 5
class MovementActions:
    # WALK by default, SPRINT with sprint shoes equipped
    ORIGINAL = 'og'
    # SPRINT by default, WALK when holding B
    AUTO_SPRINT = 'as'
    # SPRINT by default, DASH when holding B
    B_DASH = 'bd'
    # SPRINT by default, DASH when holding B with sprint shoes equipped
    SPRINT_SHOES_B_DASH = 'ssbd'

    ALL = [ORIGINAL, AUTO_SPRINT, B_DASH, SPRINT_SHOES_B_DASH]
