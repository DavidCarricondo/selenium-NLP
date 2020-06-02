from selenium import webdriver

#https://sites.google.com/a/chromium.org/chromedriver/downloads
PATH = '/home/david/Chrome_web_driver/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get('https://techwithtim.net')
print(driver.title)
driver.quit()