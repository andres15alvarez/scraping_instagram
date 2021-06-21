from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from tqdm import tqdm

def find_1st_tag(string, tag):
	return string.find(tag, string.find(tag)) + 1

def find_2nd_tag(string, tag):
	return string.find(tag, string.find(tag) + 1)

def main(username, password):
	browser = webdriver.Firefox()
	browser.implicitly_wait(5)
	actions = ActionChains(browser)
	browser.get('https://www.instagram.com/')
	sleep(5)

	username_input = browser.find_element_by_xpath("//input[@name='username']").send_keys(username)
	password_input = browser.find_element_by_xpath("//input[@name='password']").send_keys(password)

	login_button = browser.find_element_by_css_selector(".L3NKy > div:nth-child(1)").click()
	sleep(5)

	browser.get(f'https://www.instagram.com/{username}/')
	sleep(20)

	followers_xpath = "/html[@class='js logged-in client-root js-focus-visible sDN5V']/body/div[@id='react-root']/div/div/section[@class='_9eogI E3X2T']/main[@class='SCxLW  o64aR ']/div[@class='v9tJq AAaSh VfzDr']/header[@class='vtbgv ']/section[@class='zwlfE']/ul[@class='k9GMp ']/li[@class='Y8-fY '][2]/a[@class='-nal3 ']"
	followers_button = browser.find_element_by_xpath(followers_xpath).click()
	sleep(10)

	popup = browser.find_element_by_class_name('_1XyCr ')
	popup.click()
	for i in tqdm(range(50), desc='Loading your followers'):
		actions.send_keys(Keys.DOWN).perform()
	sleep(10)

	content = browser.page_source
	soup = BeautifulSoup(content, 'html.parser')
	users = []
	tag_users = soup.findAll("a",{'class' : 'FPmhX notranslate _0imsa'})
	for user in tqdm(tag_users, desc='Collecting your followers'):
		user_cleaned = str(user)[find_1st_tag(str(user), '>'):find_2nd_tag(str(user),'<')]
		users.append('@' + user_cleaned)

	print(f"You have: {len(users)} users")
	with open('users_ema.txt', 'w') as f:
		for user in tqdm(users, desc='Saving your followers'):
			f.write(user + '\n')

	browser.close()

if __name__ == '__main__':
	username = input('Enter your username: ')
	password = input('Enter your password: ')
	main(username, password)