import os
import  dotenv
import pandas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd
import json

##This script load runs a function to create a dataset with reviews and ratings scrapped from goodreads.com from a list of more than 1000 books


dotenv.load_dotenv()

DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")

books = pd.read_csv('../INPUT/books_list.csv', header=None)

## Modified functions from goodread_utils.py

def gr_log(driver, user, password):
    username_field = driver.find_element_by_id("userSignInFormEmail")
    password_field = driver.find_element_by_id("user_password")

    username_field.send_keys(user)
    #driver.implicitly_wait(1)
        
    password_field.send_keys(password)
    #driver.implicitly_wait(1)

    #Click the submit button (the third element formbox)
    submit = driver.find_elements_by_class_name('formBox')
    submit[2].click()

    driver.implicitly_wait(3) 

def get_book(driver, name):
    try:
        inputs = driver.find_elements_by_tag_name('input')
    except:
        raise ValueError('I do not seem to find that book')    
    #The search box is the first input tag
    search_box = 0
    for i in inputs:
        search_box = i
        break      
    #Input the book name and hit enter
    search_box.send_keys(name)
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(4)

    #SELECT THE FIRST INSTANCE
    driver.find_element_by_class_name('bookTitle').click()
    
def get_book2(driver, name):
    '''
    Find book from within another book page
    '''
    inputs = driver.find_elements_by_class_name('searchBox__input')
    
    #Input the book name and hit enter
    inputs[0].send_keys(name)
    inputs[0].send_keys(Keys.RETURN)
    driver.implicitly_wait(4)

    #SELECT THE FIRST INSTANCE
    driver.find_element_by_class_name('bookTitle').click()

def get_GR_reviews(driver, reviews):
    reviews_container = driver.find_elements_by_class_name('review')
    rvws = {}
    number = len(reviews)
    for i, e in enumerate(reviews_container):
        try:
            grade = e.find_element_by_class_name('staticStar').text
            read = e.find_element_by_class_name('readable')
        except:
            continue
        try:
            read.find_element_by_link_text('...more').click()
        except:
            pass

        rev = read.find_elements_by_tag_name('span')
        rvws[number] = ({'review':rev[0].text.replace('\n', ''), 'grade':grade} if len(rev)==1 else {'review':rev[1].text.replace('\n', ''), 'grade':grade})
        number+=1
    reviews.update(rvws)

   
def get_gr_database(DRIVER, GR_USER, GR_PASS, books):
    '''
    Main function that uses the other functions to create a database with goodreads reviews and their rating
    '''
    driver = webdriver.Chrome(DRIVER)
    driver.get('https://www.goodreads.com/')
    driver.implicitly_wait(2)
    gr_log(driver, GR_USER, GR_PASS)
    get_book(driver, books[0].strip())
    driver.implicitly_wait(2)
    reviews = {}
    get_GR_reviews(driver, reviews)
    
    for name in books[1:]:
        get_book2(driver, name.strip())
        driver.implicitly_wait(2)
        get_GR_reviews(driver, reviews)
        
    driver.quit()
    with open("../OUTPUT/goodread_reviews_dataset.json", "r+") as file:
        data = json.load(file)
        data.update(reviews)
        file.seek(0)
        json.dump(data, file)
        
    return print(f'The reviews dataset has increased in {len(reviews)} reviews')

if __name__=='__main__':
    get_gr_database(DRIVER, GR_USER, GR_PASS, list(books[:200]))