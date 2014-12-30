import procedures as proc
import time
import trial_classes as tc

def test():
    t = tc.Trial(3, False)
    t.run()
    print t
    
test()