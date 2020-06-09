import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()


DRIVER = os.getenv("DRIVER")
TWITTER_PASS = os.getenv("TWITTER_PASS")
TWITTER_USER = os.getenv("TWITTER_USER")

driver = webdriver.Chrome(DRIVER)

###LOG IN TO TWITTER ACCOUNT:

#Open web:
driver.get('https://twitter.com/login')

driver.implicitly_wait(5) 
username_field = driver.find_element_by_name("session[username_or_email]")
password_field = driver.find_element_by_name("session[password]")


username_field.send_keys(TWITTER_USER)
driver.implicitly_wait(1)
    
password_field.send_keys(TWITTER_PASS)
driver.implicitly_wait(1)

#Click the submit button
driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div').click()

###GET THE SHOWN TWEETS
'''
try:
    tweet_boxes = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.cssSelector, "[data-testid: \"tweet\"]"))
    )
    print(tweet_boxes)
    
except:
    driver.quit()
'''
driver.implicitly_wait(5)
tweet_boxes = driver.find_element_by_css_selector(".tweet")

print(tweet_boxes)
