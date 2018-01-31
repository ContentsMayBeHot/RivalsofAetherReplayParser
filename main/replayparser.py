# replayparser.py by Rei Armenia(lazerzes)
#
# This function set takes in a .roa replay file and extracts the information
# that the user may find useful.


import sys

def parser(filename):

    f = open(filename, "r")
    print ("file.name:", f.name)

    lines = f.readlines()
    players = []

    # Even lines contain player information, except for line 0 which contains
    # replay information, if an even line starts with the letter H then it is
    # a human player, and has an input replay that we can use.
    # This section of code detects if a line starts with H, if so then it takes
    # that line and the next line and puts it into a list of player objects
    for i, line in enumerate(lines):
        if (i % 2 == 0 and i != 0):
            if(line[0] == 'H'):
                players.append(Player(line, lines[i + 1]))

    for n, player in enumerate(players):
        print("Player", n, "information:")
        print("info", '\n', player.p_info)
        print("~~~~~~~~~~~")
        print("replay", '\n', player.p_replay)
        print("-----------------------------------------------------------")


# The Player class is a wrapper for our player file, it contains the raw
# information that we pull from the replay file as information that we can
# easily work with in python.
class Player:
    def __init__(self, p_info, p_replay):
        self.p_info = p_info
        self.p_replay = p_replay


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print ("You must include a file.")
    elif(len(sys.argv) > 2):
        print("At this time, we can only accept one file.")
    else:
        parser(sys.argv[1])
