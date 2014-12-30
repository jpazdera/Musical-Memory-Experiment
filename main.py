import procedures as proc
import instructions as instr
import trial_classes as tc

def main():
    tc.initialize_trial_counter()
    tc.initialize_data_log()
    proc.initialize_trial_blocks()
    instr.display_main_instructions()
    # run_practice_trials()
    proc.run_procedure()
    # save_data()
    instr.display_end_message()
   
main()