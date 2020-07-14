from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def get_book(driver, name, log=False):
    if log==True:
        try:
            inputs = driver.find_elements_by_tag_name('input')
        except:
            raise ValueError('I do not seem to find that book')    
        #The search box is the first input tag
        search_box = 0
        for i in inputs:
            search_box = i
            break
    else:
        search_box = driver.find_element_by_id('sitesearch_field')        
    #Input the book name and hit enter
    search_box.send_keys(name)
    search_box.send_keys(Keys.RETURN)

    #close log-in banner
    close_button_path = "/html/body/div[3]/div/div/div[1]" 
    wait = WebDriverWait(driver, 10)
    close_button = wait.until(EC.visibility_of_element_located((By.XPATH, close_button_path)))
    close_button .click()

    #SELECT THE FIRST INSTANCE
    driver.find_element_by_class_name('bookTitle').click()

def get_GR_reviews(driver):
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
    return reviews

def get_title_and_pic(driver):

    title = driver.find_element_by_id('bookTitle').text
    
    author = driver.find_element_by_id('bookAuthors')
    authors = author.find_elements_by_class_name('authorName')
    aut = ', '.join([aut.text for aut in authors])

    title_author = title.upper() + '\n' + aut

    pic = driver.find_element_by_id('coverImage').get_attribute("src")

    return title_author, pic



    
