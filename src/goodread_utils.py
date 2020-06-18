from selenium.webdriver.common.keys import Keys

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
    driver.implicitly_wait(3)

    #SELECT THE FIRST INSTANCE
    driver.find_element_by_class_name('bookTitle').click()