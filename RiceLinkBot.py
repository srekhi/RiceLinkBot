import argparse, os, time, urlparse, random, ctypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getApplyButtons(page):
	applyBtns = []
	for link in page.find_all('a'):
		url = link.get('href')
		classRef = link.get('class')
		if classRef: 
			if 'act' in classRef:
				links.append(url)
	return applyBtns
def getID(url):
	parsedURL = urlparse.urlparse(url)
	return urlparse.parse_qs(parsedURL.query)['id'][0] #gets the ID of the job we're applying to
def ViewBot(browser):
	visited = {} #dictionary stores the ids of jobs that have been visited. dict hashes are quicker to search thru.
	jobList = [] 
	count = 0
	while True: 
		#sleep to make sure everything loads
		#add random to make us look human
		time.sleep(random.uniform(3.9, 7)) #randomize time so we don't look like robots
		page = BeautifulSoup(browser.page_source) 
		#grabs source of page that's being viewed.
		applyButtons  = getApplyButtons(page) #returns list of all applybuttons on the page
		if applyButtons: #if there are applyBtns found
			for applyButton in applyButtons:
				ID = getID(applyButton) 
				if ID not in visited:
					pList.append(applyButton)
					visited[ID]=1
		if jobList: #If there are jobs available
			job  = jobList.pop()
			browser.get(applyButton)
			count += 1
		else: #give an alert to the user that no applybtns can be found, and they need to refine their search.
			ctypes.windll.user32.MessageBoxA(0, "Not seeing any Apply Buttons, try refining your search.", "Oops!")


def Main():
	
	browser = webdriver.Firefox()
	browser.get("https://netid.rice.edu/cas/login?service=https%3A%2F%2Frice-csm.symplicity.com%2Fsso%2Fstudents%2Flogin&")
	browser.find_element_by_css_selector('.button.c_button.s_button').click()	
	time.sleep(random.uniform(5,7))
	jobsBtn = browser.find_element_by_id('yui-gen15')
	jobsBtn.click()
	os.system('clear') # clears screen
	
	ViewBot(browser)
	browser.close()
if __name__ == "__main__":
	Main()
