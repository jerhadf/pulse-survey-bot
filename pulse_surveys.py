import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from web_functions import Web_Functions

pulse = Web_Functions(user="selenium")

driver = pulse.open_site('https://collegepulse.com/app/answer') 

num_surveys = 300
surveys_completed = 0 
question_answers = pulse.generate_answers(75)

while surveys_completed < num_surveys:

    # navigate to surveys page and sort by number of responses
    if not pulse.open_surveys_page(): 
        print("No more surveys available! Quitting the bot")
        driver.quit()
        break

    # find all available web surveys, open the first available one 
    web_surveys = pulse.find_available_surveys(driver)
    curr_survey = pulse.open_survey(web_surveys[0])
    start_time = time.time() # keep track of time survey started

    for question in curr_survey['question_btns']: 
        pulse.answer_question(question, question_answers)
    
    pulse.submit_survey()

    elapsed_time = time.time() - start_time # keep track of time bot took on survey

    pulse.save_survey_stats(curr_survey['text'], elapsed_time)

    surveys_completed += 1
    print(f"\nSURVEY COMPLETED in {round(elapsed_time)} secs! surveys completed in this run: {surveys_completed}")

driver.quit()