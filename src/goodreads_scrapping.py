import os
import dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from goodread_utils import *

dotenv.load_dotenv()


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")
BOOK_NAME = input('Give me a book to look for: ')

def GR_scrapping(DRIVER, GR_PASS, GR_USER, BOOK_NAME):
    driver = webdriver.Chrome(DRIVER)

    #Open web:
    driver.get('https://www.goodreads.com/')
    driver.implicitly_wait(3)


    ###LOG IN TO GOODREADS ACCOUNT:
    gr_log(driver, GR_USER, GR_PASS)


    ###FIND A BOOK
    get_book(driver, BOOK_NAME)
    driver.implicitly_wait(3)


    #GET THE REVIEWS
    reviews = get_GR_reviews(driver)

    #Save json:

    with open('../OUTPUT/data.json', 'w') as fp:
        json.dump(reviews, fp)

    driver.quit()
