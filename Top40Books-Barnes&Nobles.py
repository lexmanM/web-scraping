#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 08:45:01 2022

@author: lexman
"""

import requests
import pandas as pd
import os
import time
import random
import codecs
from bs4 import BeautifulSoup

## Setting the headers

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'}

main_URL = "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
page1 = requests.get(main_URL, headers=headers)

## Iterating through the webpage's elements

soup1 = BeautifulSoup(page1.content, "html.parser")

urls = []
url_prefix = 'https://www.barnesandnoble.com'

for books in soup1.find_all('div', {'class': 'product-shelf-title'}):
    url = books.find('a')
    url2 = url_prefix + url['href']
    urls.append(url2)
    
len(urls)

## Saving them locally

for i in range(40):
    page2 = requests.get(urls[i], headers=headers)
    
    soup2 = BeautifulSoup(page2.content, "html.parser")
    
    file_name = "bn_top100_"+str(i+1)+".html"
    
    Html_file= open(file_name,"w")
    Html_file.write(str(soup2))
    Html_file.close()

    print("Page:", str(i+1), " saved!")
    wait_time = random.randrange(5,8)
    time.sleep(wait_time)
    
## Reading the local file to extract necessary information


for i in range(40):
    file_name = "bn_top100_"+str(i+1)+".html" 
    
    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        
        content = soup.find('div', {'class':'overview-cntnt'})
        # printing the first 100 characters of the overview text
        print(content.text.strip()[0:100], "\n")
            
            
            
            
            
