# AutoPulse: An Automated Bot to Take Pulse Surveys

## Description

This is an automated bot, built with Python and Selenium, to automatically take surveys on CollegePulse.com. Pulse is a startup collecting information from college students to assist with data-driven marketing. The company started at Dartmouth by friends of mine, and I helped advise them with early-stage design and strategy decisions. One problem they had is that, like many startups, the code for the web app was written rapidly and, without tests, documentation, or any automated way to confirm that the site still worked. After hearing my friend talk about this problem, I decided to engage in some white-hat hacking, using my experience in automated testing to create a tool to complete all of the surveys on the website extremely rapidly. 

To do this, I had to bypass Captchas, timers, and other questions used to prevent bots from taking the surveys. I also collected data from the surveys, including the questions answered, time spent, total respondents for each survey, and more. The codebase became large enough that I had to implement object-oriented programming for Python, using Classes, functions, and PEP 8 style documentation to make the code functional, extensible, and easy to interpret. 

Ultimately, I reached out to my friend and showed them the bot. They were shocked to see its speed and success in taking surveys that were meant to be for only humans. Further, the bot was able to collect points that could be redeemed for rewards. After showing them the tool, I helped Pulse implement changes to fix the vulnerabilities and add automated tests to their web app. I’m proud of this project because I took my own initiative to singlehandedly improve a startup’s product at a vulnerable and early stage. I also applied good design practices for code in Python to enable the startup to conduct test-driven development. CollegePulse is now a successful startup accepted at YCombinator S18, and most of the code I wrote is still in use for automated testing.

## Demo

Here's a quick video demonstration of the bot in action. 

https://youtu.be/QbEZDLqxWPc

## Setup process

**Selenium installation**: https://selenium-python.readthedocs.io/installation.html

**Short Survey-Automation Blog Post I Used*: http://devinmancuso.com/blog/2015/using-selenium-to-mess-with-survey-monkey.html

**Automating the Web with Selenium (blog post)**: https://irwinkwan.com/2013/04/05/automating-the-web-with-selenium-complete-tasks-automatically-and-write-test-cases/

## Stats
These are underestimates, as I started running the bot before I set up the stats-tracking and saving part. 

**Total Pulse points accumulated (2 different accounts)**: 17160

**Total Pulse surveys taken**: 1421 

**Shortest time taken on a single survey**: 10 seconds (expected time 50 seconds)
