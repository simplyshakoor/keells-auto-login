#!/usr/bin/env python
# coding: utf-8

# In[49]:


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


# In[50]:


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


# In[51]:


keells_url = 'https://int.keellssuper.net/'
KEELLS_LOGIN_HEADER = 'https://int.keellssuper.net/login'
KEELLS_LOGIN_SUCCESS_HEADER = 'Welcome to Keells Super-The First Online Supermarket in Sri Lanka'


WAIT_TIME_SECONDS = 180
start_time=datetime.datetime(2020,4,2,6,0,0)
PREFERED_CITY= ('Kohuwala','Boralesgamuwa','Dehiwala','Nugegoda','Colombo')
PREFERED_SUBURB= (('Kohuwala','Hathbodhiya','Dutugemunu'),
                   ('Rattanapitiya','Boralesgamuwa'),
                   ('Kalubowila','Nedimala','Karagampitiya'),
                   ('Delkanda','Nugegoda'),
                   ('Polhengoda','Havelock Town'))
notice1, notice2,notice3='','',''


# In[52]:


PREFERED_LOC_TEST={
    '1':{
        'city':'Kohuwala'
        'suburb':['Kohuwala','Hathbodhiya','Dutugemunu']
    },
    '2':{
        'city':'Boralesgamuwa'
        'suburb':['Rattanapitiya','Boralesgamuwa']
    },
    '3':{
        'city':'Dehiwala'
        'suburb':['Kalubowila','Nedimala','Karagampitiya']
    },
    '4':{
        'city':'Nugegoda'
        'suburb':['Delkanda','Nugegoda']
    },
    '5':{
        'city':'Colombo'
        'suburb':['Polhengoda','Havelock Town']
    }
}


# In[53]:


url_read = 'https://int.keellssuper.net/'
url="https://member.daraz.lk/user/login?spm=a2a0e.home.header.d5.675a4625BepTpy&redirect=https%3A%2F%2Fwww.daraz.lk%2F"
usernameStr = 'Enter Your User Name Here'
passwordStr = 'Enter Your Password Here'


# In[54]:


#r = requests.get('https://member.daraz.lk')


# In[55]:


def keells_available(r):
    if KEELLS_LOGIN_HEADER in r:
        print('site available')
        return True
    else:
        print('site busy:',datetime.datetime.now())
        return False
    


# In[56]:


def select_suburb(suburb, city_index):
    town=''

    #Search for the availability of the preffered Surburb
    for y in PREFERED_SUBURB[city_index]:
        print('looking for suburb:',y)
        for option in suburb.find_elements_by_tag_name('option'):
            if option.text==y:
                print(option.text,'city available')
                town=option.text
                Select(suburb).select_by_visible_text(town)
                notice3='Selected Town : '+town
                print(notice3)
                return True
                break
    return False
#        


# In[57]:


def select_city(site):    
    deliveryCity = site.find_element_by_id('BodyContent_ddlDeliveryCity')
    city=''
    notice2='No prefered cities'

    #Search for the availability of the prefered city
    for x in PREFERED_CITY:
        print('looking for city:',x)
        for option in deliveryCity.find_elements_by_tag_name('option'):
            if option.text==x:
                city=x
                notice2='Selected City :'+x
                print(notice2)
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


# In[58]:


def login(browser):
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


# In[59]:


def notify_sound(count):
    duration = 1000  # milliseconds
    freq = 440  # Hz
    for i in range(count):
        winsound.Beep(freq, duration)


# In[44]:


now=datetime.datetime.now()
if now.hour<start_time.hour:
        time_to_start=start_time-now
        print('too early: waiting for',time_to_start.seconds-10,'s')
        time.sleep(time_to_start.seconds-10)


# In[60]:


browser = webdriver.Chrome()

while True:
    quick_attempts=random.randint(1,5)
    for i in range(quick_attempts):
        print('attempting',i+1,' of ',quick_attempts)
        browser.get(keells_url)  
        time.sleep(1)
        if keells_available(browser.current_url):
            notify_sound(1)
            print('site opened, immediately check:',datetime.datetime.now())
            select_city(browser)
            login(browser)
            break
            break
        wait_short= random.randint(int(wait/100),int(3*wait/200))
        time.sleep(wait_short)
    wait=random.randint(WAIT_TIME_SECONDS/2, 3*WAIT_TIME_SECONDS/2)
    print(quick_attempts,'attempts failed.', 'system will retry in ',wait,' seconds')
    time.sleep(wait)
browser.current_url


# In[ ]:


notice3


# In[ ]:



def win_notice(txt):
    toaster = ToastNotifier()
    toaster.show_toast(txt)
    
txt=notice1,notice2+'\n'+notice3
win_notice(txt)

