import subprocess
import time
import os
import re
import glob

file_path = '/scratch/jczhang/MITgcm_baroclinic_instability_old/MITgcm/verification/tutorial_reentrant_channel/input'
data_file = file_path + '/data'
run_path = '/scratch/jczhang/MITgcm_baroclinic_instability_old/MITgcm/verification/tutorial_reentrant_channel/run'

def find_latest_pickup_iter(run_path):
    # Match all pickup.*.data files
    pattern = os.path.join(run_path, 'pickup.*.data')
    pickup_files = glob.glob(pattern)

    iter_strings = []
    for file in pickup_files:
        # Extract the iteration string (with leading zeros)
        match = re.search(r'pickup\.(\d+)\.data', os.path.basename(file))
        if match:
            iter_strings.append(match.group(1))  # Keep it as string with leading zeros

    if not iter_strings:
        return None

    # Return the string with the highest numeric value, preserving format
    return max(iter_strings, key=lambda x: int(x))
    
def modify_mitgcm_data_file(data_path, new_values):
    # Open the file and read all lines into a list
    with open(data_path, 'r') as f:
        lines = f.readlines()
    updated = False # Flag to track if we successfully updated the line
    for i, line in enumerate(lines):
            if line.strip().startswith('nIter0'):
                # Replace the line with the new value for nIter0
                lines[i] = f' nIter0 = {new_values},\n'
                updated = True
                break

    if not updated:
        print("⚠️ 'nIter0' not found in data file.")
    # Write the modified lines back to the file
    with open(data_path, 'w') as f:
        f.writelines(lines)
    print(f"✅ Updated nIter0 = {new_values} in {data_path}")

def run_debugjob():
    print("Starting the debugjob and simulation... ")
    # Run the expect script that handles the interactive debugjob session
    subprocess.run(['expect', '/scratch/jczhang/MITgcm_baroclinic_instability_old/MITgcm/verification/tutorial_reentrant_channel/auto_command.exp'], check=True)
    print("Debugjob session ended.")

def main_loop():
        for cycle in range(max_cycles):
            print(f"\n Cycle {cycle+1}/{max_cycles} ~ smily emoji")

            run_debugjob()
            
            latest_iter = find_latest_pickup_iter(run_path)
            print(latest_iter)
            if latest_iter is None:
                print("No pickup files found, stopping.")
                break

            # Update nIter0 in data file
            modify_mitgcm_data_file(data_file, latest_iter)
    
            print("Ready for running next iter~.")
            # Optionally sleep or wait here before restarting debugjob
            time.sleep(10)

if __name__ == '__main__':
    max_cycles = 89
    main_loop()