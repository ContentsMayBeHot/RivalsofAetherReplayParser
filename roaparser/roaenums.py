"""ROAEnums Declaration
"""
from enum import Enum
import numpy as np

class ActionType(Enum):
    INVALID = -1

    LEFT_PRESS = 0
    LEFT_RELEASE = 1
    LEFT_TAP = 2

    RIGHT_PRESS = 3
    RIGHT_RELEASE = 4
    RIGHT_TAP = 5

    UP_PRESS = 6
    UP_RELEASE = 7
    UP_TAP = 8

    DOWN_PRESS = 9
    DOWN_RELEASE = 10
    DOWN_TAP = 11

    ATTACK_PRESS = 12
    ATTACK_RELEASE = 13

    SPECIAL_PRESS = 14
    SPECIAL_RELEASE = 15

    JUMP_PRESS = 16
    JUMP_RELEASE = 17

    DODGE_PRESS = 18
    DODGE_RELEASE = 19

    STRONG_PRESS = 20
    STRONG_RELEASE = 21

    STRONG_LEFT_PRESS = 22
    STRONG_LEFT_RELEASE = 23

    STRONG_RIGHT_PRESS = 24
    STRONG_RIGHT_RELEASE = 25

    STRONG_UP_PRESS = 26
    STRONG_UP_RELEASE = 27

    STRONG_DOWN_PRESS = 28
    STRONG_DOWN_RELEASE = 29

    ANG_RIGHT = 30
    ANG_UP_RIGHT = 31
    ANG_UP = 32
    ANG_UP_LEFT = 33
    ANG_LEFT = 34
    ANG_DOWN_LEFT = 35
    ANG_DOWN = 36
    ANG_DOWN_RIGHT = 37

    ANG_TOGGLE_PRESS = 38
    ANG_TOGGLE_RELEASE = 39

    @staticmethod
    def map_actions(action_rune):
        return{
            'L': ActionType.LEFT_PRESS,
            'l': ActionType.LEFT_RELEASE,
            'E': ActionType.LEFT_TAP,
            'R': ActionType.RIGHT_PRESS,
            'r': ActionType.RIGHT_RELEASE,
            'I': ActionType.RIGHT_TAP,
            'U': ActionType.UP_PRESS,
            'u': ActionType.UP_RELEASE,
            'M': ActionType.UP_TAP,
            'D': ActionType.DOWN_PRESS,
            'd': ActionType.DOWN_RELEASE,
            'O': ActionType.DOWN_TAP,
            'A': ActionType.ATTACK_PRESS,
            'a': ActionType.ATTACK_RELEASE,
            'B': ActionType.SPECIAL_PRESS,
            'b': ActionType.SPECIAL_RELEASE,
            'J': ActionType.JUMP_PRESS,
            'j': ActionType.JUMP_RELEASE,
            'S': ActionType.DODGE_PRESS,
            's': ActionType.DODGE_RELEASE,
            'C': ActionType.STRONG_PRESS,
            'c': ActionType.STRONG_RELEASE,
            'F': ActionType.STRONG_LEFT_PRESS,
            'f': ActionType.STRONG_LEFT_RELEASE,
            'G': ActionType.STRONG_RIGHT_PRESS,
            'g': ActionType.STRONG_RIGHT_RELEASE,
            'X': ActionType.STRONG_UP_PRESS,
            'x': ActionType.STRONG_UP_RELEASE,
            'W': ActionType.STRONG_DOWN_PRESS,
            'w': ActionType.STRONG_DOWN_RELEASE,
            0: ActionType.ANG_RIGHT,
            45: ActionType.ANG_UP_RIGHT,
            90: ActionType.ANG_UP,
            135: ActionType.ANG_UP_LEFT,
            180: ActionType.ANG_LEFT,
            225: ActionType.ANG_DOWN_LEFT,
            270: ActionType.ANG_DOWN,
            315: ActionType.ANG_DOWN_RIGHT,
            'Z': ActionType.ANG_TOGGLE_PRESS,
            'z': ActionType.ANG_TOGGLE_RELEASE
        }.get(action_rune, ActionType.INVALID)

    @staticmethod
    def initialize_matrix(action):
        if action is ActionType.INVALID:
            return np.zeros((40))

        temp_array = np.zeros((40))
        temp_array[action.value] = 1
        return temp_array


