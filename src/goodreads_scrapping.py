import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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

#Click the submit button (the third element formbox)
submit = driver.find_elements_by_class_name('formBox')
submit[2].click()

driver.implicitly_wait(5) 


###FIND A BOOK

BOOK_NAME = input('Give me a book to look for: ')

inputs = driver.find_elements_by_tag_name('input')

#The search box is the first input tag
search_box = 0
for i in inputs:
    search_box = i
    break

#Input the book name and hit enter
search_box.send_keys(BOOK_NAME)
search_box.send_keys(Keys.RETURN)
driver.implicitly_wait(5)

#SELECT THE FIRST INSTANCE

driver.find_element_by_class_name('bookTitle').click()

#GET THE REVIEWS

reviews_container = driver.find_elements_by_class_name('review')

reviews = {}

for i, e in enumerate(reviews_container):
    reviews[i] = e.text

print(reviews)

#driver.quit()
