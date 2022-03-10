#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:10:17 2022

@author: lexman
"""

import requests
import pandas as pd
import numpy as np
import os
import time
import random
import codecs
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import json

os.chdir('/Users/lexman/Documents/msba/Coursework/BAX 422 - Data Design and Representation/Individual Project II')

## Question 1

for i in range(4):
    URL1 = "https://www.yelp.com/search?find_desc=donut+shop&find_loc=San+Francisco%2C+CA&start="+str(i*10)
    page1 = requests.get(URL1)
    
    soup1 = BeautifulSoup(page1.content, "html.parser")
    
    file_name = "sf_donut_shop_search_page_"+str(i+1)+".html"
    
    Html_file= open(file_name,"w")
    Html_file.write(str(soup1))
    Html_file.close()
    
    del soup1
    
    print("Page: ",str(i+1)," saved!")
    wait_time = random.randrange(10,15)
    time.sleep(wait_time)

## Question 2

def first_letter(s):
    m = re.search(r'[a-z]', s, re.I)
    if m is not None:
        return m.start()
    return -1

def first_dot(s):
    m = re.search(r'[.]', s, re.I)
    if m is not None:
        return m.start()
    return -1

for i in range(4):
    file_name = "sf_donut_shop_search_page_"+str(i+1)+".html" 
    print("\n","Page:",str(i+1), "\n")

    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        for item in soup.select('[class*=container]'):
            #print(item)
            if item.find('h3'): 
                name = item.find('h3').get_text() 

                strt_pt = first_letter(name)
                frst_dot = first_dot(name)

                # search rank and name
                rank = name[:frst_dot]
                name_cut = name[strt_pt:]
                print("Search Rank:", rank)
                print("Restaurant Name:", name_cut)

                # url
                url_ele = item.find('a')
                url = url_ele['href']
                print("https://www.yelp.com"+url)

                # rating
                print(item.select('[aria-label*=rating]')[0]['aria-label'])

                # reviews
                print("#Reviews: ",item.select('[class*=reviewCount]')[0].get_text())

                # price range $ signs
                try:
                    print("Price Range: ",item.select('[class*=priceRange]')[0].get_text())
                except:
                    pass

                # store tags
                tag_list = []
                for tags in item.find_all('button'):
                    #print(tags.get_text())
                    tag_list.append(tags.get_text())

                print("Store Tags: ", tag_list)

                # delivery & dine-in tags
                try:
                    tag_list2 = []
                    for tags2 in item.select('[class*=tagText]'):
                        #print(tags.get_text())
                        tag_list2.append(tags2.get_text())

                    print("Dining Tag: ", tag_list2)
                except:
                    pass

                # if one can order through Yelp
                try:
                    if item.select('[class*=platformSearchAction]')[0].get_text()=='Start Order':
                        print("Can order through Yelp!")

                except:
                    pass

                print("-----")


## Question 3

#Creating a pymongo client
client = MongoClient('localhost', 27017)

#Getting the database instance
db = client['yelp']

#Creating a collection
collection = db['sf_donut_shops']

for i in range(4):
    file_name = "sf_donut_shop_search_page_"+str(i+1)+".html" 
    print("Page:",str(i+1), "\n")

    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        for item in soup.select('[class*=container]'):
            #print(item)
            if item.find('h3'): 
                name = item.find('h3').get_text() 

                strt_pt = first_letter(name)
                frst_dot = first_dot(name)

                # search rank and name
                rank = name[:frst_dot]
                name_cut = name[strt_pt:]
                #print("Search Rank:", rank)
                #print("Restaurant Name:", name_cut)

                # url
                url_ele = item.find('a')
                url = url_ele['href']
                url2 = "https://www.yelp.com"+url
                #print("https://www.yelp.com"+url)

                # rating
                rating = item.select('[aria-label*=rating]')[0]['aria-label']
                #print(item.select('[aria-label*=rating]')[0]['aria-label'])

                # reviews
                review = item.select('[class*=reviewCount]')[0].get_text()
                #print("#Reviews: ",item.select('[class*=reviewCount]')[0].get_text())

                # price range $ signs
                try:
                    price_range = item.select('[class*=priceRange]')[0].get_text()
                    #print("Price Range: ",item.select('[class*=priceRange]')[0].get_text())
                except:
                    pass

                # store tags
                tag_list = []
                for tags in item.find_all('button'):
                    #print(tags.get_text())
                    tag_list.append(tags.get_text())

                #print("Store Tags: ", tag_list)

                # delivery & dine-in tags
                try:
                    tag_list2 = []
                    for tags2 in item.select('[class*=tagText]'):
                        #print(tags.get_text())
                        tag_list2.append(tags2.get_text())

                    #print("Dining Tag: ", tag_list2)
                except:
                    pass

                # if one can order through Yelp
                try:
                    if item.select('[class*=platformSearchAction]')[0].get_text()=='Start Order':
                        order_detail = "Can order through Yelp!"
                        #print("Can order through Yelp!")
                        doc1 = {"search rank": rank,
                                "shop": name_cut,
                                "url": url2,
                                "star rating": rating,
                                "number of reviews": review,
                                "price range": price_range,
                                "store tags": tag_list,
                                "delivery/dine-in tags": tag_list2,
                                "order tag": order_detail}
                except:
                    doc1 = {"search rank": rank,
                            "shop": name_cut,
                            "url": url2,
                            "star rating": rating,
                            "number of reviews": review,
                            "price range": price_range,
                            "store tags": tag_list,
                            "delivery/dine-in tags": tag_list2}
                    pass

                collection.insert_one(doc1)
                
                #print("-----")

                
                
## Question 4

for x in collection.find({},{"url": 1, "search rank": 1}):
    
    pg_url = x['url']
    rank = x['search rank']
    
    # to see how many shops' code are being executed
    print(rank)
    
    pages = requests.get(pg_url)
    
    soup2 = BeautifulSoup(pages.content, "html.parser")
    
    file_name = "sf_donut_shop_"+str(rank)+".html"
    
    Html_file= open(file_name,"w")
    Html_file.write(str(soup2))
    Html_file.close()
    
    del soup2
    
    #print("Page: ",str(i+1)," saved!")
    wait_time = random.randrange(10,15)
    time.sleep(wait_time)
    #print(x['url'])


    
    
## Question 5

for i in range(40):
    file_name = "sf_donut_shop_"+str(i+1)+".html" 
    print("\n","Shop:",str(i+1), "\n")

    with open(file_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

        for item in soup.select('[class*=stickySidebar--fullHeight]')[0]:
            q = item.find("a", rel="noopener")
            if q is None:
                pass
            else:
                print(q.get_text())

            temp1 = []
            temp2 = []
            for r in item.find_all("p", attrs={'data-font-weight':'semibold'}):
                for p in r.find_all("a"):
                    temp1.append(p.get_text())
                    #print(temp)
                temp2.append(r.get_text())

            #print(temp2)
            temp3 = np.setdiff1d(temp2,temp1)
            #print(temp3)
            
            for n in range(len(temp3)):
                if n<2:
                    print(temp3[n])
                    
            del temp1, temp2, temp3



## Question 6

for i in range(40):
    file_name = "sf_donut_shop_"+str(i+1)+".html" 
    #print("\n","Shop:",str(i+1), "\n")

    with open(file_name) as fp:
        website = None
        phone = None
        address = None
        latitude = None
        longitude = None
        
        soup = BeautifulSoup(fp, 'html.parser')

        item = soup.select('[class*=stickySidebar--fullHeight]')[0]
        q = item.find("a", rel="noopener")
        if q is None:
            website = None
        else:
            website = q.get_text()

        temp1 = []
        temp2 = []
        for r in item.find_all("p", attrs={'data-font-weight':'semibold'}):
            for p in r.find_all("a"):
                temp1.append(p.get_text())
                #print(temp)
            temp2.append(r.get_text())

        #print(temp2)
        temp3 = np.setdiff1d(temp2,temp1)
        #print(temp3)

        if len(temp3)>1:
            if len(temp3[0])==14:
                phone = temp3[0]
                address = temp3[1]
            elif len(temp3[0]) > 14:
                address = temp3[0]
        elif len(temp3)==1:
            if len(temp3[0])==14:
                phone = temp3[0]
                address = temp3[1]
            elif len(temp3[0]) > 14:
                address = temp3[0]
        else:
            pass

        # creating the API endpoint
        temp_url = str("http://api.positionstack.com/v1/forward?access_key=bdc014e49a70470e31e2a49985bd666e&query="+address)
        #print(temp_url)

        t = requests.get(temp_url)
        json_temp = t.json()

        latitude = json_temp['data'][0]['latitude']
        longitude = json_temp['data'][0]['longitude']
        
        print(website, "\n", phone, "\n", address, "\n", latitude, "\n", longitude)  

        #print(collection.find_one())

        # updating the additional information extracted
        db.sf_donut_shops.update_one({"search rank": str(i+1)},{"$set": {"website": website,
                                                                         "phone number": phone,
                                                                         "address": address,
                                                                         "latitude": latitude,
                                                                         "longitude": longitude}})

        
        del temp1, temp2, temp3, temp_url, json_temp, website, phone, address, latitude, longitude 


# Creating an index based on search rank
from pymongo import MongoClient, ASCENDING, DESCENDING

db.sf_donut_shops.create_index([('search rank', ASCENDING )],
                               name='rank index', default_language='english')

















