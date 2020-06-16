import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")

driver = webdriver.Chrome(DRIVER)

###LOG IN TO GOODREADS ACCOUNT:

#Open web:
driver.get('https://www.goodreads.com/')

driver.implicitly_wait(5) 
username_field = driver.find_element_by_id("userSignInFormEmail")
password_field = driver.find_element_by_id("user_password")


username_field.send_keys(GR_USER)
driver.implicitly_wait(1)
    
password_field.send_keys(GR_PASS)
driver.implicitly_wait(1)

#Click the submit button
submit = driver.find_elements_by_class_name('formBox')
submit[2].click()

driver.implicitly_wait(5) 

#driver.quit()
