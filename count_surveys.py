import random
import time
import json
from datetime import timedelta
from selenium.webdriver.common.by import By
from web_functions import Web_Functions
from selenium.webdriver.common.action_chains import ActionChains

driver = Web_Functions.open_site('https://collegepulse.com/app/answer') 
Web_Functions.open_surveys_page(driver)

Web_Functions.wait_until_element_appears(driver, 'page-number ')
page_numbers = driver.find_elements_by_class_name('page-number ')
print(f"SURVEY PAGES FOUND: {len(page_numbers)}\n")
time.sleep(5)

for i in range(1, len(page_numbers) + 1): 
    # click page_number
    Web_Functions.wait_until_element_appears(driver, str(i), By.ID)
    page_number = driver.find_element_by_id(str(i))
    print(f"... clicking page {page_number.text} button ...")
    ActionChains(driver).move_to_element(page_number).click(page_number).perform() 

    time.sleep(2.5)
    surveys = Web_Functions.find_available_surveys(driver, type="all")
    web = surveys[0]
    mobile = surveys[1]
    web_stats = {"points": 0, "respondents": 0, "time": "00:00:00", "names": []}
    mobile_stats = {"points": 0, "respondents": 0, "time": "00:00:00", "names": []}

    for survey in web: 
        survey_text = survey.text.split('\n')
        print(f"WEB: {survey_text}")
        web_stats["points"] += int(survey_text[0])
        web_stats["respondents"] += int(survey_text[3])
        web_stats["time"] = Web_Functions.add_times(web_stats['time'], survey_text[-1])
        web_stats["names"].append(survey_text[2])
    for survey in mobile: 
        survey_text = survey.text.split('\n')
        print(f"MOBILE: {survey_text}")
        mobile_stats["points"] += int(survey_text[2])
        mobile_stats["respondents"] += int(survey_text[5])
        mobile_stats["time"] = Web_Functions.add_times(mobile_stats['time'], survey_text[-1])
        mobile_stats["names"].append(survey_text[4])

        # write these stats to a file to keep track
    with open(r'tests\all_survey_stats.json', 'r') as fp:
        all_survey_stats = json.load(fp)
    
    all_survey_stats["Total_Surveys"] += len(web) + len(mobile)
    all_survey_stats["Web_Surveys"] += len(web)
    all_survey_stats["Mobile_Surveys"] += len(mobile)
    all_survey_stats["Mobile_Points_Available"] += mobile_stats["points"]
    all_survey_stats["Web_Points_Available"] += web_stats["points"]
    all_survey_stats["Total_Points_Available"] += mobile_stats["points"] + web_stats["points"]
    all_survey_stats["Web_Time_Expected"] = Web_Functions.add_times(all_survey_stats["Web_Time_Expected"], web_stats['time'])
    all_survey_stats["Mobile_Time_Expected"] = Web_Functions.add_times(all_survey_stats["Mobile_Time_Expected"], mobile_stats['time'])
    all_survey_stats["Total_Time_Expected"] = Web_Functions.add_times(all_survey_stats["Web_Time_Expected"], all_survey_stats["Mobile_Time_Expected"])
    all_survey_stats["Web_Total_Respondents"] += web_stats["respondents"]
    all_survey_stats["Mobile_Total_Respondents"] += mobile_stats["respondents"]
    all_survey_stats["Total_Respondents"] += mobile_stats["respondents"] + web_stats["respondents"]
    [all_survey_stats["Web_Survey_List"].append(name) for name in web_stats["names"]]
    [all_survey_stats["Mobile_Survey_List"].append(name) for name in mobile_stats["names"]]
        
    with open(r'tests\all_survey_stats.json', 'w') as fp:
        json.dump(all_survey_stats, fp, indent=2)

    print(f"SURVEYS FOUND on PAGE {page_number.text}: WEB {len(web)} MOBILE {len(mobile)}")

