from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='list_text').find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    #JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    link = soup.find('div', class_='carousel_items').find('a')["data-fancybox-href"]
    featured_image_url = f'https://www.jpl.nasa.gov{link}'

    #MARS WEATHER
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('div',class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text

    #MARS FACTS
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['description', 'value']
    html_table = df.to_html(index=False)
    html_table = html_table.replace('\n', '')

    #MARS HEMISPHERE
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    all_hemisphere = soup.find_all('div', class_="description")

    hemisphere_url = []

    for info in all_hemisphere:
        #store title
        title = info.h3.text
        
        #get links to page with image
        link_to_image = info.find('a')["href"]
        
        #go to page with image link
        browser.visit(f'https://astrogeology.usgs.gov/{link_to_image}')
        html = browser.html
        new_soup = bs(html, 'html.parser')
        #get image link
        
        img_url = new_soup.find('div', class_="downloads").find_all('li')[0].a["href"]
        
        #create dictionary
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['image_url'] = img_url
        
        hemisphere_url.append(hemisphere_dict)

    mars_dict = {}

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": html_table,
        "hemisphere_images": hemisphere_url
        }

    return mars_dict
