from selenium import webdriver
import platform

def get_driver(headless = False):
	"""Gets a selenium webdriver"""
	options = webdriver.ChromeOptions()
	if headless:
		options.add_argument('headless')

	my_system = platform.system()
	if my_system == "Windows":
		return webdriver.Chrome(chrome_options = options)
