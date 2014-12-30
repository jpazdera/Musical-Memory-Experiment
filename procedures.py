import winsound
import trial_classes as tc
from random import sample

def initialize_trial_blocks():
    global TRIAL_BLOCKS
    TRIAL_BLOCKS = []
    i = 0
    while i < 4: # four blocks have three of each melody length condition
        b = tc.Block()
        b.randomize_block([3,3,3,4,4,4,5,5,5])
        TRIAL_BLOCKS.append(b)
        i += 1
    while (i == 4) or (i == 5): # two blocks have 3 threes, 2 fours, and 4 fives
        b = tc.Block()
        b.randomize_block([3,3,3,4,4,5,5,5,5])
        TRIAL_BLOCKS.append(b)
        i += 1
    TRIAL_BLOCKS = sample(TRIAL_BLOCKS, len(TRIAL_BLOCKS))
    return


def run_procedure():
    global TRIAL_BLOCKS
    for block in TRIAL_BLOCKS:
        block.run()
    return
    
def play_melody():
    winsound.PlaySound('current_melody', winsound.SND_FILENAME)
    return


def play_target():
    winsound.PlaySound('target_phrase', winsound.SND_FILENAME)
    return