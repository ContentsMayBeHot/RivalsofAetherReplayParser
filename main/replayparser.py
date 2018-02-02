# replayparser.py by Rei Armenia(lazerzes)
#
# This function set takes in a .roa replay file and extracts the information
# that the user may find useful.


import sys
from enum import Enum

def parse_wrapper(file_name):
    return Replay(file_name)


class Replay:
    def __init__(self, file_name):
        f = open(file_name, "r")
        lines = f.readlines()
        self.file_name = f.name
        self.meta = self.get_meta(lines[0])
        self.rules = self.get_rules(lines[1])
        self.players = []
        self.get_players(lines[2:])

    def get_meta(self, meta_line):
        return meta_line

    def get_rules(self, rules_line):
        return rules_line

    def get_players(self, player_lines):
        for i, line in enumerate(player_lines):
            if (i % 2 == 0):
                if(line[0] == 'H'):
                    self.players.append(Player(line, player_lines[i + 1]))

    def print_replay(self):
        print("Replay Name:", self.file_name)
        print("----------------------------")
        for i, player in enumerate(self.players):
            print("Player " + str(i+1) + ": ", player.name)
            print("Character:", player.character)
            print("----------------------------")
            for action in player.actions:
                print ("On Frame #:", action.frame_num, "action " + action.input_id + " took place")


# The Player class is a wrapper for our player file, it contains the raw
# information that we pull from the replay file as information that we can
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
        #print("action_frame", actions[0].frame_num, "action id", actions[0].input_id)
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
            frame_str = self.actions[-1].frame_num

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
        self.frame_num = int(frame_str)
        self.input_id = input_id

    def get_ms_from_start(self):
        return (self.frame_num / 60.00) * 1000

    def get_ms_delta(self, action):
        return ((self.frame_num / 60.00) * 1000) - ((action.frame_num / 60.00) * 1000)



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

    if(len(sys.argv) < 2):
        print ("You must include a file.")
    elif(len(sys.argv) > 2):
        for i, arg in enumerate(sys.argv):
            if(i != 0):
                replays.append(parse_wrapper(arg))
    else:
        replays.append(parse_wrapper(sys.argv[1]))

    for replay in replays:
        replay.print_replay()
