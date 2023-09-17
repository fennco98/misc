from twill.commands import *
from bs4 import BeautifulSoup
import requests

username_trash = "connorfenn@gmail.com"
password_trash = "SpaceHaus1!"

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

## Trash
driver.get('https://www.wm.com/us/en/user/login')

driver.implicitly_wait(10)

# Note that fields ARE case sensitive
username = driver.find_element(By.ID, 'EmailInput')
password = driver.find_element(By.ID, 'PasswordInput')

username.send_keys(username_trash)
password.send_keys(password_trash)

driver.implicitly_wait(10)

# password.submit()

driver.implicitly_wait(10)

login_button_xpath = '//*[@id="mainContent"]/div/div/div[3]/div/div[1]/div/div/form/div[3]/div[2]/button'
login_button = driver.find_element(By.XPATH, login_button_xpath)
login_button.click()

driver.implicitly_wait(10)

session = requests.Session()
# session.post('https://www.wm.com/us/en/login', data={'username': username_trash, 'password': password_trash})
# response = session.get('https://www.wm.com/us/en/my-account/billing-history')

page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

bills = soup.find_all('div', {'class': 'bill-history__item'})

for bill in bills:
    date = bill.find('div', {'class': 'bill-history__date'}).text.strip()
    amount = bill.find('div', {'class': 'bill-history__amount'}).text.strip()
    print(f'{date} - {amount}')
