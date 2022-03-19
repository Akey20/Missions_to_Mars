#imports
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import requests
import json


def scrape_info():
    
    #  init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    data = {}

    data["news_title"] = soup.find("div", class_="content_title").get_text()
    data["news_p"] = soup.find("div", class_="article_teaser_body").get_text()
    data["featured_image"] = get_featured(browser)
    data["mars_table"] = get_table()
    data["hemispheres"] = get_hemispheres(browser)

    browser.quit()

    return data



def get_featured(browser):
    
    #JPL Mars Space Images - Featured Image
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.body.find_all("img")[1]
   
    featured_image_url = url + "image/featured/mars2.jpg"
    
    return featured_image_url



def get_table():
    
    #Mars Facts
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)

    df = tables[0] 

    html_table = df.to_html()
     
    html_table.replace('\n', '')

    return df.to_html()



def get_hemispheres(browser):
    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    all_hemispheres = []
    for num in range(4):
        browser.find_by_css("a.product-item img")[num].click()
        all_hemispheres.append({
            'title':browser.find_by_css('h2.title')[0].text,
            'url':browser.find_by_text('Sample')[0]['href']
        })
        browser.back()

    return all_hemispheres