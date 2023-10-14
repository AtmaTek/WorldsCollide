from enum import Flag, unique, auto
@unique
class RewardType(Flag):
    NONE = auto()
    CHARACTER = auto()
    ESPER = auto()
    ITEM = auto()

CHARACTER_ESPER_ONLY_REWARDS = 6
class Reward:
    def __init__(self, event, possible_types):
        self.id = None
        self.type = None
        self.event = event
        self.possible_types = possible_types

    def single_possible_type(self):
        return self.possible_types in RewardType

    def __str__(self):
        result = f"{self.id} {self.type} {self.event.name()}"

        possible_strings = []
        if self.possible_types & RewardType.CHARACTER:
            possible_strings.append("Character")
        if self.possible_types & RewardType.ESPER:
            possible_strings.append("Esper")
        if self.possible_types & RewardType.ITEM:
            possible_strings.append("Item")

        return result + " (" + ', '.join(possible_strings) + ")"

def choose_reward(possible_types, characters, espers, items):
    import random

    all_types = [flag for flag in RewardType]
    random.shuffle(all_types)

    item_possible = False
    for reward_type in all_types:
        if reward_type & possible_types:
            if reward_type == RewardType.CHARACTER and characters.get_available_count():
                return (characters.get_random_available(), reward_type)
            elif reward_type == RewardType.ESPER and espers.available():
                return (espers.get_random_esper(), reward_type)
            elif reward_type == RewardType.ITEM:
                item_possible = True

    # tried all possible_rewards and none were available
    # probably running out of chars and espers and need to make item rewards possible for more events
    assert(item_possible)
    return (items.get_good_random(), RewardType.ITEM)

# Documentation from AtmaTek:
# The main idea for gating is that we have y characters that we want to distribute amongst x checks with equal probability while also guaranteeing a path between them. The natural approach is to take our starting character(s), put the checks they unlock into a pool, pick a check at random from the pool, assign a character to it then put that character's checks into the pool and repeat until all characters have been assigned. This is basically the approach WC takes (and I assume what other gating randomizers do as well).
# However, there is a problem. We guaranteed a path but the x original checks no longer all have an equal probability of being assigned a character in a single seed. I think the easiest way to picture it is to imagine you have a bag with a red marble and a blue marble. You pick one at random so both red and blue have a 50/50 chance. Let's say you pick blue then take it out and replace it with yellow. Now you pick again with a 50% chance of red and a 50% chance of yellow. However, red has now had 2 chances to be picked with 50% odds while yellow has only had 1 chance. This means that checks which were unlocked by characters assigned by the algorithm earlier will have a higher chance of rewarding a character than checks unlocked by characters assigned later. In other words, the checks unlocked by the first character had many more chances to be picked than the checks unlocked by the 13th character.

# Broadly speaking, for a randomizer with a gating mechanic and decently balanced checks (never really true, but something many believe should be a goal), a breadth-first-search is the optimal approach to unlocking gates.
# I am not sure if/how other randomizers handle this (and would be interested in learning). However, in an attempt to compensate, the WC code at line 53 in event_reward.py instead picks the "marbles" with a weighting based on how long they have been in the "bag". So instead of 50/50 red and yellow, red will now have lower odds than yellow. With the given algorithm, it is not possible to make them entirely equally weighted because a decision has already been made by the time yellow is added. Instead, I somewhat arbitrarily opted to make new "marbles" twice as likely so red will have 33% chance and yellow 66%.
# My hope is that in practice (when combined with the unequal value of some checks and real-time opportunities like checks a player is already close to) this compensation is enough to offset the breadth-first-search skew. If it ever becomes a more serious issue then the compensation can be adjusted or entirely new approaches may be possible (like possibly finding a new algorithm with a depth-first-search skew and randomly choosing between them).


# weight reward slots based on how long they have been in the reward pool (longer means lower odds)
# the first events unlocked will have more chances to be picked, this balances it somewhat by lowering their odds each time they aren't picked
# specifically, when an event is added to the pool it is twice as likely to be picked as an event added in the previous iteration
# e.g. 4 slots in pool, a has been in for 2 picks, b has been in for 1 pick and c,d have been in for 0 picks
# a should have half the weight of b which should have half the weight of c and d
# a + b + c + d = 1.0
# a + 2a + 4a + 4a = 1.0        11a = 1.0   a = 0.0909
# 0.5b + b + 2b + 2b = 1.0     5.5b = 1.0   b = 0.1818
# 0.25c + 0.5c + c + c = 1.0  2.75c = 1.0   c = 0.3636 # and same for d
def reward_slot_weight(slot_iterations, slot, iteration):
    csum = 0
    cmod = 2**(iteration - slot_iterations[slot])
    for s in slot_iterations:
        csum += 2**(iteration - s) / cmod
    return 1 / csum

# generate weights for each slot based on its number of iterations
def reward_slot_weights(slot_iterations, iteration):
    slot_weights = []
    for x in range(len(slot_iterations)):
        slot_weights.append(reward_slot_weight(slot_iterations, x, iteration))
    return slot_weights

# return index of randomly chosen (biased) slots
# https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_reward_choice(slot_iterations, iteration):
    weights = reward_slot_weights(slot_iterations, iteration)

    from utils.weighted_random import weighted_random
    return weighted_random(weights)
