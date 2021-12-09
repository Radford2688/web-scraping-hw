# pyimport os
import pandas as pd
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import requests
import pymongo
import pprint

def scrape_info():
    mars={}
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    mars_url= ("https://redplanetscience.com/")
  

    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    print (soup.prettify())
    titles = soup.find_all('div', class_='content_title')
    articles = soup.find_all('div', class_='article_teaser_body')
    news_title=titles[0].get_text()
    print (news_title)

    news_p=articles[0].get_text()
    print (news_p)
    Mars_df=pd.read_html("https://galaxyfacts-mars.com")
    Mars_facts=Mars_df[0]
    Mars_facts
    Mars_html=Mars_facts.to_html()
    Mars_html


    space_image_url= ('https://spaceimages-mars.com')
    browser.visit(space_image_url)
    browser.links.find_by_partial_text("FULL IMAGE").click()
    html=browser.html
    soup=bs(html, 'html.parser')
    image=soup.find('img', class_="fancybox-image")["src"]
    featured_image_url='https://spaceimages-mars.com/'+image
    print (featured_image_url)

    Mars_df=pd.read_html("https://galaxyfacts-mars.com")
    Mars_facts=Mars_df[0]
    Mars_facts

    Mars_html=Mars_facts.to_html()
    Mars_html

    hemisphere_url="https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    hemisphere_links=browser.links.find_by_partial_text("Hemisphere Enhanced")
    hemisphere_image_urls=[]
    for link in range(len(hemisphere_links)):
        browser.links.find_by_partial_text("Hemisphere Enhanced")[link].click()
        html=browser.html
        soup=bs(html, 'html.parser')
        hemisphere_dic={}
        hemisphere=soup.find('h2',class_='title')
        hemisphere_dic["title"]=hemisphere.get_text()
        img_link_list=soup.find('div',class_='downloads').find_all('a')
        for img_link in img_link_list:
            if img_link.text == "Original":
                img_link_full = f"{hemisphere_url}{img_link['href']}"
                hemisphere_dic["img_url"]=img_link_full
                hemisphere_image_urls.append(hemisphere_dic)
                browser.back()
        
    # print (hemisphere_image_urls)
    mars={
        'title':news_title,
        'paragraph':news_p,
        'featured_image':featured_image_url,
        'hemisphere_image':hemisphere_image_urls,
        'mars_facts': Mars_html
    }
    return(mars)
