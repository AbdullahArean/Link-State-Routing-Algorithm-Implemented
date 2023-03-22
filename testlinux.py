import os

os.system('xterm -T "A" -e python3 LinkStateRouting.py configA.txt &')
os.system('xterm -T "B" -e python3 LinkStateRouting.py configB.txt &')
os.system('xterm -T "C" -e python3 LinkStateRouting.py configC.txt &')
os.system('xterm -T "D" -e python3 LinkStateRouting.py configD.txt &')
os.system('xterm -T "E" -e python3 LinkStateRouting.py configE.txt &')
os.system('xterm -T "F" -e python3 LinkStateRouting.py configF.txt')
