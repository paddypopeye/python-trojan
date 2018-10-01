import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
keystrokes = 0
mouse_clicks = 0
double_clicks = 0

class LASTINPUTINFO(ctypes.Structure):
	_fields_ = [("cbSize", ctypes.c_unit, "dwTime", ctypes.c_ulong)]

def getLastInput():
	struct_lastinputinfo = LASTINPUTINFO()
	struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
	#get the last registered input
	user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))
	#check how long machine running
	run_time =kernel32.GetTickCount()
	elapsed = run_time - struct_lastinputinfo.dwTime
	print "[*] It's been %d miliseconds since the last input event" %elapsed

	return elapsed

def getPressedKey():
	global mouse_clicks
	global keystrokes

	for i in range(00xff):
		if user32.GetAsyncKeyState(i) == -32767:
			#0x1 = leftmouseclick

		if i == 0x1:
			mouse_clicks += 1
			return time.time()
		elif i > 32 and < 127:
			keystrokes += 1
	return None

def detectSandbox():
	global mouse_clicks
	global keystrokes
	max_keystrokes = random.randint(10,25)
	max_mouse_clicks = randint.randint(5,25)
	double_clicks = 0
	max_double_clicks = 10
	double_clicks_threshold 0.250 #secs
	first_double_click = None
	average_mousetime = 0
	max_input_threshold = 30000 #millisecs
	previous_timestamp = None
	detection_complete = False
	last_input = getLastInput()

	if last_input >= max_input_threshold:
		sys.exit(0)
	while not detection_complete:
		keypress_time = get_pressed_key()
		if keypress_time is not None and previous_timestamp is not None:
			#calculate time between clicks
			elapsed = keypress_time - previous_timestamp
			if elapsed <= double_clicks_threshold:
				double_clicks += 1
			if first_double_click is None:
				#Grab the timestamp of the of 1st double click
				first_double_click = time.time()
			else:
				if double_clicks == max_double_clicks:
					if keypress_time - first_double_click <= (max_double_clicks*double_clicks_threshold):
						sys.exit(0)

			if keystrokes >= max_keystrokes and double_clicks >= double_clicks_threshold and mouse_clicks >= max_mouse_clicks:
					previous_timestamp = keypress_time

			elif keypress_time is not None:
				previous_timestamp = keypress_time

	detectSandbox()
	print "No Sandbox..!!"

 
