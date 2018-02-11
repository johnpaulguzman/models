from tfeyes import TFEyes

import threading

sensory_threads = []

my_eyes = TFEyes()
thread_eye = threading.Thread(name='threadEye', target=my_eyes.start_watching, daemon=True)
sensory_threads += [thread_eye]

for thread in sensory_threads: thread.start()

my_eyes.do_print = True

for thread in sensory_threads: thread.join()

"""
import threading
from time import time

def wattim():
	while True:
		t = time()
		if t%10==0: print("its been 10 sec")
		if t%2==0: print("its been 2 sec")

thread_eye = threading.Thread(name='timer', target=wattim)
thread_eye.start()
"""