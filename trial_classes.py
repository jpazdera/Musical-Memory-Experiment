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
        m.tempo = 112
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
        t.tempo = 112
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
        RT = time() - start # record reaction time in milliseconds
        RT = round(RT, 3) * 1000
        RT = int(RT)
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
            self.correct = True
        else:
            self.correct = False
            
    def log_data(self):
        global SUBJ_NUM
        global IS_MUSICIAN
        global DATA
        # solution = 1 if the target was present, 0 if not
        if self.solution == True:
            sol = 1
        else:
            sol = 0
        # correct = 1 if the participant's response was correct, 0 if not
        if  self.correct == True:
            cor = 1
        else:
            cor = 0
        td = [SUBJ_NUM, IS_MUSICIAN, self.length, sol, self.rt, cor, self.target, self.t_position]
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
    global SUBJ_NUM # the participant's id number
    global DATA
    global IS_MUSICIAN # 1 if participant is a musician, 0 if not
    #DATA = [['ID','is_musician','MelodyLength','Solution','ReactionTime','Accuracy','TargetPhrase','TargetPosition']]
    DATA = []
    SUBJ_NUM = raw_input('Enter the participant\'s ID number. ')
    mus = ''
    print 'Is the participant a musician? (Y/N) '
    while mus.upper() != 'Y' and mus.upper() != 'N':
        mus = raw_input()
    if mus.upper() == 'Y':
        IS_MUSICIAN = 1
    else:
        IS_MUSICIAN = 0
    print '\n'


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
    #global SUBJ_NUM
    #global IS_MUSICIAN
    #global MEANS
    #MEANS = [SUBJ_NUM, IS_MUSICIAN]
    input = ''
    print 'Do you wish to save the data collected in this run of the experiment? (Y/N) '
    while input.upper() != 'Y' and input.upper() != 'N':
        input = raw_input()
    if input.upper() == 'Y':
        print 'Saving trial data...'
        data_file = open('Data-Logs/trial_data.csv', 'a')
        writer = csv.writer(data_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(DATA)
        data_file.close()
        print 'Save complete!'
    else:
        print 'Data not saved.'
        
        
'''
def acc_by_solution(solution_cond):
    global DATA
    global MEANS
    count_total = 0
    count_correct = 0
    for trial in DATA[1:]:
        if trial[1] == solution_cond:
            count_total += 1.0
            if trial[3] == 1:
                count_correct += 1.0
    acc = count_correct/count_total
    acc = round(acc, 3) * 100
    MEANS.append(acc)
    
    
def means_by_length(length_cond):
    global DATA
    global MEANS
    count_total = 0
    count_correct = 0
    sum = 0
    for trial in DATA[1:]:
        if trial[0] == length_cond:
            count_total += 1
            if trial[3] == 1: #if correct response was given
                sum += trial[2] #add RT to the overall sum
                count_correct += 1.0
    mean_RT = sum/count_correct
    mean_RT = int(round(mean_RT, 0))
    acc = count_correct/count_total
    acc = round(acc, 3) * 100
    MEANS.append(mean_RT) 
    MEANS.append(acc)


def means_by_condition(length_cond, solution_cond):
    global DATA
    global MEANS
    count_total = 0
    count_correct = 0
    sum = 0
    for trial in DATA[1:]: #ignore the first entry in DATA, i.e. the column names
        if (trial[0] == length_cond) and (trial[1] == solution_cond):
            count_total += 1.0
            if trial[3] == 1: #if correct response was given
                sum += trial[2] #add RT to the overall sum
                count_correct += 1.0
    mean_RT = sum/count_correct
    mean_RT = int(round(mean_RT, 0))
    acc = count_correct/count_total
    acc = round(acc, 3) * 100
    MEANS.append(mean_RT) 
    MEANS.append(acc)


def RT_by_target(target): # used for determining whether certain target phrases are identified more quickly
    global DATA
    global MEANS
    count_correct = 0
    sum = 0
    for trial in DATA[1:]:
        if trial[4] == target:
            if trial[3] == 1:
                sum += trial[2]
                count_correct += 1.0
    mean_RT = sum/count_correct
    mean_RT = int(round(mean_RT, 0))
    MEANS.append(mean_RT) 

    
def RT_by_t_position(t_position): # used for determining whether a serial position effect occurs
    global DATA
    global MEANS
    count_correct = 0
    sum = 0
    for trial in DATA[1:]:
        if trial[5] == t_position:
            if trial[3] == 1:
                sum += trial[2]
                count_correct += 1.0
    mean_RT = sum/count_correct
    mean_RT = int(round(mean_RT, 0))
    MEANS.append(mean_RT)
'''

'''
        file_name = 'Data-Logs/subject-data-' + SUBJ_NUM + '.csv'
        data_file = open(file_name,'w')
        writer = csv.writer(data_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(DATA)
        data_file.close()
        print 'Trial data saved.'
        print 'Calculating means and accuracy...'
        #the following functions calculate and store the accuracy and mean RT of each trial type
        #data columns will be as follows:
        #[ID, is_musician, acc_P, acc_N, RT_3, acc_3, RT_4, acc_4, RT_5, acc_5, RT_3P, acc_3P, RT_3N, acc_3N, RT_4P, acc_4P, RT_4N, acc_4N, RT_5P, acc_5P, RT_5N, acc_5N, RT_T0,...,RT_T7, RT_TP1,..., RT_TP5]
        acc_by_solution(1)
        acc_by_solution(0)
        means_by_length(3)
        means_by_length(4)
        means_by_length(5)
        means_by_condition(3, 1)
        means_by_condition(3, 0)
        means_by_condition(4, 1)
        means_by_condition(4, 0)
        means_by_condition(5, 1)
        means_by_condition(5, 0)
        i = 0
        while i < 8:
            RT_by_target(i)
            i += 1
        i = 0
        while i < 6:
            RT_by_t_position(i):
            i += 1
        print 'Saving genderal data...'
        data_file = open('Data-Logs/mean_data.csv', 'a')
        writer = csv.writer(data_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(MEANS)
        data_file.close()
        print 'Save complete!'
    else: #input.upper() == 'N'
        print 'Data not saved.'
'''