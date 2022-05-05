from bs4 import BeautifulSoup
from numpy import mask_indices
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

mars_information = {}

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def get_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find("div", class_="content_title")
    news_p = soup.find("div", class_="article_teaser_body")
    mars_information["news_title"] = news_title.text
    mars_information["news_paragraph"] = news_p.text
    browser.quit()
    return mars_information


def get_featured_image():
    browser = init_browser()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    images_url = "https://spaceimages-mars.com/"
    browser.visit(images_url)
    html_images = browser.html
    soup = BeautifulSoup(html_images, "html.parser")
    featured_image_url = (
        soup.find("div", class_="container mt-5")
        .find("div", class_="thmb")
        .find("img")["src"]
    )
    featured_image_url = f"https://spaceimages-mars.com/{featured_image_url}"
    mars_information["featured_image_url"] = featured_image_url
    browser.quit()
    return mars_information


def get_facts():
    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header=False, index=False)
    mars_information["mars_facts"] = mars_facts
    browser.quit()
    return mars_information

def get_hemispheres():
    browser = init_browser()
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    array_url = soup.find_all("div", class_="item")
    hemisphere_image_urls = []
    for item in array_url:
        title = item.find("h3").text
        p_img_url = item.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemispheres_url + p_img_url)
        p_img_url = browser.html
        soup = BeautifulSoup(p_img_url, "html.parser")
        image_url = hemispheres_url + soup.find("img", class_="thumb")["src"]
        hem_data = dict({"title": title, "img_url": image_url})
        hemisphere_image_urls.append(hem_data)

    mars_information["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()
    return mars_information

