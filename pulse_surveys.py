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

num_surveys = 50
surveys_completed = 0 
question_answers = Web_Functions.generate_answers(75)
while surveys_completed < num_surveys:
    # navigate to surveys page 
    Web_Functions.open_surveys_page(driver)

    # verify a survey card appears
    Web_Functions.wait_until_element_appears(driver, "survey-card")

    # find all available web surveys
    web_surveys = Web_Functions.find_available_web_surveys(driver)

    # open the first web survey available, save its stats
    curr_survey = web_surveys[0] 
    curr_survey.click()
    print(f"*** ANSWERING SURVEY: {curr_survey.text[2]}, {curr_survey.text[0]} points ***")
    Web_Functions.save_survey_stats(curr_survey.text)

    # verify that highlighted question appears
    Web_Functions.wait_until_element_appears(driver, "question-button-highlighted")

    question_buttons = driver.find_elements_by_class_name("question-button")
    question_buttons.insert(0, driver.find_element_by_class_name("question-button-highlighted"))
    submit_button, question_buttons = question_buttons[-1], question_buttons[:-1]

    print(f"NUM OF QUESTIONS: {len(question_buttons)}\n")

    for question in question_buttons: 
        Web_Functions.answer_question(driver, question, question_answers)
    
    print(f"\nSURVEY COMPLETED!\n")
    surveys_completed += 1

    # click the small submit button (the last item with question-button class)
    time.sleep(1)
    try: 
        submit_button.click()
    except StaleElementReferenceException: 
        print("StaleElement exception caught, clicking survey submit button")
    finally: 
        Web_Functions.wait_until_element_appears(driver, 'survey-submit-button')
        final_submit_btn = driver.find_element_by_class_name("survey-submit-button")
        final_submit_btn.click()
    
    time.sleep(1)

    # find the take new survey button and click it to return to surveys page 
    Web_Functions.wait_until_element_appears(driver, "//*[contains(text(), 'Take A Survey')]", find_type = By.XPATH)
    take_new_survey_btn = driver.find_element_by_xpath("//*[contains(text(), 'Take A Survey')]")
    try: 
        print(f"Take a Survey Button Text: {take_new_survey_btn.text}")
    except AttributeError: 
        print(f"AttributeError caught! Trying to click survey complete button another way")
        Web_Functions.wait_until_element_appears(driver, ".survey-complete-button.small", find_type = By.CSS_SELECTOR)
        small_complete_btns = driver.find_elements_by_css_selector(".survey-complete-button.small")
        small_complete_btns[1].click()
    else: 
        take_new_survey_btn.click()

    time.sleep(8)