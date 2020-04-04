import webbrowser
import requests
import time
import datetime
import random
import winsound
from win10toast import ToastNotifier

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
keells_url = 'https://int.keellssuper.net/'
usernameStr = ''
passwordStr = ''

WAIT_TIME_SECONDS = 180
start_time=datetime.datetime(2020,4,2,6,0,0) #Only start time of 6am is important
PREFERED_CITY= ('Kohuwala''Boralesgamuwa','Dehiwala','Nugegoda','Colombo')
PREFERED_SUBURB= (('Kohuwala','Hathbodhiya','Dutugemunu'),
                   ('Rattanapitiya','Boralesgamuwa'),
                   ('Kalubowila','Nedimala','Karagampitiya'),
                   ('Delkanda','Nugegoda'),
                   ('Polhengoda','Havelock Town'))
                   
def keells_available(r):
    if 'Sorry.aspx' in r.text:
        print('site busy:',datetime.datetime.now())
        return False
    else:
        print('site available')
        return True
        
def notify_sound(count):
    duration = 1000  # milliseconds
    freq = 440  # Hz
    for i in range(count):
        winsound.Beep(freq, duration)
        
now=datetime.datetime.now()
if now.hour<start_time.hour:
        time_to_start=start_time-now
        print('too early: waiting for',time_to_start.seconds-10,'s')
        time.sleep(time_to_start.seconds-10)
        
browser = webdriver.Chrome()
while True:
    keells = requests.get(keells_url)    
    if keells_available(keells):
        #webbrowser.get(chrome_path).open(keells_url)
        notify_sound(1)
        print('site opened, immediately check:',datetime.datetime.now())
        browser.get((keells_url))
        break
    wait=WAIT_TIME_SECONDS+random.randint(-WAIT_TIME_SECONDS/2, WAIT_TIME_SECONDS/2)
    time.sleep(wait)
    
#Select the prefered city
DeliveryCity = browser.find_element_by_id('BodyContent_ddlDeliveryCity')
city=''
notice2='No prefered cities'

#Search for the availability of the prefered city
for x in PREFERED_CITY:
    for option in DeliveryCity.find_elements_by_tag_name('option'):
        if option.text==x:
            city=option.text
            notice2='Selected City :'+city
            break
        print(option.text)

try:
    Select(DeliveryCity).select_by_visible_text(city)
except:
    Select(DeliveryCity).select_by_index(0)
    
#Search for the availability of the preffered Surburb
Suburb = browser.find_element_by_id('BodyContent_ddlSuburb')
town=''

try:

    for x in PREFERED_SUBURB[PREFERED_CITY.index(city)]:
        for option in el.find_elements_by_tag_name('option'):
            if option.text==x:
                town=option.text
                notice3='Selected Town : '+town
                break
            print(option.text)
    town
except:
    notice3='No preffered towns'
#Select the preffered suburb
try:
    Select(Suburb).select_by_visible_text('Rattanapitiya')
except:
    Select(Suburb).select_by_index(0)

# Login with username and password
username = browser.find_element_by_id('BodyContent_UserName')
username.send_keys(usernameStr)
password = browser.find_element_by_id('BodyContent_LoginPassword')
password.send_keys(passwordStr)
signInButton = browser.find_element_by_id('BodyContent_BtnLogin')
try:
    signInButton.click()
    notice1='Keells Logged in'
except:
    notice1='Keells Loggin Failed'
    notify_sound(3)
    
# Generate windows notification
toaster = ToastNotifier()
toaster.show_toast(notice1,notice2+'\n'+notice3)
