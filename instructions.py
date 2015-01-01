def main_instructions():
    print 'Welcome to the experiment!\n'
    print 'In this study, you will hear a series of short melodies, consisting of three to five phrases. Each melody will be followed by a single target phrase.'
    print 'Your goal is to determine, as quickly as possible,\nwhether the target phrase was present in the preceding melody.\n'
    print 'If the target phrase was present, press the J key. Press F if it was not.\nDo not make your response until the target phrase finishes playing.'
    print 'Responses made before the phrase finishes will not be recorded.'
    print 'You will be notified (\"GO!\") when the target phrase ends,\nindicating that you may now make your response.\n'
    print 'REMEMBER: J = YES, F = NO\n'
    raw_input('Press enter to begin!')
    print '\n'


def end_message():
    print 'Congratulations on completing the study!'
    print 'Thank you for your participation.'
    print '\n'
    raw_input('Press enter to finish...')
    

def exit_message():
    raw_input('Hit enter to exit the program...')
    print 'The program will now exit.'