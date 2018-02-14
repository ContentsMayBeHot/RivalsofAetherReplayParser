# replayparser.py by Rei Armenia
# With Contributions by Matthew Harrison

import sys
import os
from enum import Enum
import numpy as np


class Replay:
    def __init__(self, roa_apath):
        f_in = open(roa_apath, "r")
        self.f_name = f_in.name
        f_lines = f_in.readlines()
        f_in.close()
        print(self.f_name)
        self.meta = MetaData(f_lines[0])
        self.rules = RuleData(f_lines[1])
        self.players = []
        for i, line in enumerate(f_lines[2:]):
            if line[0] is 'H':
                self.players.append(Player(line, f_lines[i + 1]))


class MetaData:
    def __init__(self, meta_line):
        self.is_starred = bool(int(meta_line[0]))
        self.version = meta_line[1:8]
        self.date_time = meta_line[8:22]


class RuleData:
    def __init__(self, rule_line):
        self.stage_type = StageType(int(rule_line[0]))
        self.stage_id = Stage(int(rule_line[1:3]))
        self.stock_count = rule_line[3:5]
        self.time = rule_line[5:7]
        self.team = bool(int(rule_line[7]))
        self.friendly_fire = bool(int(rule_line[8]))


class Player:
    def __init__(self, ln_info, ln_actions):
        self.name = ln_info[1:33].rstrip()
        self.character = Character(int(ln_info[39:41]))

        self.actions = []
        i = 0
        while i < len(ln_actions):
            i += self.get_single_action(i, ln_actions)

    def get_single_action(self, lower_bound, ln_actions):
        position = 0
        frame_str = ""
        input_str = ""

        while True:
            if ln_actions[lower_bound + position].isdigit():
                frame_str = frame_str + ln_actions[lower_bound + position]
                position += 1
            else:
                break

        # If the input does not have a frame, give it the same frame number as
        # the previous action
        if frame_str == "":
            frame_str = self.actions[-1].frame_index

        while True:
            if ln_actions[lower_bound + position] != 'y':
                input_str = input_str + ln_actions[lower_bound + position]
                break
            else:
                input_str = input_str + \
                    ln_actions[lower_bound + position: lower_bound + position + 4]
                position += 3
                break

        # This line is here to remove any invaid actions
        # We do this because sometimes there are spaces at the end of a line
        if(len(input_str.rstrip()) > 0):
            self.actions.append(Action(frame_str, input_str))

        position += 1
        return position


class Action:
    def __init__(self, frame_str, input_id):
        self.frame_index = int(frame_str)
        self.input_id = input_id
        self.type = self.cast_action()
        self.matrix = self.initialize_matrix()

    def initialize_matrix(self):
        temp_array = np.zeros((1,40))
        temp_array[self.type.value] = 1
        return temp_array

    def cast_action(self):
        simp_action = 0
        if(self.input_id[0] in ['y', 'Y']):
            simp_action = 45 * round(float(self.input_id[1:]) / 45)
            if(simp_action == 360):
                simp_action = 0
        else:
            simp_action = self.input_id[0]

        return self.map_actions(simp_action)

    def map_actions(self, x):
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
        }.get(x, ActionType.INVALID)

    def get_ms_from_start(self):
        return (self.frame_index / 60.00) * 1000

    def get_ms_delta(self, action):
        return ((self.frame_index / 60.00) * 1000) - \
            ((action.frame_index / 60.00) * 1000)


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
    ALSO_NOTHING = 6
    BLAZING_HIDEOUT = 7
    TOWER_HEAVEN = 8
    TEMPEST_PEAK = 9
    SOMETHING = 10
    ANOTHER = 11


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


if __name__ == "__main__":

    passed_commands = []
    possible_commands = ["-d", "-f", "-o"]
    replays = []
    outdir_apath = False

    temp_command = []
    for arg in sys.argv:
        if arg in possible_commands:
            if len(temp_command) > 0:
                passed_commands.append(temp_command)
                temp_command = []
            temp_command.append(arg)
        elif len(temp_command) > 0:
            temp_command.append(arg)

    if len(temp_command) > 0:
        passed_commands.append(temp_command)

    for cmd in passed_commands:
        if cmd[0] == '-f' and len(cmd) > 1:
            for roa_apath in cmd[1:]:
                replays.append(Replay(roa_apath))

        elif cmd[0] == '-d' and len(cmd) > 1:
            for dir_apath in cmd[1:]:
                for roa_apath in os.listdir(dir_apath):
                    if(roa_apath.endswith('.roa')):
                        replays.append(Replay(dir_apath + roa_apath))

        elif cmd[0] == '-d' and len(cmd) == 1:
            print("DIR not spec")
            # TODO :: Grab all .roa files from cwd

        elif cmd[0] == '-o':
            outdir_apath = True

        else:
            print(cmd[0], "is not a supported command")

        if outdir_apath:
            print("Creating Simplified Replays in output/")

    for replay in replays:
        print(replay.f_name)
