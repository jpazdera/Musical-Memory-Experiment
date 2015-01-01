from melopy import Melopy
from random import sample, choice
from time import time, sleep
from msvcrt import getch
import procedures as proc
import phrase_list as pl
import winsound
import csv

class Trial:
    def __init__(self, l, s):
        self.length = l # denotes the number of phrases in the melody for that trial
        self.solution = s # True if the target phrase is in the memory set, False if not
        self.phrases = None # a list of the id numbers of the phrases to be used in the trial's melody
        self.target = None # the id number of the target phrase
        self.t_position = None # the position of the target in the melody (positive trials only)
        self.response = None # will be set to True or False, based on the participant's response
        self.correct = None # whether or not the participant responded correctly to the trial
        self.rt = None # the reaction time of the participant on the trial (in milliseconds)
    
    def __repr__(self):
        print "TRIAL RECORD"
        print "Melody: " + self.phrases
        print "Target: " + self.target
        print "Solution: " + self.solution
        print "Response given: " + self.response
        print "Accuracy: " + self.correct
        print "Reaction time: " + self.rt + " ms"

    def randomize_phrases(self): # chooses self.length phrases without replacement to create the melody; the target is either selected from the melody phrases (pos) or the unused phrases (neg)
        if self.solution == True:
            self.phrases = sample(xrange(8), self.length)
            target = sample(self.phrases, 1)
            self.target = target[0]
            self.t_position = self.phrases.index(target[0]) + 1 # records position of the target in the melody (i.e. first phrase = 1, etc.)
        else:
            ids = sample(xrange(8), (self.length + 1))
            self.phrases = ids[0:self.length]
            self.target = ids[self.length]
            self.t_position = ''
            
    def construct_melody(self):
        m = Melopy('current_melody')
        m.tempo = 96
        for id in self.phrases:
            m.add_quarter_rest()
            m.add_quarter_note('C4')
            m.add_eighth_note(pl.PHRASE_LIST[id][0])
            m.add_eighth_note(pl.PHRASE_LIST[id][1])
            m.add_quarter_note(pl.PHRASE_LIST[id][2])
        m.render()
    
    def construct_target(self):
        id = self.target
        t = Melopy('target_phrase')
        t.tempo = 96
        t.add_quarter_rest()
        t.add_quarter_note('C4')
        t.add_eighth_note(pl.PHRASE_LIST[id][0])
        t.add_eighth_note(pl.PHRASE_LIST[id][1])
        t.add_quarter_note(pl.PHRASE_LIST[id][2])
        t.render()

    def get_response(self):
        print "Go!\n"
        start = time()
        input = getch() # getch will only work when experiment is run in command line
        RT = (time() - start) * 1000 # record reaction time in milliseconds
        winsound.Beep(1000,500)
        return [input, RT]
        
    def record_response(self, resp):
        input = resp[0]
        RT = resp[1]
        self.rt = RT
        if input.upper() == 'J':
            self.response = True
        elif input.upper() == 'F':
            self.response = False
        else:
            self.response = None
            
    def check_response(self): # determines whether the given response was correct, and modifies self.correct appropriately
        if self.response == self.solution:
            self.correct = "C" # C == correct
        elif (self.response == True) and (self.solution == False):
            self.correct = "FP" # FP == false positive
        elif (self.response == False) and (self.solution == True):
            self.correct = "FN" # FN == false negative
        else:
            self.correct = None
            
    def log_data(self):
        global DATA
        td = [self.rt, self.correct, self.target, self.t_position]
        DATA.append(td)
        
    def run(self):
        self.randomize_phrases()
        self.construct_melody()
        self.construct_target()
        print 'The following melody will contain ' + str(self.length) + ' phrases...'
        sleep(2)
        proc.play_melody()
        print 'Prepare to hear the target phrase...'
        sleep(2)
        proc.play_target()
        resp = self.get_response()
        self.record_response(resp)
        self.check_response()
        self.log_data()
        sleep(1)


class Block:
    def __init__(self):
        self.trial_list = []
    
    def add_trial(self, trial):
        self.trial_list.append(trial)
    
    def randomize_block(self, melody_lengths):
        global COUNTER
        order = sample(melody_lengths, len(melody_lengths))
        for length in order:
            solution = decide_trial_solution(length)              
            t = Trial(length, solution)
            self.add_trial(t)
            # update trial counter according to the selected trial conditions
            if length == 3: 
                if solution == True:
                    COUNTER.three_pos += 1
                else:
                    COUNTER.three_neg += 1
            elif length == 4:
                if solution == True:
                    COUNTER.four_pos += 1
                else:
                    COUNTER.four_neg += 1
            else: # if length == 5:
                if solution == True:
                    COUNTER.five_pos += 1
                else:
                    COUNTER.five_neg += 1

    def run(self):
        for trial in self.trial_list:
            trial.run()


class TrialCounter:
    def __init__(self):
        self.remaining = 54
        self.three_pos = 0
        self.three_neg = 0
        self.four_pos = 0
        self.four_neg = 0
        self.five_pos = 0
        self.five_neg = 0
        

def initialize_trial_counter():
    global COUNTER
    COUNTER = TrialCounter()


def initialize_data_log():
    global DATA
    DATA = []


def decide_trial_solution(melody_length):
    global COUNTER
    if melody_length == 3:
        if COUNTER.three_pos == 9:
            solution = False
        elif COUNTER.three_neg == 9:
            solution = True
        else:
            solution = choice([True, False])
    elif melody_length == 4:
        if COUNTER.four_pos == 8:
            solution = False
        elif COUNTER.four_neg == 8:
            solution = True
        else:
            solution = choice([True, False])
    else: # if melody_length == 5:
        if COUNTER.five_pos == 10:
            solution = False
        elif COUNTER.five_neg == 10:
            solution = True
        else:
            solution = choice([True, False])
    return solution


def save_data():
    global DATA
    print 'Do you wish to save the data collected in this run of the experiment? (Y/N)\n'
    input = getch()
    if input.upper() == 'Y':
        print 'Saving data...'
        data_file = open('experiment-data.csv','a')
        writer = csv.writer(data_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(DATA)
        data_file.close()
        print 'Save complete!'
    else:
        print 'Data not saved.'