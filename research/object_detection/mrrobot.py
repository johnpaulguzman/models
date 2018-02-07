from tfeyes import TFEyes

import threading

sensory_threads = []

my_eyes = TFEyes()
thread_eye = threading.Thread(name='threadEye', target=my_eyes.start_watching, daemon=True)
sensory_threads += [thread_eye]

for thread in sensory_threads: thread.start()

my_eyes.do_print = True

for thread in sensory_threads: thread.join()