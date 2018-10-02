import sys
import struct
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.Isadump import  HashDump

memory_file = "WindowsXPSP2.vmem"
sys.path.append("<DRIVE TO VOLATITLITY>")
registry.PluginImporter()
config = conf.ConfObject()

config.parse_options()
config.PROFIE  = "WinXPSPx86"
config.LOCATION = "file://s" %memory_file
registry.register_global(config, commands.Command)
registry.register_global(config, addrspace.BaseAddressSpace)

registry = RegistryApi(config)
registry.populate_offsets()
sam_offset = None
sys_offset = None

for offset in registry.all_offsets:
	if registry.all_offsets[offset].endswith("\\SAM"):
		sam_offset = offset
		print "[*] SAM: 0x%08x" %offset
	if registry.all_offsets[offset].endswith("\\system"):
		sys_offset = offset
		print "[*] System: 0x%08x" %offset
	if sam_offset is not None and sys_offset is not None:
		config.sys_offset = sys_offset
		config.sam_offset = sam_offset
		hashdump = HashDump(config)
		for hash1 in hashdump.calculate():
			print hash1
			break
	if sam_offset is None or sys_offset is None:
		print "[!] Failed to find the system or SAM offsets"