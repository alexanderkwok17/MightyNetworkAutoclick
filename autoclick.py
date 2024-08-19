from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml
import time 

conf = yaml.load(open('secret.yml'))
username = conf['site']['email']
password = conf['site']['password']
url = conf['site']['url']
# Create the webdriver object. Here the  
# chromedriver is present in the driver  
# folder of the root directory. 
# driver = webdriver.Chrome(r"./driver/chromedriver") 
driver = webdriver.Chrome()


  
# get https://www.geeksforgeeks.org/ 
driver.get(url) 

driver.find_element(By.NAME,"email").send_keys(username)
driver.find_element(By.NAME,"password").send_keys(password)

# driver.find_element(By.CLASS_NAME,"action").click()
driver.find_element(By.XPATH, '//*[@id="page-region"]/div/div/div/div[2]/div/div/div/div[2]/div[2]').click()
# driver.find_element(By.XPATH, '//*[@id="page-region"]/div/div/div/div[2]/div/div/div/div[2]/div[2]/a').click()
# /html/body/div[3]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]/a 
# <a class="basic-box-primary-action-button mighty-btn-square-large mighty-btn-filled-theme-color-button" href="#">Sign In</a>
time.sleep(60)
driver.find_element(By.XPATH, '//*[@id="user-menu"]/a/div[2]/div/div/div[2]').click()

driver.find_element(By.XPATH, '//*[@id="menu-list-item-user-menu-links-layout"]/div/div/div/div/div/div[2]/ul/li[2]/div/a').click()
time.sleep(15)
driver.find_element(By.XPATH, '//*[@id="mui-2-member_list"]/div/div[2]').click()
time.sleep(15)
driver.find_element(By.XPATH, '//*[@id="members-list-actions"]/a/span[2]').click()
time.sleep(15)
driver.find_element(By.XPATH, '//*[@id="flyout-content-region"]/div/div/a[1]').click()
time.sleep(15)
driver.find_element(By.XPATH, '//*[@id="modal-content-region"]/div/div/div[4]/a').click()
time.sleep(15)

