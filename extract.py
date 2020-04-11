from lxml import html
import requests
from selenium import webdriver
import time
from xml.dom import minidom
import numpy as np
import pandas as pd
   

def main():
    # Initialize the driver
    driver = webdriver.Chrome()
    # Open provided link in a browser window using the driver
    driver.get("http://soccerverse.com/ranking_table")
    time.sleep(1)
    rank = np.array(0)
    team = np.array(0)
    country = np.array(0)
    points = np.array(0)
    # 103 pages for the above used website. Can be changed for other websites
    # FIXME: pass the page number and html tags as command line arguments
    # FIXME: make it more generic to use for other pages
    for i in range(103):
        paginateDiv = driver.find_element_by_id("rankingTable_paginate")
        paginateSpan = paginateDiv.find_element_by_tag_name("span")
        paginateButtons = paginateSpan.find_elements_by_tag_name('a')
        currentPage = str(i+1)
        print("we are on page number:", currentPage)
        for i in range(len(paginateButtons)):
            if paginateButtons[i].get_attribute('innerHTML') == currentPage:
                currentIndex = i
        print("index for the page number",currentIndex)
        paginateButtons[currentIndex].click()
        element = driver.find_element_by_tag_name("tbody")
        trows = element.find_elements_by_tag_name("td")
        for x in range(0, len(trows), 5):
            rank = np.append(rank, trows[x].get_attribute('innerHTML')) 
            team = np.append(team, trows[x+1].get_attribute('innerHTML'))
            country = np.append(country, trows[x+2].get_attribute('innerHTML'))
            points = np.append(points, trows[x+3].get_attribute('innerHTML'))
    
    soccerData = np.array([rank, team, country, points])
    soccerDf = pd.DataFrame({'rank': rank, 'team': team, 'country': country, 'points': points})
    soccerDf.to_csv('output.csv')
    

if __name__ == '__main__':
    main()