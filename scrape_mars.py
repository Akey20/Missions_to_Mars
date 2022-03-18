#imports
#import splinter, beautiful soup and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import html5lib
import pandas as pd
import datetime as dt

#scrape function and return a json that has the data, so it can be loaded into mongoDB
def scrape_all():
    #setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    #get information from news page
    ##scrape_news(browser)
    news_title, news_paragraph = scrape_news(browser)

    #dictionary using information from scrapes
    mars_Data = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now
    }

    #stop the webdriver
    browser.quit()
    
    #display data
    return mars_Data
   

#scrape mars news page
def scrape_news(browser):
    #go to news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    #optional delay for loading page
    # browser.is_element_present_by_css('div.list_text', wait_time=1)

   #convert html to soup object
   #convert to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    #find the first 'a' tag and save it as news_title
    news_title = slide_elem.find('div', class_ = 'content_title').get_text()
    #grabs the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    #return the news title & paragraph
    return news_title, news_p

#scrape image page
def scrape_feature_img(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

        #parse html with soup
    ###html = browser.html
    ###img_soup = soup(html, 'html.parser')
        #image url
   ### img_url_rel = img_soup = img_soup.find('img', class_='fancybox-img').get('src')
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img = img_soup.find('img', class_='headerimage fade-in')
    img_link = img['src']

    featured_image_url = url + img_link

       
        #absolute url
    url_2 = 'https://spaceimages-mars.comimage/featured/mars2.jpg'
    ###img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    ###return img_url
        
    return url_2



#scrape facts page
def scrape_facts_page(browser):
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #find location for facts
    factsLocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factsLocation.find('table')

    #create empty string
    facts = ""
    # add text then return
    facts += str(factTable)
    return facts

   

#scrape hemispheres page
def scrape_hemispheres(browser):
    #url
    url= "https://marshemispheres.com/"
    browser.visit(url)

    #list to hold images & titles
    hemisphere_image_urls = []

    #loop
    for i in range(4):
       #hemisphere
        hemisphereInfo = {}
        #find the elements on each loop
        browser.find_by_css('a.product-item img')[i].click()
        #find sample image anchor tag and extract
        sample = browser.links.find_by_text('Sample').first
        # print(sample)
        hemisphereInfo["img_url"] = sample['href']
            
        #get hemisphere title
        hemisphereInfo['title']= browser.find_by_css('h2.title').text
        
        #append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
                
        
        browser.back()
             

    #return hemisphere urls w/titles
    return hemisphere_image_urls







if __name__ == "__main__":
    print(scrape_all())