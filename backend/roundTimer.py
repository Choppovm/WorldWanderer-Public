import time
import sys

timeLeft = int(sys.argv[1]) # Time limit will be received from main.py

while timeLeft > 0:
    time.sleep(1)
    timeLeft -= 1

# When file terminates, main.py will recognize file isn't running anymore