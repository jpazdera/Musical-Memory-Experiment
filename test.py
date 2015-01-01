import trial_classes as tc

def test():
    tc.initialize_data_log()
    t = tc.Trial(3, False)
    t.run()
    try:
        tc.save_data()
    except Exception as ex:
        print ex
        raw_input()
    
test()