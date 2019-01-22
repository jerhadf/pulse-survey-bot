# List of All Errors I've Hit

## Run 1, 1/21/19 : NoSuchElementException, unable to locate question-button-highlighted

Bug with the bot where it failed to click a survey card and was thus unable to locate a question-button.

```python
SURVEY COMPLETED!
Page timed out after 10, element 'survey-submit-button' not found
Error caught, clicking submit button
Message: no such element: Unable to locate element: {"method":"class name","selector":"survey-submit-button"}
  (Session info: chrome=71.0.3578.98)
  (Driver info: chromedriver=2.45.615291 (ec3682e3c9061c10f26ea9e5cdcf3c53f3f74387),platform=Windows NT 10.0.17134 x86_64)
Page timed out after 1, element 'too-fast-message' not found
SURVEYS AVAILABLE: MOBILE - 0 | WEB - 8
*** ANSWERING SURVEY: American Dream ***
Page timed out after 10, element 'question-button-highlighted' not found
Traceback (most recent call last):
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\pulse_surveys.py", line 38, in <module>
    question_buttons.insert(0, driver.find_element_by_class_name("question-button-highlighted"))
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 564, in find_element_by_class_name
    return self.find_element(by=By.CLASS_NAME, value=name)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 978, in find_element
    'value': value})['value']
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"class name","selector":"question-button-highlighted"}
  (Session info: chrome=71.0.3578.98)
  (Driver info: chromedriver=2.45.615291 (ec3682e3c9061c10f26ea9e5cdcf3c53f3f74387),platform=Windows NT 10.0.17134 x86_64)
```

## Run 2, 1/21/19 : serious bugs in Pulse survey

The State of the Economys has lots of bugs that I reported -- the answers were wigging out, and it let me submit without finishing the survey.

```python
*** ANSWERING SURVEY: State of the Economy ***
NUM OF QUESTIONS: 7

... Answering question:
 Which of the following issues is the most important issue for you right now? ...
# OPTION BOXES: 15 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 How important of an issue is the economy to you? ...
# OPTION BOXES: 19 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
Traceback (most recent call last):
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\web_functions.py", line 215, in answer_question
    option_chosen.click()
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webelement.py", line 80, in click
    self._execute(Command.CLICK_ELEMENT)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webelement.py", line 633, in _execute
    return self._parent.execute(command, params)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: unknown error: Element <div class="mc-option" data="Somewhat Important
" data-reactid=".0.1.3.7.1.$=1$1.0.0.1:$Somewhat Important
">...</div> is not clickable at point (1275, 432). Other element would receive the click: <div class="mc-option-text-container" data-reactid=".0.1.3.7.1.$=1$0.0.0.1:$Medicare
.1.0">...</div>
  (Session info: chrome=71.0.3578.98)
  (Driver info: chromedriver=2.45.615291 (ec3682e3c9061c10f26ea9e5cdcf3c53f3f74387),platform=Windows NT 10.0.17134 x86_64)


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\pulse_surveys.py", line 44, in <module>
    Web_Functions.answer_question(driver, question, question_answers)
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\web_functions.py", line 220, in answer_question
    option_chosen.click()
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webelement.py", line 80, in click
    self._execute(Command.CLICK_ELEMENT)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webelement.py", line 633, in _execute
    return self._parent.execute(command, params)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\Guest User\AppData\Local\Programs\Python\Python37-32\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: unknown error: Element <div class="mc-option" data="Somewhat Important
" data-reactid=".0.1.3.7.1.$=1$1.0.0.1:$Somewhat Important
">...</div> is not clickable at point (1275, 432). Other element would receive the click: <div class="mc-option-text-container" data-reactid=".0.1.3.7.1.$=1$0.0.0.1:$Medicare
.1.0">...</div>
  (Session info: chrome=71.0.3578.98)
  (Driver info: chromedriver=2.45.615291 (ec3682e3c9061c10f26ea9e5cdcf3c53f3f74387),platform=Windows NT 10.0.17134 x86_64)
```

## Run 3, 1/21/19 : bug with saving stats

Bug where for some reason the bot collected Mobile-Only stats while taking the Online Harassment survey, which is a web survey.

```python
*** ANSWERING SURVEY: 10 ***
NUM OF QUESTIONS: 6

... Answering question:
 Have you ever been harassed or bullied online? ...
# OPTION BOXES: 3 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 Just your impression, who do you think is more likely to engage in bullying behavior online: women or men? ...
# OPTION BOXES: 3 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 Just your impression, who do you think is more likely to engage in bullying behavior online: conservatives or liberals? (Conservatives more likely, Liberals more likely) ...
# OPTION BOXES: 3 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 How often, if at all do you post messages or public comments on discussion boards? ...
# OPTION BOXES: 5 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 As far as you know, how good of a job are social media sites doing when it comes to addressing online harassment and online bullying? ...
# OPTION BOXES: 4 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0
... Answering question:
 Compared to other platforms, do you think there is more or less harassment and online bullying on College Pulse? ...
# OPTION BOXES: 6 # ANSWER BOXES: 0 # CHECK BOXES: 0 # NUM BOXES: 0

SURVEY COMPLETED!

Page timed out after 1, element 'too-fast-message' not found
Traceback (most recent call last):
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\pulse_surveys.py", line 54, in <module>
    Web_Functions.save_survey_stats(curr_survey_text, elapsed_time)
  File "c:\Users\Guest User\Desktop\Coding\pulse-testing\tests\web_functions.py", line 122, in save_survey_stats
    bot_stats["Total_Points_Accumulated"] += int(survey_points)
ValueError: invalid literal for int() with base 10: 'Mobile Only'
```