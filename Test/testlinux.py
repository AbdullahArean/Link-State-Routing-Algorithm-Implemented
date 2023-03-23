# import os
#
# os.system('xterm -T "A" -e python3 LinkStateRouting.py configA.txt &')
# os.system('xterm -T "B" -e python3 LinkStateRouting.py configB.txt &')
# os.system('xterm -T "C" -e python3 LinkStateRouting.py configC.txt &')
# os.system('xterm -T "D" -e python3 LinkStateRouting.py configD.txt &')
# os.system('xterm -T "E" -e python3 LinkStateRouting.py configE.txt &')
# os.system('xterm -T "F" -e python3 LinkStateRouting.py configF.txt')
import os

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the path of the LinkStateRouting.py file (assuming it's in the parent directory's src folder)
lsr_path = os.path.join(current_dir, "..", "src", "LinkStateRouting.py")

# List of config files to run
configs = ['configA.txt', 'configB.txt', 'configC.txt', 'configD.txt', 'configE.txt', 'configF.txt']

# Loop through each config file and open a new terminal window for each one
for i, config in enumerate(configs):
    # Use xterm to open a new terminal window with a specific title and run the python command with the configuration
    os.system(f"xterm -T \"{chr(65+i)}\" -e python3 {lsr_path} {config} &")
