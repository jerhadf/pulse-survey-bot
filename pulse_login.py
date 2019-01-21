''' 
DEPRECATED
Attempted to login to Pulse but don't need to because I can save browser session
'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def check_exists_by_ID(element): 
    try: 
        driver.find_element_by_id(element)
    except NoSuchElementException: 
        return False
    return True

chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(r"C:\chromedriver_win32\chromedriver.exe", options = chrome_options)

driver.get('https://collegepulse.com/app/answer') # navigate to pulse 

# LOGIN TO PULSE
email = "jeremy.hadfield.21@dartmouth.edu"
email_box = driver.find_element_by_id("email")
email_box.send_keys(email)
pass_box = driver.find_element_by_id("password1")
pass_box.send_keys(Keys.RETURN)

# wait for Dartmouth login page to show up
wait = WebDriverWait(driver, 40)
wait.until(lambda driver: driver.current_url[:29] == "https://websso.dartmouth.edu/")

netID = "f0036dh"
netID_box = driver.find_element_by_id("userid")
netID_box.send_keys(netID, Keys.RETURN)

password = "Gyrf@lc0n"
pass_box_Dart = driver.find_element_by_id("Bharosa_Password_PadDataField")
pass_box_Dart.send_keys(password, Keys.RETURN)

challenge = {
    "mascot" : "Lion", 
    "state" : "Utah", 
    "first_job" : "Provo", 
    "holiday" : "Labor Day"
}

challenge_options = [val for val in challenge.values()]
challenge_box = driver.find_element_by_id("Bharosa_Challenge_PadDataField")
challenge_box.send_keys(challenge_options[0], Keys.RETURN)

option_num = 1
while check_exists_by_ID("errorMessage"): # if error, try the next value
    challenge_box.send_keys(challenge_options[option_num], Keys.RETURN)
    option_num += 1
        
# wait for Pulse survey page to show up 
wait = WebDriverWait(driver, 20)
wait.until(lambda driver: driver.current_url == "https://collegepulse.com/app/answer")

# time.sleep(2) 
# print(driver.page_source)
# first_survey = driver.find_element_by_css_selector("div.survey-card")
# first_survey.click() 
# time.sleep(2) 

# first_input = driver.find_element_by_id('stkv-text-10c6bc953552bd9a')
# first_input.send_keys("Toobler Amb")