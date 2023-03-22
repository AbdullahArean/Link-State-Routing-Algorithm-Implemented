import os

# List of config files to run
configs = ['configA.txt', 'configB.txt', 'configC.txt', 'configD.txt', 'configE.txt', 'configF.txt']

# Loop through each config file and open a new terminal window for each one
for config in configs:
    os.system(f"osascript -e 'tell app \"Terminal\" to do script \"python3 LinkStateRouting.py {config}\"'")
