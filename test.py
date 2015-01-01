import trial_classes as tc

def test():
    try:
        tc.initialize_data_log()
        t = tc.Trial(3, False)
        t.run()
        t = tc.Trial(3, True)
        t.run()
        t = tc.Trial(4, True)
        t.run()
        t = tc.Trial(4, False)
        t.run()
        t = tc.Trial(5, False)
        t.run()
        t = tc.Trial(5, True)
        t.run()
        tc.save_data()
    except Exception as ex:
        print ex
        raw_input()
    
test()