class SimpleAction(Enum):
    INVALID = -1

    LEFT = 0
    LEFT_TAP = 1

    RIGHT = 2
    RIGHT_TAP = 3

    UP = 4
    UP_TAP = 5

    DOWN = 6
    DOWN_TAP = 7

    ATTACK = 8
    SPECIAL = 9
    JUMP = 10
    DODGE = 11
    STRONG = 12

    STRONG_LEFT = 13
    STRONG_RIGHT = 14
    STRONG_UP = 15
    STRONG_DOWN = 16

    ANG_RIGHT = 17
    ANG_UP_RIGHT = 18
    ANG_UP = 19
    ANG_UP_LEFT = 20
    ANG_LEFT = 21
    ANG_DOWN_LEFT = 22
    ANG_DOWN = 23
    ANG_DOWN_RIGHT = 24

    ANG_TOGGLE = 25

    @staticmethod
    def map_simple(action):
        return{
            ActionType.LEFT_PRESS: SimpleAction.LEFT,
            ActionType.LEFT_RELEASE: SimpleAction.LEFT,
            ActionType.LEFT_TAP: SimpleAction.LEFT_TAP,
            ActionType.RIGHT_PRESS: SimpleAction.RIGHT,
            ActionType.RIGHT_RELEASE: SimpleAction.RIGHT,
            ActionType.RIGHT_TAP: SimpleAction.RIGHT_TAP,
            ActionType.UP_PRESS: SimpleAction.UP,
            ActionType.UP_RELEASE: SimpleAction.UP,
            ActionType.UP_TAP: SimpleAction.UP_TAP,
            ActionType.DOWN_PRESS: SimpleAction.DOWN,
            ActionType.DOWN_RELEASE: SimpleAction.DOWN,
            ActionType.DOWN_TAP: SimpleAction.DOWN_TAP,
            ActionType.ATTACK_PRESS: SimpleAction.ATTACK,
            ActionType.ATTACK_RELEASE: SimpleAction.ATTACK,
            ActionType.SPECIAL_PRESS: SimpleAction.SPECIAL,
            ActionType.SPECIAL_RELEASE: SimpleAction.SPECIAL,
            ActionType.JUMP_PRESS: SimpleAction.JUMP,
            ActionType.JUMP_RELEASE: SimpleAction.JUMP,
            ActionType.DODGE_PRESS: SimpleAction.DODGE,
            ActionType.DODGE_RELEASE: SimpleAction.DODGE,
            ActionType.STRONG_PRESS: SimpleAction.STRONG,
            ActionType.STRONG_RELEASE: SimpleAction.STRONG,
            ActionType.STRONG_LEFT_PRESS: SimpleAction.STRONG_LEFT,
            ActionType.STRONG_LEFT_RELEASE: SimpleAction.STRONG_LEFT,
            ActionType.STRONG_RIGHT_PRESS: SimpleAction.STRONG_RIGHT,
            ActionType.STRONG_RIGHT_RELEASE: SimpleAction.STRONG_RIGHT,
            ActionType.STRONG_UP_PRESS: SimpleAction.STRONG_UP,
            ActionType.STRONG_UP_RELEASE: SimpleAction.STRONG_UP,
            ActionType.STRONG_DOWN_PRESS: SimpleAction.STRONG_DOWN,
            ActionType.STRONG_DOWN_RELEASE: SimpleAction.STRONG_DOWN,
            ActionType.ANG_RIGHT: SimpleAction.ANG_RIGHT,
            ActionType.ANG_UP_RIGHT: SimpleAction.ANG_UP_RIGHT,
            ActionType.ANG_UP: SimpleAction.ANG_UP,
            ActionType.ANG_UP_LEFT: SimpleAction.ANG_UP_LEFT,
            ActionType.ANG_LEFT: SimpleAction.ANG_LEFT,
            ActionType.ANG_DOWN_LEFT: SimpleAction.ANG_DOWN_LEFT,
            ActionType.ANG_DOWN: SimpleAction.ANG_DOWN,
            ActionType.ANG_DOWN_RIGHT: SimpleAction.ANG_DOWN_RIGHT,
            ActionType.ANG_TOGGLE_PRESS: SimpleAction.ANG_TOGGLE,
            ActionType.ANG_TOGGLE_RELEASE: SimpleAction.ANG_TOGGLE
        }.get(action, SimpleAction.INVALID)

    @staticmethod
    def initialize_simple_matrix(simple_action):
        if simple_action is SimpleAction.INVALID:
            return np.zeros((26))

        temp_array = np.zeros((26))
        temp_array[simple_action.value] = 1
        return temp_array


class StageType(Enum):
    INVALID = -1
    BASIC = 0
    AETHER = 1


class Stage(Enum):
    INVALID = -1
    NOTHING = 0
    TREETOP_LODGE = 1
    FIRE_CAPITOL = 2
    AIR_ARMADA = 3
    ROCK_WALL = 4
    MERCHANT_PORT = 5
    CRASH_GAME = 6
    BLAZING_HIDEOUT = 7
    TOWER_HEAVEN = 8
    TEMPEST_PEAK = 9
    FROZEN_FORTRESS = 10
    AETHERIAL_GATES = 11
    ENDLESS_ABYSS = 12
    UNAVAILABLE = 13
    CEO_RING = 14
    SPIRIT_TREE = 15
    STAGE_NAME = 16
    NEO_FIRE_CAPITAL = 17
    SWAMPY_ESTUARY = 18


class Character(Enum):
    NONE = 0
    INVALID = 1
    ZETTERBURN = 2
    ORCANE = 3
    WRASTOR = 4
    KRAGG = 5
    FORSBURN = 6
    MAYPUL = 7
    ABSA = 8
    ETALUS = 9
    ORI = 10
    RANNO = 11
    CLAIREN = 12
