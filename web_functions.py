import time
import random
import json
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Web_Functions():
    ''' 
    A set of functions to be used for the Selenium Chrome Webdriver
    Also designed for automated survey taking on the Pulse website 
    ''' 

    @staticmethod
    def open_site_new_session(url): 
        ''' Using a new Chrome session, create a Chrome webdriver and open the specified site '''
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(r"C:\chromedriver_win32\chromedriver.exe", options = chrome_options)
        return Web_Functions.redirect_to_page(driver, url)

    @staticmethod
    def open_site(url): 
        ''' Using a folder to save cookies, create a Chrome webdriver and open the website''' 
        # use a user-data-dir folder to save cookies and login info 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=selenium") 
        
        # create a driver
        driver = webdriver.Chrome(r"C:\chromedriver_win32\chromedriver.exe", options = chrome_options)

        # open pulse page and wait for it to redirect
        return Web_Functions.redirect_to_page(driver, url)
    
    @staticmethod
    def redirect_to_page(driver, url): 
        driver.get(url) 
        try: 
            WebDriverWait(driver, 10).until(lambda driver: driver.current_url == url)
        except TimeoutException: 
            print(f"Failed to redirect to {url}, timeout after 10 seconds")
        return driver

    @staticmethod 
    def wait_until_element_appears(driver, element, find_type = By.CLASS_NAME, wait_time = 10): 
        ''' 
        Wait specified time until a specified element appears in the browser 
        If element appears, return True; else, return False 
        ''' 
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((find_type, element)))
        except TimeoutException:
            print(f"Page timed out after {wait_time}, element '{element}' not found")
            return False
        return True 

    @staticmethod
    def open_rewards_page(driver): 
        ''' Open the rewards page from the Pulse homepage '''
        Web_Functions.wait_until_element_appears(driver, "rewards", find_type = By.ID)
        rewards_page = driver.find_element_by_id("rewards")
        rewards_page.click()
        time.sleep(.25)

    @staticmethod 
    def open_surveys_page(driver): 
        ''' Open the surveys page from the Pulse homepage'''
        # verify that surveys page button appears, navigate to surveys page 
        Web_Functions.wait_until_element_appears(driver, "surveys", find_type = By.ID)
        surveys_page = driver.find_element_by_id("surveys")
        surveys_page.click()
        time.sleep(.25)
    
    @staticmethod 
    def find_available_surveys(driver, type="web"): 
        ''' 
        Find all available surveys in current page and return the list of survey-card WebElements
        arg type -- the type of surveys to be returned ('mobile', 'web', or 'all', by default web) 
        if 'all' is selected, returns a tuple of lists (web_surveys, mobile surveys)
        ''' 

        Web_Functions.wait_until_element_appears(driver, ".survey-card", find_type=By.CSS_SELECTOR)
        all_surveys = driver.find_elements_by_css_selector(".survey-card")
        mobile_surveys = driver.find_elements_by_css_selector(".survey-card.mobile-only")
        web_surveys = [survey for survey in all_surveys if survey not in mobile_surveys]
        print(f"\nSURVEYS AVAILABLE: MOBILE - {len(mobile_surveys)} | WEB - {len(web_surveys)}")
        
        # if there are no web_surveys on this page, navigate to another one and check recursively
        if type == "web" and not web_surveys: 
            page_numbers = driver.find_elements_by_class_name('page-number ')
            page_number = random.choice(page_numbers)
            print(f"No web surveys found, proceeding to another random page (pg. {page_number.text})")
            ActionChains(driver).move_to_element(page_number).click(page_number).perform() # move to item and click it
            web_surveys = Web_Functions.find_available_surveys(driver)

        if type == "web": return web_surveys
        elif type == "mobile": return mobile_surveys
        else: return (web_surveys, mobile_surveys)

    @staticmethod
    def save_survey_stats(survey_text, time_taken): 
        ''' 
        Saves the passed survey bot_stats to a JSON file 
        arg survey -- the .text value for a WebElement item, split by '\n'
        arg time_taken -- the time taken for survey completion by bot
        ''' 

        survey_points = survey_text[0]
        survey_name = survey_text[2]
        survey_respondents = survey_text[3]
        survey_questions = survey_text[-2]
        survey_time = survey_text[-1]

        # write these stats to a file to keep track
        with open(r'tests\pulse_bot_stats.json', 'r') as fp:
            bot_stats = json.load(fp)
        
        bot_stats["Total_Points_Accumulated"] += int(survey_points)
        bot_stats["Surveys_Completed"].append({
            "name" : survey_name, 
            "points" : survey_points, 
            "respondents" : survey_respondents, 
            "questions" : survey_questions,
            "expected_time" : f"00:{survey_time}",
            "bot_time" : str(timedelta(seconds=round(time_taken)))
        })
            
        with open(r'tests\pulse_bot_stats.json', 'w', encoding='utf-8') as fp:
            json.dump(bot_stats, fp, indent=2, ensure_ascii = False)
    
    @staticmethod
    def add_times(curr_time, new_time): 
        ''' Takes two times (one current, one to add to current value) and adds them using timedeltas, returns string '''
        curr_split = list(map(int, curr_time.split(":")))
        new_split = list(map(int, new_time.split(":")))
        if len(curr_split) == 3:
            hrs, mins, secs = curr_split
            curr_time = timedelta(hours = hrs, minutes = mins, seconds = secs)
        else: 
            mins, secs = curr_split
            curr_time = timedelta(minutes = mins, seconds = secs)
        if len(new_split) == 3:
            hrs, mins, secs = new_split
            new_time = timedelta(hours = hrs, minutes = mins, seconds = secs)
        else: 
            mins, secs = new_split
            new_time = timedelta(minutes = mins, seconds = secs)
        return str(curr_time + new_time)

    @staticmethod
    def generate_answers(num_answers): 
        ''' Returns an array of answers '''
        driver = Web_Functions.open_site_new_session("https://randomwordgenerator.com/sentence.php")

        question_answers = [
        "I don't care", 
        "I'm not sure", 
        "Why do you ask?", 
        "Big Oof notation", 
        "Yikes" ]

        answer_num = driver.find_element_by_css_selector(".form-control.input-sm")
        answer_num.clear()
        answer_num.send_keys(str(num_answers))

        generate_button = driver.find_element_by_css_selector(".btn.btn-primary")
        generate_button.click()

        generated_answers = driver.find_elements_by_class_name("support-sentence")
        question_answers = [answer.text for answer in generated_answers]

        with open('generated_answers.txt', 'w') as file:
            file.write('\n'.join(question_answers))

        driver.quit()

        return question_answers

    @staticmethod 
    def answer_question(driver, question, text_answers): 
        ''' Answer the specified question 
        arg question -- a WebElement specifying a question_button
        arg text_answers -- a list of strings to be used as answers in text input fields''' 

        # scroll to top of window 
        driver.execute_script("scrollBy(0,250);")
        question.click()
        
        # print out the current question 
        question_text = driver.find_element_by_class_name("question-text").text
        print(f"... Answering question:\n {question_text} ...")

        input_boxes, answer_boxes, num_boxes, check_boxes = [], [], [], []

        # find all the types of answer inputs 
        time.sleep(.5)
        if Web_Functions.wait_until_element_appears(driver, "mc-option", By.CLASS_NAME, wait_time=1): 
            input_boxes = driver.find_elements_by_class_name("mc-option")
        elif Web_Functions.wait_until_element_appears(driver, "answer-box", By.ID, wait_time=1): 
            answer_boxes = driver.find_elements_by_id("answer-box")
        elif Web_Functions.wait_until_element_appears(driver, "numeric-input-box", By.ID, wait_time=1): 
            num_boxes = driver.find_elements_by_id("numeric-input-box")

        print(f"# OPTION BOXES: {len(input_boxes)} # ANSWER BOXES: {len(answer_boxes)} # CHECK BOXES: {len(check_boxes)} # NUM BOXES: {len(num_boxes)}")

        # answer the question depending on the input type
        if answer_boxes: 
            driver.execute_script("scrollBy(0,250);")
            answer_boxes[0].send_keys(random.choice(text_answers))
        elif input_boxes: 
            driver.execute_script("scrollBy(0,250);")
            option_chosen = random.choice(input_boxes[:4])
            try: 
                option_chosen.click()
            except WebDriverException: 
                action = ActionChains(driver)
                action.move_to_element(option_chosen).perform()
                time.sleep(.5)
                option_chosen.click()
            driver.execute_script("scrollBy(0,250);")
        elif num_boxes: 
            driver.execute_script("scrollBy(0,250);")
            if "GPA" in question_text:
                num_boxes[0].send_keys("2.69")
            elif "Keystones" in question_text: 
                num_boxes[0].send_keys("420")
            else: 
                num_boxes[0].send_keys(str(random.randint(0, 5)))   
        else: 
            print(f"New input type on question {question}!")

        time.sleep(.5)

    @staticmethod
    def submit_survey(driver): 
        ''' Submits a finished survey ''' 

        time.sleep(2)

        # continue to submit survey
        try: 
            Web_Functions.wait_until_element_appears(driver, 'survey-submit-button')
            final_submit_btn = driver.find_element_by_class_name("survey-submit-button")
            final_submit_btn.click()
        except (StaleElementReferenceException, NoSuchElementException) as error: 
            print(f"Error caught, clicking submit button")
            print(error)
            submit_button = driver.find_elements_by_class_name("question-button")[-1]
            submit_button.click()
            Web_Functions.wait_until_element_appears(driver, 'survey-submit-button')
            final_submit_btn = driver.find_element_by_class_name("survey-submit-button")
            final_submit_btn.click()
        
        time.sleep(1)

        Web_Functions.check_if_too_fast(driver)

        # find the take new survey button and click it to return to surveys page 
        try: 
            driver.find_element_by_xpath("//*[contains(text(), 'Take A Survey')]")
        except NoSuchElementException:
            Web_Functions.wait_until_element_appears(driver, 'survey-submit-button')
            final_submit_btn = driver.find_element_by_class_name("survey-submit-button")
            final_submit_btn.click()
        finally:
            time.sleep(1)
            # navigate back to the homepage to ensure we go back to survey answering page
            Web_Functions.wait_until_element_appears(driver, 'icon-container')
            pulse_logo_btn = driver.find_element_by_class_name("icon-container")
            pulse_logo_btn.click()

    @staticmethod
    def check_if_too_fast(driver):
        ''' If too fast message appears, wait a few seconds and then resubmit '''
        if Web_Functions.wait_until_element_appears(driver, 'too-fast-message', wait_time=1): 
            print(f"Submitted the survey too quickly! Trying again")
            go_back_btn = driver.find_element_by_class_name("go-back-container")
            go_back_btn.click()
            time.sleep(1)
            submit_button = driver.find_elements_by_class_name("question-button")[-1]
            submit_button.click()

    



