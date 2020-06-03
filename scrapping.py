#SELENIUM TUTORIAL:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#https://sites.google.com/a/chromium.org/chromedriver/downloads
PATH = '/home/david/Chrome_web_driver/chromedriver'
driver = webdriver.Chrome(PATH)

#Open web and get title:
driver.get('https://techwithtim.net')
print(driver.title)

##Navigate through buttom clicking:
link = driver.find_element_by_link_text("Python Programming")
link.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sow-button-19310003"))
    )
    element.click()
except:
    driver.quit()

driver.back()
driver.back()
driver.back()

##Search bars and retrieve results:
search = driver.find_element_by_name('s')    
search.send_keys("test")
search.send_keys(Keys.RETURN)

#Wait until the key has been found:
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)
finally:
    driver.quit()


time.sleep(5)
#driver.quit()   