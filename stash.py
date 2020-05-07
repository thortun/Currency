import time
import json
from driver import get_driver

def stash_url(league, tabs, tab_index, account_name):
	"""Returns the url to the tab."""
	base_url = "https://www.pathofexile.com/character-window/get-stash-items?"
	return base_url + "league={0}&tabs={1}&tabIndex={2},{2}&accountName={3}".format(
								league, tabs, tab_index, account_name)

def input_credentials(driver, usr, pwd):
	login_usr_input = driver.find_element_by_xpath("//input[@id='login_email']")
	login_pwd_input = driver.find_element_by_xpath("//input[@name='login_password']")
	login_usr_input.send_keys(usr)
	login_pwd_input.send_keys(pwd)

def main():
	USR = "thor_tunge@hotmail.com"
	PWD = "b97ZGP85Bnx$"
	BASE_STASH_URL = "https://www.pathofexile.com/character-window/get-stash-items?league=Delirium&tabs=1&tabIndex=0,0&accountName=Meldrin"

	driver = get_driver()

	driver.get("https://www.pathofexile.com/login")
	print("Waiting for browser check...")
	time.sleep(10)	# Wait for browser check
	input_credentials(driver, USR, PWD)
	input("Please finish login...")

	driver.get(BASE_STASH_URL)
	time.sleep(2)
	contents = driver.find_element_by_xpath("//pre").get_attribute("innerHTML")
	data = json.loads(contents)
	num_tabs = int(data["numTabs"])

	stash = {"tabs" : []}

	for i in range(num_tabs):
		url = stash_url("Delirium", i, i, "Meldrin")
		driver.get(url)
		this_data = driver.find_element_by_xpath("//pre").get_attribute("innerHTML")
		stash["tabs"].append(json.loads(this_data))
	with open("data/stash.json", "w") as fileID:
		fileID.write(json.dumps(stash))
	driver.quit()


if __name__ == '__main__':
	main()