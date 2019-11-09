#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import datetime as dt


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# # NASA Mars News

# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = slide_element.find(
            "div", class_="content_title").get_text()
        news_p = slide_element.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    return news_title, news_p


# JPL Mars Space Images - Featured Image


# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


# Use splinter to navigate the site and find the image url for the current Featured Mars Image
# and assign the url string to a variable called `featured_image_url`
    JPL_Navigation = browser.find_by_id("full_image")
    JPL_Navigation.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None
   # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url


# Mars Weather


# Mars Weather Twitter Account Web Scraper
def twitter_weather(browser):
    # Visit the Mars Weather Twitter Account
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    Marsweather_soup = BeautifulSoup(html, "html.parser")

    # scrape the latest "Mars weather" tweet from the page
    tweet = Marsweather_soup.find("div",
                                  attrs={
                                      "class": "tweet",
                                               "data-name": "Mars Weather"
                                  })
   # Search Within Tweet for <p> Tag Containing Tweet Text
    mars_weather = tweet.find("p", "tweet-text").get_text()
    return mars_weather


# Mars Facts

# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description", inplace=True)

    return mars_df.to_html(classes="table table-striped")


# Mars Hemispheres

# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()

        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)

        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# Helper Function


def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


# Main Web Scraping Bot

def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data


if __name__ == "__main__":
    print(scrape())
