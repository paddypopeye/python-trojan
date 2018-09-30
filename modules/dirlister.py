import os

def run(**args):
	print "[*] In dirlist module."
	files = os.listdir(".")
	return str(files)