import procedures as proc
import instructions as instr
import trial_classes as tc

def main():
    try:
        tc.initialize_trial_counter()
        proc.initialize_trial_blocks()
        tc.initialize_data_log()
        instr.main_instructions()
        proc.run_practice_trials()
        tc.reset_counter_after_practice()
        instr.end_practice_message()
        proc.run_procedure()
        instr.end_message()
        tc.save_data()
        instr.exit_message()
    except Exception as ex:
        print ex
        raw_input()

main()