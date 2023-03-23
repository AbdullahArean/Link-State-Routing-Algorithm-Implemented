# import os
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configA.txt"')
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configB.txt"')
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configC.txt"')
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configD.txt"')
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configE.txt"')
# os.system('start cmd.exe @cmd /k "python LinkStateRouting.py configF.txt"')
import os

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the path of the LinkStateRouting.py file (assuming it's in the parent directory's src folder)
lsr_path = os.path.join(current_dir, "..", "src", "LinkStateRouting.py")

# List of config files to run
configs = ['configA.txt', 'configB.txt', 'configC.txt', 'configD.txt', 'configE.txt', 'configF.txt']

# Loop through each config file and open a new Command Prompt (cmd) window for each one
for config in configs:
    # Change the working directory of the Command Prompt to the current directory of the Python file
    # Use the /d switch to also change the drive if necessary
    os.system(f"start cmd.exe /d {current_dir} /k python {lsr_path} {config}")
