#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:25:57 2022

@author: lexman
"""

from bs4 import BeautifulSoup
import requests
import time

# PART 1

# (1)

# Hitting the login page to check if it responds with a cookie

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}

session = requests.Session()
print(session.cookies.get_dict())
response = session.get('https://www.planespotters.net/user/login', headers=headers)
print(session.cookies.get_dict())

## The cookie that comes with the response of the initial hit
cookie1 = session.cookies.get_dict()

## Hidden input field that will be required for the login process
URL = "https://www.planespotters.net/user/login"
page1 = requests.get(URL, headers=headers, cookies=cookie1)
doc1 = BeautifulSoup(page1.content, 'html.parser')

input = doc1.select("div.planespotters-form input[name=csrf]")[0];
csrf = input.get("value")
print(csrf)

input = doc1.select("div.planespotters-form input[name=rid]")[0];
rid = input.get("value")
print(rid)

# The rid variable seemed to be populated when I checked the website but it returns None sometimes. It's not needed all the time I guess.

# (2)

time.sleep(5)

session_requests = requests.session()

res = session_requests.post(URL, data = {"username" : "xalukin",
                                         "password" : "b8n9m0",
                                         "csrf": csrf,
                                         "rid": rid},
                            headers = headers,
                            cookies = cookie1,
                            timeout = 15)

# (3)

cookie2 = session_requests.cookies.get_dict()
#print(cookie2)

# (4)

URL2 = 'https://www.planespotters.net/member/profile'

page2 = session_requests.get(URL2,
                             headers=headers, 
                             cookies=cookie2)
        
doc2 = BeautifulSoup(page2.content, 'html.parser')

# (5)

print(doc2)

print("COOKIE1: ",cookie1,"\n")
print("COOKIE2: ",cookie2)

print(bool(doc2.findAll(text = "xalukin"))) 













