import time
import random
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
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
    def find_available_web_surveys(driver): 
        ''' Find all available surveys in current page and return all web surveys ''' 
        all_surveys = driver.find_elements_by_css_selector(".survey-card")
        mobile_surveys = driver.find_elements_by_css_selector(".survey-card.mobile-only")
        web_surveys = [survey for survey in all_surveys if survey not in mobile_surveys]
        print(f"\nSURVEYS AVAILABLE: MOBILE - {len(mobile_surveys)} | WEB - {len(web_surveys)} \n")

        return web_surveys

    @staticmethod
    def save_survey_stats(survey): 
        ''' 
        Saves the passed survey bot_stats to a JSON file 
        arg survey -- the .text value for a WebElement item 
        ''' 

        survey_text = survey.split("\n")
        survey_points = survey_text[0]
        survey_name = survey_text[2]
        survey_respondents = survey_text[3]
        survey_questions = survey_text[-2]
        survey_time = survey_text[-1]

        # write these stats to a file to keep track
        with open('tests\pulse_bot_stats.json', 'r') as fp:
            bot_stats = json.load(fp)
        
        bot_stats["Total_Points_Accumulated"] += int(survey_points)
        bot_stats["Surveys_Completed"].append({
            "name" : survey_name, 
            "points" : survey_points, 
            "respondents" : survey_respondents, 
            "questions" : survey_questions,
            "expected_time" : survey_time
        })
            
        with open('tests\pulse_bot_stats.json', 'w') as fp:
            json.dump(bot_stats, fp, indent=2)

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
        time.sleep(1)
        if Web_Functions.wait_until_element_appears(driver, "mc-option", By.CLASS_NAME, wait_time=2): 
            input_boxes = driver.find_elements_by_class_name("mc-option")
        elif Web_Functions.wait_until_element_appears(driver, "answer-box", By.ID, wait_time=2): 
            answer_boxes = driver.find_elements_by_id("answer-box")
        #! Check boxes will never be populated because it is always reached after mc-option
        elif Web_Functions.wait_until_element_appears(driver, ".option-box.multi", By.CSS_SELECTOR, wait_time=2): 
            check_boxes = driver.find_elements_by_css_selector(".option-box.multi")
        elif Web_Functions.wait_until_element_appears(driver, "numeric-input-box", By.ID, wait_time=2): 
            num_boxes = driver.find_elements_by_id("numeric-input-box")

        print(f"# OPTION BOXES: {len(input_boxes)} # ANSWER BOXES: {len(answer_boxes)} # CHECK BOXES: {len(check_boxes)} # NUM BOXES: {len(num_boxes)}")

        # answer the question depending on the input type
        if answer_boxes: 
            answer_boxes[0].send_keys(random.choice(text_answers))
        elif input_boxes: 
            driver.execute_script("scrollBy(0,250);")
            if check_boxes: 
                random.choice(input_boxes).click()
                driver.execute_script("scrollBy(0,250);")
                random.choice(input_boxes).click()
                driver.execute_script("scrollBy(0,250);")
            random.choice(input_boxes).click()
            driver.execute_script("scrollBy(0,250);")
        elif num_boxes: 
            if "GPA" in question_text:
                num_boxes[0].send_keys("2.69")
            elif "Keystones" in question_text: 
                num_boxes[0].send_keys("420")
            else: 
                num_boxes[0].send_keys(str(random.randint(0, 5)))   
        else: 
            print(f"New input type on question {question}!")

        time.sleep(2)

    @staticmethod
    def submit_survey(driver): 
        # click the small submit button (the last item with question-button class)
        Web_Functions.wait_until_element_appears(driver, "question-button")

        submit_button = driver.find_elements_by_class_name("question-button")[-1]
        time.sleep(1)
        
        try: 
            submit_button.click()
        except StaleElementReferenceException: 
            print("StaleElement exception caught, trying to click survey submit button")
        finally: 
            Web_Functions.wait_until_element_appears(driver, 'survey-submit-button')
            final_submit_btn = driver.find_element_by_class_name("survey-submit-button")
            final_submit_btn.click()
        
        time.sleep(1)

        # find the take new survey button and click it to return to surveys page 
        Web_Functions.wait_until_element_appears(driver, "//*[contains(text(), 'Take A Survey')]", find_type = By.XPATH)
        take_new_survey_btn = driver.find_element_by_xpath("//*[contains(text(), 'Take A Survey')]")
        take_new_survey_btn.click()


    



