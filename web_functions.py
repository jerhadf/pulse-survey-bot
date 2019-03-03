import time
import random
import json
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Web_Functions():
    """ 
    A set of functions to be used for the Selenium Chrome Webdriver
    Also designed for automated survey taking on the Pulse website 
    """

    def __init__(self, user="selenium"):
        """
        Setup instance variables and class-level constants
        """
        self.STATS_FILE = r"tests\survey_stats\pulse_bot_stats.json"
        self.driver = None # initialized to none, set in open_site
        self.user = user

    def click(self, element):
        """ 
        Moves to the WebElement item and then clicks it
        returns -- none 
        """
        ActionChains(self.driver).move_to_element(
            element).click(element).perform()

    def open_site_new_session(self, url):
        """ 
        Using a new Chrome session, create a Chrome webdriver and open the specified site 
        returns -- the function redirect_to_page(url)
        """
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(
            r"C:\chromedriver_win32\chromedriver.exe", options=chrome_options)
        return self.redirect_to_page(url)

    def open_site(self, url):
        """ 
        Using a folder to save cookies, create a Chrome webdriver and open the website
        """
        # use a user-data-dir folder to save cookies and login info
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={self.user}")

        # create a self.driver
        self.driver = webdriver.Chrome(
            r"C:\chromedriver_win32\chromedriver.exe", options=chrome_options)

        # open pulse page and wait for it to redirect
        return self.redirect_to_page(url)

    def redirect_to_page(self, url):
        """
        Navigates to the specified url in the driver
        returns -- the driver after navigating to the url
        """
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.current_url == url)
        except TimeoutException:
            print(f"Failed to redirect to {url}, timeout after 10 seconds")
        return self.driver

    def wait_until_element_appears(self, element, find_type=By.CLASS_NAME, wait_time=10):
        """ 
        Wait specified time until a specified element appears in the browser 
        returns -- If element appears, return True; else, return False 
        """
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((find_type, element)))
        except TimeoutException:
            print(
                f"Page timed out after {wait_time}, element '{element}' not found")
            return False
        return True

    def open_rewards_page(self):
        """ Open the rewards page from the Pulse homepage """
        self.wait_until_element_appears(
            "rewards", find_type=By.ID)
        rewards_page = self.driver.find_element_by_id("rewards")
        self.click(rewards_page)

    def open_surveys_page(self):
        """ 
        Open the surveys page from the Pulse homepage
        returns -- if No surveys are available, return False; else, True 
        """
        # verify that surveys page button appears, navigate to surveys page
        self.wait_until_element_appears("surveys", find_type=By.ID)
        surveys_page = self.driver.find_element_by_id("surveys")
        self.click(surveys_page)

        # click the button to sort surveys by # of responses (b/c more responses tends to == more points)
        responses = self.wait_until_element_appears(
            'responses', find_type=By.ID)
        if not responses:
            return False
        else:
            sort_by_responses_btn = self.driver.find_element_by_id('responses')
            self.click(sort_by_responses_btn)
            return True

    def find_available_surveys(self, type="web"):
        """ 
        Find all available surveys in current page and return the list of survey-card WebElements
        arg type -- the type of surveys to be returned ('mobile', 'web', or 'all', by default web) 
        returns -- if 'all' is selected, returns a tuple of lists (web_surveys, mobile surveys)
        """

        self.wait_until_element_appears(
            ".survey-card", find_type=By.CSS_SELECTOR)
        all_surveys = self.driver.find_elements_by_css_selector(".survey-card")
        mobile_surveys = self.driver.find_elements_by_css_selector(
            ".survey-card.mobile-only")
        web_surveys = [
            survey for survey in all_surveys if survey not in mobile_surveys]
        print(
            f"\nSURVEYS AVAILABLE: MOBILE - {len(mobile_surveys)} | WEB - {len(web_surveys)}")

        # if there are no web_surveys on this page, navigate to another one and check recursively
        if type == "web" and not web_surveys:
            page_numbers = self.driver.find_elements_by_class_name(
                'page-number ')
            page_number = random.choice(page_numbers)
            print(
                f"No web surveys found, proceeding to another random page (pg. {page_number.text})")
            self.click(page_number)
            web_surveys = self.find_available_surveys()

        if type == "web":
            return web_surveys
        elif type == "mobile":
            return mobile_surveys
        else:
            return (web_surveys, mobile_surveys)

    def open_survey(self, web_survey):
        """ 
        Open the survey and verify that it appears 
        arg web_survey -- a WebElement object that represents a survey button (e.g. 'survey-card' class)
        returns -- {'text': survey .text value, split by newlines, 
                'question_btns': list of WebElements for each question_button in survey}
        """

        survey_text = web_survey.text.split('\n')
        self.click(web_survey)

        # verify that the survey opens by looking for question-button elements
        if self.wait_until_element_appears("question-button"):
            question_btns = self.driver.find_elements_by_class_name(
                "question-button")
            question_btns.insert(0, self.driver.find_element_by_class_name(
                "question-button-highlighted"))
            question_btns = question_btns[:-1]
        else:
            print(
                f"Error caught in open_survey; question-button not found, opening new survey")
            web_surveys = self.find_available_surveys()
            # open a new survey recursively
            return self.open_survey(web_surveys[0])

        print(
            f"*** ANSWERING SURVEY: {survey_text[2]}, {survey_text[0]} points***")
        print(f"NUM OF QUESTIONS: {len(question_btns)}\n")

        return {'text': survey_text, 'question_btns': question_btns}

    def save_survey_stats(self, survey_text, time_taken):
        """ 
        Saves the passed survey bot_stats to a JSON file 
        arg survey -- the .text value for a WebElement item, split by newlines
        arg time_taken -- the time taken for survey completion by bot
        """

        survey_points = survey_text[0]
        survey_name = survey_text[2]
        survey_respondents = survey_text[3]
        survey_questions = survey_text[-2]
        survey_time = survey_text[-1]

        # write these stats to a file to keep track
        with open(self.STATS_FILE, 'r') as fp:
            bot_stats = json.load(fp)

        bot_stats["Total_Points_Accumulated"] += int(survey_points)
        bot_stats["Surveys_Completed"].append({
            "name": survey_name,
            "date_taken": datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
            "points": survey_points,
            "respondents": survey_respondents,
            "questions": survey_questions,
            "expected_time": f"00:{survey_time}",
            "bot_time": str(timedelta(seconds=round(time_taken)))
        })
        bot_stats["Total_Surveys_Taken"] = int(
            len(bot_stats["Surveys_Completed"]))

        with open(self.STATS_FILE, 'w') as fp:
            json.dump(bot_stats, fp, indent=2)

    def add_times(self, curr_time, new_time):
        """ 
        Takes two times (one current, one to add to current value) and adds them using timedeltas
        returns -- string output of curr_time + new_time 
        """
        curr_split = list(map(int, curr_time.split(":")))
        new_split = list(map(int, new_time.split(":")))
        if len(curr_split) == 3:
            hrs, mins, secs = curr_split
            curr_time = timedelta(hours=hrs, minutes=mins, seconds=secs)
        else:
            mins, secs = curr_split
            curr_time = timedelta(minutes=mins, seconds=secs)
        if len(new_split) == 3:
            hrs, mins, secs = new_split
            new_time = timedelta(hours=hrs, minutes=mins, seconds=secs)
        else:
            mins, secs = new_split
            new_time = timedelta(minutes=mins, seconds=secs)
        return str(curr_time + new_time)

    def generate_answers(self, num_answers):
        """ 
        returns -- an array of strings, randomly generated answers 
        """
        self.driver = self.open_site_new_session(
            "https://randomwordgenerator.com/sentence.php")

        question_answers = [
            "I don't care",
            "I'm not sure",
            "Why do you ask?",
            "Big Oof notation",
            "Yikes"]

        answer_num = self.driver.find_element_by_css_selector(
            ".form-control.input-sm")
        answer_num.clear()
        answer_num.send_keys(str(num_answers))

        generate_button = self.driver.find_element_by_css_selector(
            ".btn.btn-primary")
        self.click(generate_button)

        generated_answers = self.driver.find_elements_by_class_name(
            "support-sentence")
        question_answers = [answer.text for answer in generated_answers]

        self.driver.quit()

        return question_answers

    def answer_question(self, question, text_answers):
        """ 
        Answer the specified question 
        arg question -- a WebElement specifying a question_button
        arg text_answers -- a list of strings to be used as answers in text input fields
        """

        # scroll to top of window
        self.driver.execute_script("scrollBy(0,250);")
        time.sleep(.3)
        self.click(question)
        time.sleep(.5)

        # print out the current question
        self.wait_until_element_appears(
            self.driver, "question-text", wait_time=2)
        question_text = self.driver.find_element_by_class_name(
            "question-text").text
        print(f"... Answering question:\n {question_text} ...")

        input_boxes, answer_boxes, num_boxes = [], [], []

        # find all the types of answer inputs
        if self.wait_until_element_appears("mc-option", wait_time=1):
            input_boxes = self.driver.find_elements_by_class_name("mc-option")
        elif self.wait_until_element_appears("answer-box", find_type=By.ID, wait_time=1):
            answer_boxes = self.driver.find_elements_by_id("answer-box")
        elif self.wait_until_element_appears("numeric-input-box", find_type=By.ID, wait_time=1):
            num_boxes = self.driver.find_elements_by_id("numeric-input-box")

        print(
            f"# OPTION BOXES: {len(input_boxes)} \
             # ANSWER BOXES: {len(answer_boxes)} \
             # # NUM BOXES: {len(num_boxes)}")
        time.sleep(.3)

        # answer the question depending on the input type
        if answer_boxes:
            self.driver.execute_script("scrollBy(0,250);")
            answer_boxes[0].send_keys(random.choice(text_answers))
        elif input_boxes:
            self.driver.execute_script("scrollBy(0,250);")
            option_chosen = random.choice(input_boxes[:5])
            self.click(option_chosen)
            self.driver.execute_script("scrollBy(0,250);")
        elif num_boxes:
            self.driver.execute_script("scrollBy(0,250);")
            if "GPA" in question_text:
                num_boxes[0].send_keys("2.69")
            elif "Keystones" in question_text:
                num_boxes[0].send_keys("420")
            else:
                num_boxes[0].send_keys(str(random.randint(0, 5)))
        else:
            print(f"New input type on question {question}!")

        time.sleep(.3)

    def submit_survey(self):
        """ 
        Submits a finished survey 
        returns -- none 
        """
        if self.wait_until_element_appears("question-button", wait_time=1):
            submit_btn = self.driver.find_elements_by_class_name(
                "question-button")[-1]
            self.click(submit_btn)

        self.wait_until_element_appears("survey-submit-button")
        final_submit_btn = self.driver.find_element_by_class_name(
            "survey-submit-button")
        self.click(final_submit_btn)
        self.check_if_too_fast()
        time.sleep(.5)

        # navigate back to the homepage to ensure we go back to survey answering page
        self.wait_until_element_appears('icon-container')
        pulse_logo_btn = self.driver.find_element_by_class_name(
            "icon-container")
        self.click(pulse_logo_btn)

    def check_if_too_fast(self):
        """ 
        If too fast message appears, wait a few seconds and then resubmit 
        returns -- none
        """
        if self.wait_until_element_appears('too-fast-message', wait_time=1):
            print(f"Submitted the survey too quickly! Trying again")
            self.wait_until_element_appears('go-back-container', wait_time=1)
            go_back_btn = self.driver.find_element_by_class_name(
                "go-back-container")
            self.click(go_back_btn)
            time.sleep(.75)
            self.wait_until_element_appears(
                self.driver, 'question-button', wait_time=1)
            submit_btn = self.driver.find_elements_by_class_name(
                "question-button")[-1]
            self.click(submit_btn)
            self.submit_survey()
