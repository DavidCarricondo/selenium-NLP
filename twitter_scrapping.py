import os
import dotenv
from selenium import webdriver

dotenv.load_dotenv()


DRIVER = os.getenv("DRIVER")
TWITTER_PASS = os.getenv("TWITTER_PASS")
TWITTER_USER = os.getenv("TWITTER_USER")

driver = webdriver.Chrome(DRIVER)

###LOG IN TO TWITTER ACCOUNT:

#Open web and get title:
driver.get('https://twitter.com/login')

driver.implicitly_wait(5) 
username_field = driver.find_element_by_name("session[username_or_email]")
password_field = driver.find_element_by_name("session[password]")
#css-1dbjc4n r-18u37iz r-16y2uox r-1wbh5a2 r-1udh08x

username_field.send_keys(TWITTER_USER)
driver.implicitly_wait(1)
    
password_field.send_keys(TWITTER_PASS)
driver.implicitly_wait(1)

driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div').click()

driver.implicitly_wait(5)

