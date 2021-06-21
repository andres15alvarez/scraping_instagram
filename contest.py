import random, pyperclip
from time import sleep
from selenium import webdriver
from tqdm import tqdm

def get_comments(file):
	with open(file, 'r') as f:
		users = f.readlines()

	users = list(set(map(lambda x: x[:-1], users)))
	L = len(users)
	comments = [users[i] + ' ' + users[i+1] + ' ' + users[i+2] for i in range(0,L-2,3)]

	return comments

def main(username, password, post):
	comments = get_comments('comments.txt')
	browser = webdriver.Firefox()
	browser.implicitly_wait(5)
	browser.get('https://www.instagram.com/')

	sleep(5)

	username_input = browser.find_element_by_xpath("//input[@name='username']").send_keys(username)
	password_input = browser.find_element_by_xpath("//input[@name='password']").send_keys(password)

	login_button = browser.find_element_by_css_selector(".L3NKy > div:nth-child(1)").click()
	sleep(5)

	browser.get(post)
	sleep(5)

	for comment in tqdm(comments, desc='Commenting'):
		pyperclip.copy(comment)
		comment_area = browser.find_element_by_class_name('Ypffh').click()
		comment_area = browser.find_element_by_class_name('Ypffh').send_keys(pyperclip.paste())
		sleep(5)
		browser.find_element_by_xpath('/html/body/div[1]/div/div/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]').click()
		sleep(random.randint(10,20))

	browser.close()

if __name__ == '__main__':
	username = input('Enter your username: ')
	password = input('Enter your password: ')
	post = input('Enter the URL of the post: ')
	main(username, password, post)