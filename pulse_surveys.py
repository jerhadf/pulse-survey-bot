import time
import random
import re 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from web_functions import Web_Functions

driver = Web_Functions.open_site('https://collegepulse.com/app/answer') 

num_surveys = 100
surveys_completed = 0 
question_answers = Web_Functions.generate_answers(75)
while surveys_completed < num_surveys:

    # navigate to surveys page and sort by most recent surveys
    Web_Functions.open_surveys_page(driver)
    Web_Functions.wait_until_element_appears(driver, 'date', find_type = By.ID)
    newest_surveys_btn = driver.find_element_by_id('date')
    newest_surveys_btn.click()

    # verify a survey card appears
    Web_Functions.wait_until_element_appears(driver, "survey-card")

    # find all available web surveys
    web_surveys = Web_Functions.find_available_web_surveys(driver)

    curr_survey_text = web_surveys[0].text.split('\n')
    web_surveys[0].click()
    print(f"*** ANSWERING SURVEY: {curr_survey_text[2]} ***")

    start_time = time.time() # keep track of time survey started

    # verify that highlighted question appears
    Web_Functions.wait_until_element_appears(driver, "question-button-highlighted")

    question_buttons = driver.find_elements_by_class_name("question-button")
    question_buttons.insert(0, driver.find_element_by_class_name("question-button-highlighted"))
    question_buttons = question_buttons[:-1]

    print(f"NUM OF QUESTIONS: {len(question_buttons)}\n")

    for question in question_buttons: 
        Web_Functions.answer_question(driver, question, question_answers)
        time.sleep(1)
    
    print(f"\nSURVEY COMPLETED!\n")
    surveys_completed += 1

    Web_Functions.submit_survey(driver)

    elapsed_time = time.time() - start_time # keep track of time bot took on survey

    Web_Functions.save_survey_stats(curr_survey_text, elapsed_time)