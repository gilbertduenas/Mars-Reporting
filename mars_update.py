# imports and froms
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "c:/windows/chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():
    # define variables
    browser = init_browser()
    url_news = 'https://mars.nasa.gov/news/'

### NASA Mars News ###############################################################

    # create news objects
    browser.visit(url_news)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find('div', class_="grid_layout")

    # scrape news
    news_title = articles.find('h3').text
    news_p = articles.find('div', class_='article_teaser_body').text

# JPL Mars Space Images - Featured Image ###############################################################

    # load url into soup
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.findAll('article', class_='carousel_item')

    # search through soup and save the url
    for article in articles:
        featured_image_url = 'https://www.jpl.nasa.gov' + str(re.findall(r"'(.*?)'", article['style'])[0])

### Mars Weather ###############################################################

    # load url into soup
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # load into soup and get the first tweet
    article = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = article.text.split('pic.twitter')[0]

### Mars Facts ###############################################################

    # # load url into soup
    # url = 'http://space-facts.com/mars/'
    # browser.visit(url)
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    # # save the table to a dataframe
    # data = []
    # table = soup.find('table')
    # rows = table.findAll('tr')

    # for row in rows:
    #     cols = row.findAll('td')
    #     cols = [ele.text.strip() for ele in cols]
    #     data.append([ele for ele in cols if ele]) 
    # data_df = pd.DataFrame(data, columns=['key', 'value'])

    # # save the dataframe to html
    # temp_dict = data_df.set_index('key').to_dict()
    # news_dict = temp_dict['value']

### Mars Hemispheres ###############################################################

    # load url into soup
    url_img = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_img)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # search through soup and save image dictionaries to a list
    articles = soup.findAll('a', class_='itemLink product-item')
    hemi_list = []
    count = 0
    for article in articles:
        href_partial = article['href'].replace('/search/map', '/download')
        if count%2 != 0:
            title = article.text.replace('Hemisphere Enhanced', '')
            img_url=(f'https://astropedia.astrogeology.usgs.gov{href_partial}.tif/full.jpg')
            d = dict(title=title, img_url=img_url)
            hemi_list.append(d)
        count += 1

    # save scraped data to a dictionary
    mars_data = {
        'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'mars_weather':mars_weather,
        'hemi_list':hemi_list
    }

# the end ##########################################################

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
