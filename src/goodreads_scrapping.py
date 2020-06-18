import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from goodread_utils import *

dotenv.load_dotenv()


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")

driver = webdriver.Chrome(DRIVER)

#Open web:
driver.get('https://www.goodreads.com/')
driver.implicitly_wait(3)


###LOG IN TO GOODREADS ACCOUNT:
gr_log(driver, GR_USER, GR_PASS)


###FIND A BOOK
BOOK_NAME = input('Give me a book to look for: ')
get_book(driver, BOOK_NAME)


#GET THE REVIEWS
driver.implicitly_wait(3)
reviews_container = driver.find_elements_by_class_name('review')

reviews = {}

for i, e in enumerate(reviews_container):
    rev_text = e.find_element_by_class_name('readable')
    rev_text = rev_text.find_elements_by_tag_name('span')
    for tx in rev_text:
        print(tx)
        reviews[i] = tx.text

print(reviews)

#driver.quit()
