#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 21:07:39 2018

@author: Yuan
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
import time

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

actions = webdriver.common.action_chains.ActionChains(driver)

alerts = webdriver.common.alert.Alert(driver)



"""
get prof list
"""

url_wes = "https://iasext.wesleyan.edu/regprod/!wesmaps_page.html?stuid=&facid=NONE&page=search&term=1189"

driver.get(url_wes)


search_name = []

option = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[3]/select[2]')
all_faculty = Select(option).options

faculty_name = []

for faculty in all_faculty:
    faculty = faculty.text
    faculty_name.append(faculty)

all_faculty_name = faculty_name[1:-1]


url_rate = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Wesleyan+University&schoolID=1161&queryoption=TEACHER"

driver.get(url_rate)

dismiss_alert = driver.find_element_by_xpath('//*[@id="cookie_notice"]/a[1]').click()


all_reviews = []

search_space = lambda: driver.find_element_by_xpath('//*[@id="professor-name"]')


with open('reviews1.txt', 'w') as f:
    for name in all_faculty_name: 
        
        last_name = name.split(',')[0]
        no_midd = name.split(',')[1]
        first_name = no_midd.split(' ')[0]
        
        name = first_name + ' ' + last_name
        
        """
        search for name in wes
        """
        
        search_space().send_keys(name)
        
        time.sleep(5)
        
        try:
            num_of_professor = int(driver.find_element_by_class_name('professor-count').text)
            
        except:
            num_of_professor = int(driver.find_element_by_class_name('professor-count').text)
            
        if num_of_professor != 0:
            
            try:
                
                to_click = driver.find_element_by_class_name('name')
                to_click.click()
                
            except:
                
                to_click = driver.find_element_by_class_name('name')
                to_click.click()
            
            """
            collect info
            """
            try:
                
                Overall_Quality = "Overall Quality: " + \
                driver.find_element_by_xpath \
                ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[1]/div/div/div').text
                
                num_of_reviews = driver.find_element_by_class_name \
                ('rating-count').text
                
                
                tags = driver.find_elements_by_class_name \
                ('tag-box-choosetags')
                
                Level_of_Diff = 'Level of difficulty: ' + \
                driver.find_element_by_xpath \
                ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[2]/div').text
                
                Would_Take_Again = "Would Take Again: " + \
                driver.find_element_by_xpath \
                ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[1]/div').text
                
                review_for_class = driver.find_elements_by_class_name('response')[0].text
                
                review = driver.find_elements_by_class_name('commentsParagraph')[0].text
                
                list_tag = []
                for tag in tags:
                    list_tag.append(tag.text)
                
                prof_review = name + ' (' + num_of_reviews + ')' + '\n\n' \
                    + Overall_Quality + '\n' + Level_of_Diff + '\n' + Would_Take_Again + '\n\n'\
                    + str(list_tag) + '\n\n' + "Most recent review for " + review_for_class + ':' + '\n\n' + \
                    review + '\n\n\n'
            
            except:
                
                if 'http://www.ratemyprofessors.com/AddRating.jsp?tid=' not in driver.current_url:
                    Overall_Quality = "Overall Quality: " + \
                    driver.find_element_by_xpath \
    ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[1]/div/div/div').text
                    
                    num_of_reviews = driver.find_element_by_class_name \
                    ('rating-count').text
                    
                    Level_of_Diff = 'Level of difficulty: ' + \
                    driver.find_element_by_xpath \
    ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[2]/div').text
                
                    Would_Take_Again = "Would Take Again: " + \
                    driver.find_element_by_xpath \
    ('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[1]/div').text
                    
                    review_for_class = driver.find_elements_by_class_name \
                    ('response')[0].text
                    
                    review = driver.find_elements_by_class_name \
                    ('commentsParagraph')[0].text
                    
                    """
                    combine them into a block
                    """
                    
                    prof_review = name + ' (' + num_of_reviews + ')' + '\n\n' \
                    + Overall_Quality + '\n' + Level_of_Diff + '\n' + Would_Take_Again + '\n\n'\
                    + str(list_tag) + '\n\n' + "Most recent review for " + review_for_class + ':' + '\n\n' + \
                    review + '\n\n\n'
                    
                else:
                    prof_review = name + ": No information.\n\n\n"
                    
            f.write(prof_review)
           
            
            """
            close current window, return to the search page
            """
            driver.get(url_rate)
            time.sleep(5)
            
        else:     
            msg = name + ": No information.\n\n\n"
            
            search_space().clear()
            
            time.sleep(3)
            
            f.write(msg)
        

driver.close()        
        
        
    
    
    
        
        
        
        
        
        
        
        
        
        
        
