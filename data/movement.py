
from enum import IntEnum


class MovementSpeed:
    WALK = 2    # Original FF6 walk speed
    SPRINT = 3  # Original FF6 sprint speed
    DASH = 4    # Custom, move twice as fast as sprint.

class MovementActions(IntEnum):
    # WALK by default
    # SPRINT with sprint shoes equipped
    ORIGINAL = 'og'
    # SPRINT by default
    # WALK when holding B
    AUTO_SPRINT = 'as'
    # SPRINT by default
    # DASH when holding B
    B_DASH = 'bd'
    # SPRINT by default
    # DASH when holding B with sprint shoes equipped
    # WALK when holding B without sprint shoes equipped
    SPRINT_SHOES_B_DASH = 'ssbd'

    ALL = [ORIGINAL, AUTO_SPRINT, B_DASH, SPRINT_SHOES_B_DASH]
