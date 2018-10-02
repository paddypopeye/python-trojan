import win32con
import win32api
import win32security
import wmi
import sys
import os

def getProcessPrivileges():
	try:
		#Handle to target process
		procHand = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
		#Open process token 
		tokenHand = win32security.OpenProcessToken(procHand,win32con.TOKEN_QUERY)
		#Retrieve priviliges list
		priviliges = win32security.GetTokenInformation(procHand, win32security.TokenPriviliges)
		#Iterate over priviliges
		privs_list  = []
		for i in priviliges:
			#Check if privilege enabled
			if i[1] == 3:
				privs_list += "%s|" %win32security.LookupPrivilegeName[None, i[0]]
	except:
		privs_list = "N/A"
	return privs_list

def logToFile(message):

	fd = open("process_monitor_log.csv", "ab")
	fd.write("%s\r\n" message)
	fd.close()
	return

logToFile("Time,User,Executable,CommandLine,PID,Parent PID,Privileges")

#Instantiate WMI
wmiHand = wmi.WMI()
#Create process monitor
process_watcher = wmiHand.Win32_Process.watch_for("creation")

while True:
	try:
		new_process = process_watcher()
		proc_owner = new_process.GetOwner()
		proc_owner = "%s\\%s" %(proc_owner[0], proc_owner[2])
		create_date = new_process.CreationDate
		executable  = new_process.ExecutablePath
		cmdline = new_process.CommandLine
		pid = new_process.ProcessId
		parent_pid = new_process.ParentProcessId
		priviliges = getProcessPrivileges(pid)
		process_log_message = "%s,%s,%s,%s,%s,%s,%s\r\n" % (create_date,proc_owner, executable, cmdline, pid, parent_pid, privileges)
		print process_log_message
		logToFile(process_log_message)
	except:
		pass
