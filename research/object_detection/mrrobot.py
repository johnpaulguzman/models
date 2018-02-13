from tfeyes import TFEyes

import pyautogui

import time
import threading


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

@setInterval(10*60)
def autobuff1():
    pyautogui.press('f9')
thread_buff1 = autobuff1()

@setInterval(30*60)
def autobuff2():
    pyautogui.press('f8')
thread_buff2 = autobuff2()

sensory_threads = []
my_eyes = TFEyes(0.85)
# thread_eye = threading.Thread(name='threadEye', target=my_eyes.start_watching, daemon=True)
# sensory_threads += [thread_eye]
# for thread in sensory_threads: thread.start()

my_eyes.do_print = True

cycle_wait = 1
kill_wait = 8
tele_cycles = 3
cycle_timeout = 30
center_mouse = (716, 380)
tele_key = 'q'

def clickAction(location):
    print("Clicking at {}".format(location))
    pyautogui.click(location)
    time.sleep(kill_wait)
    pyautogui.click(center_mouse, clicks=2, interval=0.1)

def teleAction():
    print("Teleporting")
    pyautogui.press(tele_key)

def centerDistance(a):
    return abs(a[0] - center_mouse[0]) + abs(a[1] - center_mouse[1])

tele_iterator = 0
cycle_iterator = 0
while True:
    try:
        my_eyes.start_watching()
        data_points = my_eyes.data_points
        
        #if data_points:
        #    locations = [b for a, b in data_points]
        #    dist_map = list(map(centerDistance, locations))
        #    clickAction(locations[dist_map.index(max(dist_map))])
        for data in data_points:
            name_confidence, location = data
            name, confidence = name_confidence
            if name == 'myst_case' or name == 'mob':
                clickAction(location)
                break

        if data_points: tele_iterator = 0
        else: tele_iterator += 1
        cycle_iterator += 1
        if tele_iterator > tele_cycles or cycle_iterator > cycle_timeout: 
            tele_iterator = 0
            cycle_iterator = 0
            teleAction()

        time.sleep(cycle_wait)
    except Exception as e:
        print(e)
        import code; code.interact(local=dict(globals(), **locals()))

# for thread in sensory_threads: thread.join()

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