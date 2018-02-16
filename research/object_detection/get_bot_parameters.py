import pyautogui

input("Move your mouse to the center of your character's cell. Then, press 'Enter' to continue...")
print("center_mouse = ", pyautogui.position())

input("Move your cursor to the damaged pixel (gray) at 75% of your hp bar. Then, press 'Enter' to continue...")
p = pyautogui.position()
q = pyautogui.pixel(*p)
print("hp_position = ", p)
print("missing_hp_color = ",q)

input("Save these values in mrrobot.py. Then, press 'Enter' to finish up.")