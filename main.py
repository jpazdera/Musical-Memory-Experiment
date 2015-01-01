import procedures as proc
import instructions as instr
import trial_classes as tc

def main():
    tc.initialize_trial_counter()
    tc.initialize_data_log()
    proc.initialize_trial_blocks()
    instr.main_instructions()
    # run_practice_trials()
    proc.run_procedure()
    instr.end_message()
    tc.save_data()
    instr.exit_message()
   
main()