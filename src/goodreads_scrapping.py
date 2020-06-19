import os
import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
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
    try:
        read = e.find_element_by_class_name('readable')
    except:
        continue
    try:
        read.find_element_by_link_text('...more').click()
    except:
        pass
    rev = read.find_elements_by_tag_name('span')
    reviews[i] = (rev[0].text if len(rev)==1 else rev[1].text)


#Save json:

with open('../OUTPUT/data.json', 'w') as fp:
    json.dump(reviews, fp)

driver.quit()
