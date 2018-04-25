# replayparser.py by Rei Armenia
# With Contributions by Matthew Harrison
# You can find the repo for this
# here(https://github.com/ContentsMayBeHot/RivalsofAetherReplayParser)
# You can find the docs for this
# here(https://github.com/ContentsMayBeHot/RivalsofAetherReplayParser/wiki)

import sys
import os
from enum import Enum
import numpy as np
import pathlib


class Replay:
    def __init__(self, roa_apath):
        f_in = open(roa_apath, "r")
        self.f_name = f_in.name
        f_lines = f_in.readlines()
        f_in.close()
        self.meta = MetaData(f_lines[0])
        self.rules = RuleData(f_lines[1])
        self.players = []
        for i, line in enumerate(f_lines):
            if line[0] == 'H':
                self.players.append(Player(line, f_lines[i + 1]))

    def format_replay_str(self, to_file=False):
        out_str = self.meta.format_meta_str()
        out_str += self.rules.format_rule_str()

        for player in self.players:
            out_str += player.format_player_str(to_file)

        return out_str

    def create_numpy(self, numpydir_path=None):
        if numpydir_path is None:
            numpydir_path = os.path.join("output", os.path.basename(self.f_name[:-4]))
        pathlib.Path(numpydir_path).mkdir(parents=True, exist_ok=True)

        for i, player in enumerate(self.players):
            out_path = os.path.join(numpydir_path, str(i) + "_" + player.name)
            print("\t" + self.f_name + " =npy=> " + out_path + ".npy")
            arr = player.collapse_actions()
            np.save(out_path, np.array(arr, dtype=object))

    def get_duration(self, as_ms=False):
        last_frame = max([x.actions[-1].frame_index for x in self.players])
        duration = int(last_frame) / 60
        if as_ms:
            duration *= 1000
        return duration


class MetaData:
    def __init__(self, meta_line):
        self.is_starred = bool(int(meta_line[0]))
        self.version = meta_line[1:8]
        self.date_time = meta_line[8:21]

    def format_meta_str(self):
        return str(self.is_starred) + "\t" + self.version + \
            "\t" + self.date_time + "\n"


class RuleData:
    def __init__(self, rule_line):
        self.stage_type = StageType(int(rule_line[0]))
        self.stage_id = Stage(int(rule_line[1:3]))
        self.stock_count = rule_line[3:5]
        self.time = rule_line[5:7]
        self.team = bool(int(rule_line[7]))
        self.friendly_fire = bool(int(rule_line[8]))

    def format_rule_str(self):
        return str(self.stage_type) + "\t" + str(self.stage_id) + "\t" + str(self.stock_count) + \
            "\t" + str(self.time) + "\t" + str(self.team) + "\t" + str(self.friendly_fire) + "\n"


class Player:
    def __init__(self, ln_info, ln_actions):
        self.name = ln_info[1:33].rstrip()
        self.character = Character(int(ln_info[39:41]))

        self.actions = []
        i = 0
        while i < len(ln_actions):
            i += self.get_single_action(i, ln_actions)

    def format_player_str(self, to_file=False):
        out_str = self.name + "\t" + str(self.character) + "\n"

        for action in self.actions:
            out_str += action.format_action_str(to_file)

        return out_str

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

    def collapse_actions(self):
        out_list = []
        u_frame = None
        u_list = None

        for action in self.actions:
            if u_frame is None:
                u_frame = action.frame_index
                u_list = action.simple_matrix
            elif u_frame is not None and u_frame == action.frame_index:
                u_list = np.add(u_list, action.simple_matrix)
            else:
                out_list.append((u_frame, u_list.tolist()))
                u_frame = action.frame_index
                u_list = action.simple_matrix

        return out_list


class Action:
    def __init__(self, frame_str, input_id):
        self.frame_index = int(frame_str)
        self.input_id = input_id
        self.type = self.cast_action()
        self.matrix = self.initialize_matrix()
        self.simple_matrix = self.initialize_simple_matrix()

    def format_action_str(self, to_file=False):
        if not to_file:
            return str(self.frame_index) + "\t" + str(self.type) + "\n"
        else:
            return str(self.frame_index) + "\t" + \
                str(self.simple_matrix) + "\n"

    def initialize_matrix(self):
        if self.type is ActionType.INVALID:
            return np.zeros((40))

        temp_array = np.zeros((40))
        temp_array[self.type.value] = 1
        return temp_array

    def initialize_simple_matrix(self):
        simp = self.map_simple()

        if simp is SimpleAction.INVALID:
            return np.zeros((26))

        temp_array = np.zeros((26))
        temp_array[simp.value] = 1
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

    def map_simple(self):
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
        }.get(self.type, SimpleAction.INVALID)

    def get_ms_from_start(self):
        return (self.frame_index / 60.00) * 1000

    def get_ms_delta(self, action):
        return ((self.frame_index / 60.00) * 1000) - \
            ((action.frame_index / 60.00) * 1000)


def print_help():
    print(
        "\n\n---------------\nreplayparser.py can be used to parse Rivals of Aether Replay Files")
    print("Commands:")
    print("\t -f : parse following files")
    print("\t -d : parse all files in following directories")
    print("\t -o : output all parsed replays as .txt files")
    print("\t -p : output all parsed replays to console")
    print("\t -npy : output all parsed replays as pickled numpy arrays")
    print("\t -help : prints the help info(this)\n---------------\n\n")


if __name__ == "__main__":

    passed_commands = []
    possible_commands = ["-d", "-f", "-o", "-npy", "-p", '-help']
    replays = []
    out_dir = False
    to_np = False
    to_console = False

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
            print("Parsing Files:")
            for roa_apath in cmd[1:]:
                print("\tParsing " + roa_apath + "...")
                replays.append(Replay(roa_apath))

        elif cmd[0] == '-d' and len(cmd) > 1:
            for dir_apath in cmd[1:]:
                print("Parsing Files from " + dir_apath + ":")
                for roa_apath in os.listdir(dir_apath):
                    if(roa_apath.endswith('.roa')):
                        print("\tParsing " + roa_apath + "...")
                        replays.append(Replay(dir_apath + roa_apath))

        elif cmd[0] == '-d' and len(cmd) == 1:
            print("DIR not spec")
            # TODO :: Grab all .roa files from cwd

        elif cmd[0] == '-o':
            out_dir = True

        elif cmd[0] == '-npy':
            to_np = True

        elif cmd[0] == '-p':
            to_console = True

        elif cmd[0] == '-help':
            print_help()
        else:
            print(cmd[0], "is not a supported command")

    if out_dir:
        print("Creating Simplified Replays")
        for replay in replays:
            dir_path = "output/"
            pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
            file_name = os.path.basename(replay.f_name[:-4])
            out_path = dir_path + file_name + "_parsed.txt"
            print("\t" + replay.f_name + " =txt=> " + out_path)
            f_out = open(out_path, "w+")
            f_out.write(replay.format_replay_str(False))

    if to_np:
        print("Creating Numpy Files")
        for replay in replays:
            replay.create_numpy()

    if to_console:
        for replay in replays:
            print(replay.f_name)
            print(replay.format_replay_str())

    if (len(passed_commands) <= 0):
        print_help()

    if(len(replays) > 0):
        print("Program finished!\nProcessed " +
              str(len(replays)) + " replays!")
