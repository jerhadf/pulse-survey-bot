import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from web_functions import Web_Functions

driver = Web_Functions.open_site('https://collegepulse.com/app/answer') 

num_surveys = 300
surveys_completed = 0 
question_answers = Web_Functions.generate_answers(75)

while surveys_completed < num_surveys:

    # navigate to surveys page and sort by number of responses
    Web_Functions.open_surveys_page(driver)

    # find all available web surveys, open the first available one 
    web_surveys = Web_Functions.find_available_surveys(driver)
    curr_survey = Web_Functions.open_survey(driver, web_surveys[0])
    start_time = time.time() # keep track of time survey started

    for question in curr_survey['question_btns']: 
        Web_Functions.answer_question(driver, question, question_answers)
    
    Web_Functions.submit_survey(driver)

    elapsed_time = time.time() - start_time # keep track of time bot took on survey

    Web_Functions.save_survey_stats(curr_survey['text'], elapsed_time)

    surveys_completed += 1
    print(f"\nSURVEY COMPLETED in {elapsed_time} secs! surveys completed in this run: {surveys_completed}")

driver.quit()