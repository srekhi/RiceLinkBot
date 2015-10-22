import argparse, os, time, urlparse, random, ctypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Tkinter import Tk
import tkMessageBox 

#class TimeoutException(Exception): pass
def getApplyButtons(page): #passing in the url of the jobs page, this takes all the urls for the apply buttons and adds them to applyBtns array
	applyBtns = []
	root="https://rice-csm.symplicity.com/students/index.php"
	for link in page.find_all('a'):
		url = link.get('href')
		classRef = link.get('class')
		if classRef: 
			if 'act' in classRef:
				url = root + url
				applyBtns.append(url)
	return applyBtns
def alert(title, message):
	box = Tk()
	box.title(title)
	Message(box, text = message, bg='red', fg = 'ivory').pack(padx=1, pady=1)
	Button(box, text = "Close", command=box.destroy).pack(side=BOTTOM)
	box.geometry('300x150')
	box.after(0, hello)
def getID(url):
	parsedURL = urlparse.urlparse(url)
	return urlparse.parse_qs(parsedURL.query)['id'][0] #gets the ID of the job we're applying to
def ViewBot(browser):
	visited = {} #dictionary stores the ids of jobs that have been visited. dict hashes are quicker to search thru.
	jobList = [] 
	count = 0
	while True: 
		time.sleep(random.uniform(1,1.5)) #randomize time so we don't look like robots
		page = BeautifulSoup(browser.page_source) #variable page contains source code of the page being looked @
		applyButtons  = getApplyButtons(page) #returns list of all applybuttons on the page
		if applyButtons: #if there are applyBtns found
			for applyButton in applyButtons:
				ID = getID(applyButton) #gets the URL for each apply button's url
				if ID not in visited:
					jobList.append(applyButton) #add to array jobs that have been applied to
					visited[ID]=1
					browser.get(applyButton)
					time.sleep(random.uniform(1,1.2))
					try:
						finalApplyBtn = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.NAME, 'dnf_opt_submit')))
						finalApplyBtn.click() 
										
					except TimeoutException: 
  						browser.get("https://rice-csm.symplicity.com/students/index.php?s=jobs&ss=jobs&mode=list")
						
					finally:
						
						browser.get("https://rice-csm.symplicity.com/students/index.php?s=jobs&ss=jobs&mode=list")#returning browser to job page
					

		else: #give an alert to the user that no applybtns can be found, and they need to refine their search.
			ctypes.windll.user32.MessageBoxA(0, "Not seeing any Apply Buttons, try refining your search.", "Oops!")

	
def Main():
	
	browser = webdriver.Firefox()
	browser.get("https://netid.rice.edu/cas/login?service=https%3A%2F%2Frice-csm.symplicity.com%2Fsso%2Fstudents%2Flogin&")
	time.sleep(random.uniform(10,10.1)) #making this wait until user logs in by about 4 seconds...will modify later to act only when user presses login
	browser.find_element_by_link_text('Jobs').click()	
	browser.find_element_by_link_text('Saved Searches').click()
	browser.find_element_by_link_text('engr-software').click()
	os.system('clear') # clears screen
	
	ViewBot(browser)
	browser.close()
if __name__ == "__main__":
	Main()
