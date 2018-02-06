# replayparser.py by Rei Armenia(lazerzes)
#
# This function set takes in a .roa replay file and extracts the information
# that the user may find useful.


import sys
from enum import Enum
import time

def parse_wrapper(file_name):
    return Replay(file_name)


class Replay:
    def __init__(self, file_name):
        f = open(file_name, "r")
        lines = f.readlines()
        self.file_name = f.name
        self.meta = self.get_meta(lines[0])
        self.stage_type, self.stage_id = self.get_stage(lines[1])
        self.players = []
        self.get_players(lines[2:])

    def get_meta(self, meta_line):
        return meta_line

    def get_stage(self, line):
        return StageType(int(line[0])), Stage(int(line[1:3]))

    def get_players(self, player_lines):
        for i, line in enumerate(player_lines):
            if (i % 2 == 0):
                if(line[0] == 'H'):
                    self.players.append(Player(line, player_lines[i + 1]))

    def print_replay(self):
        print("Replay Name:", self.file_name)
        print("Stage: ", self.stage_id, self.stage_type)
        print("----------------------------")
        for i, player in enumerate(self.players):
            print("Player " + str(i+1) + ": ", player.name)
            print("Character:", player.character)
            print("----------------------------")
            for action in player.actions:
                print ("On Frame #:", action.frame_index, "action " + action.input_id + " took place", action.type)

    def to_file(self):
        file_name = self.file_name[:-4]
        file_name += "_parsed.txt"

        f = open(file_name, "w+")

        f.write(self.meta + "\n")
        f.write(str(self.stage_id) + "\t" + str(self.stage_type) + "\n")

        for i, player in enumerate(self.players):
            f.write(str(i + 1) + "\t" + player.name + "\t" + str(player.character) + "\n")
            f.write("\n")
            for action in player.actions:
                f.write(str(action.frame_index) + "\t" + action.input_id + "\t" + str(action.type) + "\n")

            f.write("\n")

        f.close()


# The Player class is a wrapper for our player file, it contains the raw
# nformation that we pull from the replay file as information that we can
# easily work with in python.
class Player:
    def __init__(self, p_info, p_replay):
        self.name = self.get_name(p_info)
        self.character = self.get_character(p_info)
        self.actions = []
        self.get_actions(p_replay)

    def get_name(self, info_line):
        name = info_line[1:33]
        name = name.rstrip()
        return name

    def get_character(self, info_line):
        character_id = info_line[39:41]
        enum = Character(int(character_id))
        return enum

    def get_actions(self, replay_line):
        i = 0
        #self.getSingleAction(0, replay_line, actions)
        #print("action_frame", actions[0].frame_index, "action id", actions[0].input_id)
        while i < len(replay_line):
            i += self.get_single_action(i, replay_line)

    def get_single_action(self, lower_bound, replay_line):
        position = 0
        frame_str = ""
        input_str = ""

        while True:
            if replay_line[lower_bound + position].isdigit():
                frame_str = frame_str + replay_line[lower_bound + position]
                position += 1
            else:
                break

        # If the input does not have a frame, give it the same frame number as
        # the previous action
        if frame_str == "":
            frame_str = self.actions[-1].frame_index

        while True:
            if replay_line[lower_bound + position] != 'y':
                input_str = input_str + replay_line[lower_bound + position]
                break
            else:
                input_str = input_str + replay_line[lower_bound + position : lower_bound + position + 4]
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
            'L' : ActionType.LEFT_PRESS,
            'l' : ActionType.LEFT_RELEASE,
            'E' : ActionType.LEFT_TAP,
            'R' : ActionType.RIGHT_PRESS,
            'r' : ActionType.RIGHT_RELEASE,
            'I' : ActionType.RIGHT_TAP,
            'U' : ActionType.UP_PRESS,
            'u' : ActionType.UP_RELEASE,
            'M' : ActionType.UP_TAP,
            'D' : ActionType.DOWN_PRESS,
            'd' : ActionType.DOWN_RELEASE,
            'O' : ActionType.DOWN_TAP,
            'A' : ActionType.ATTACK_PRESS,
            'a' : ActionType.ATTACK_RELEASE,
            'B' : ActionType.SPECIAL_PRESS,
            'b' : ActionType.SPECIAL_RELEASE,
            'J' : ActionType.JUMP_PRESS,
            'j' : ActionType.JUMP_RELEASE,
            'S' : ActionType.DODGE_PRESS,
            's' : ActionType.DODGE_RELEASE,
            'C' : ActionType.STRONG_PRESS,
            'c' : ActionType.STRONG_RELEASE,
            'F' : ActionType.STRONG_LEFT_PRESS,
            'f' : ActionType.STRONG_LEFT_RELEASE,
            'G' : ActionType.STRONG_RIGHT_PRESS,
            'g' : ActionType.STRONG_RIGHT_RELEASE,
            'X' : ActionType.STRONG_UP_PRESS,
            'x' : ActionType.STRONG_UP_RELEASE,
            'W' : ActionType.STRONG_DOWN_PRESS,
            'w' : ActionType.STRONG_DOWN_RELEASE,
            0 : ActionType.ANG_RIGHT,
            45 : ActionType.ANG_UP_RIGHT,
            90 : ActionType.ANG_UP,
            135 : ActionType.ANG_UP_LEFT,
            180 : ActionType.ANG_LEFT,
            225 : ActionType.ANG_DOWN_LEFT,
            270 : ActionType.ANG_DOWN,
            315 : ActionType.ANG_DOWN_RIGHT,
            'Z' : ActionType.ANG_TOGGLE_PRESS,
            'z' : ActionType.ANG_TOGGLE_RELEASE
        }.get(x, ActionType.INVALID)

    def get_ms_from_start(self):
        return (self.frame_index / 60.00) * 1000

    def get_ms_delta(self, action):
        return ((self.frame_index / 60.00) * 1000) - ((action.frame_index / 60.00) * 1000)

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
    replays = []
    parse_time = 0

    if(len(sys.argv) < 2):
        print ("You must include a file.")
    elif(len(sys.argv) > 2):
        for i, arg in enumerate(sys.argv):
            if(i != 0):
                before = time.time()
                replays.append(parse_wrapper(arg))
                after = time.time()
                parse_time += (after - before)
    else:
        before = time.time()
        replays.append(parse_wrapper(sys.argv[1]))
        after = time.time()
        parse_time += (after - before)

    for replay in replays:
        replay.print_replay()
        replay.to_file()

    print("Parsed", (len(sys.argv) - 1), "Replays in", (parse_time * 1000), "ms")
