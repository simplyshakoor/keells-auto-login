#!/usr/bin/env python
# coding: utf-8

# In[46]:


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


# In[47]:


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


# In[60]:


keells_url = 'https://int.keellssuper.net/'
KEELLS_LOGIN_HEADER = 'https://int.keellssuper.net/login'
KEELLS_LOGIN_SUCCESS_HEADER = 'Welcome to Keells Super-The First Online Supermarket in Sri Lanka'


WAIT_TIME_SECONDS = 60
start_time=datetime.datetime(2020,4,2,6,0,0)
PREFERED_CITY= ('Kohuwala''Boralesgamuwa','Dehiwala','Nugegoda','Colombo')
PREFERED_SUBURB= (('Kohuwala','Hathbodhiya','Dutugemunu'),
                   ('Rattanapitiya','Boralesgamuwa'),
                   ('Kalubowila','Nedimala','Karagampitiya'),
                   ('Delkanda','Nugegoda'),
                   ('Polhengoda','Havelock Town'))
notice1, notice2,notice3='','',''


# In[ ]:


url_read = 'https://int.keellssuper.net/'


# In[50]:


def keells_available(r):
    if KEELLS_LOGIN_HEADER in r:
        print('site available')
        return True
    else:
        print('site busy:',datetime.datetime.now())
        return False
    


# In[51]:


def select_suburb(suburb, city_index):
    town=''

    #Search for the availability of the preffered Surburb
    for x in PREFERED_SUBURB[city_index]:
        for option in suburb.find_elements_by_tag_name('option'):
            if option.text==x:
                town=option.text
                Select(suburb).select_by_visible_text(town)
                notice3='Selected Town : '+town
                return True
                break
    return False
#        


# In[52]:


def select_city(site):    
    deliveryCity = site.find_element_by_id('BodyContent_ddlDeliveryCity')
    city=''
    notice2='No prefered cities'

    #Search for the availability of the prefered city
    for x in PREFERED_CITY:
        for option in deliveryCity.find_elements_by_tag_name('option'):
            if option.text==x:
                city=x
                notice2='Selected City :'+x
                suburb = site.find_element_by_id('BodyContent_ddlSuburb')
                Select(deliveryCity).select_by_visible_text(x)
                if select_suburb(suburb,PREFERED_CITY.index(x)):
                    return True
                    break
            #print(option.text)
    
    # If no preferrerd city and preferred suburb combination is found then select first option just to login
    Select(deliveryCity).select_by_index(0)
    suburb = site.find_element_by_id('BodyContent_ddlSuburb')
    Select(suburb).select_by_index(0)   

    
    #    


# In[53]:


def notify_sound(count):
    duration = 1000  # milliseconds
    freq = 440  # Hz
    for i in range(count):
        winsound.Beep(freq, duration)


# In[54]:


now=datetime.datetime.now()
if now.hour<start_time.hour:
        time_to_start=start_time-now
        print('too early: waiting for',time_to_start.seconds-10,'s')
        time.sleep(time_to_start.seconds-10)


# In[55]:


browser = webdriver.Chrome()

while True:
    browser.get(keells_url)
    #keells = requests.get(keells_url)    
    if keells_available(browser.current_url):
        notify_sound(1)
        print('site opened, immediately check:',datetime.datetime.now())
        select_city(browser)
        break
    wait=WAIT_TIME_SECONDS+random.randint(-WAIT_TIME_SECONDS/2, WAIT_TIME_SECONDS/2)
    time.sleep(wait)
browser.current_url



username = browser.find_element_by_id('BodyContent_UserName')
username.send_keys(usernameStr)
password = browser.find_element_by_id('BodyContent_LoginPassword')
password.send_keys(passwordStr)
signInButton = browser.find_element_by_id('BodyContent_BtnLogin')
try:
    signInButton.click()
    if browser.title == KEELLS_LOGIN_SUCCESS_HEADER:
        notice1='Keells Logged in'
    notice1='Keells Logged in'
except:
    notice1='Keells Loggin Failed'
    notify_sound(3)


# In[61]:


toaster = ToastNotifier()
toaster.show_toast(notice1,notice2+'\n'+notice3)

