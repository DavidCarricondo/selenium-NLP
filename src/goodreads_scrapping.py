import os
import dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from src.goodread_utils import *

dotenv.load_dotenv()


def GR_scrapping(DRIVER, BOOK_NAME, GR_PASS=None, GR_USER=None):
    driver = webdriver.Chrome(DRIVER)

    #Open web:
    driver.get('https://www.goodreads.com/')
    driver.implicitly_wait(2)


    ###LOG IN TO GOODREADS ACCOUNT:
    #gr_log(driver, GR_USER, GR_PASS)


    ###FIND A BOOK
    get_book(driver, BOOK_NAME, log=False)
    driver.implicitly_wait(4)


    #GET THE REVIEWS
    title, author, pic = get_title_and_pic(driver)
    reviews = get_GR_reviews(driver)

    #Save json:
    #with open('OUTPUT/data.json', 'w') as fp:
    #    json.dump(reviews, fp)

    driver.quit()

    return reviews, title, author, pic
