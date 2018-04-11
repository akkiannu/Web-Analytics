import time
import random
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

rev=[]
rat=[]
dat=[]
tit=[]
com=[]
aut=[]
def scrape(driver):
    reviews = driver.find_elements_by_css_selector('.a-size-base.review-text')
    ratings = driver.find_elements_by_xpath(".//a[contains(@title,  'out of 5 stars')]")
    dates = driver.find_elements_by_css_selector(".a-size-base.a-color-secondary.review-date")
    titles = driver.find_elements_by_css_selector(".a-size-base.a-link-normal.review-title.a-color-base.a-text-bold")
    comments = driver.find_elements_by_xpath("//*[contains(text(), 'Was this review helpful to you?')]")
    authors = driver.find_elements_by_css_selector('.a-size-base.a-color-secondary.review-byline > a')

    author=[author.text for author in authors]
    aut.extend(author)
    review=[review.text for review in reviews]
    rev.extend(review)
    rating=[rating.get_attribute('title') for rating in ratings]
    rat.extend(rating)
    date=[date.text.strip('on ').replace(',','') for date in dates]
    del date[:2]
    dat.extend(date)
    title = [title.text for title in titles]
    tit.extend(title)
    comment = [comment.text.strip('Was this review helpful to you?') for comment in comments]
    com.extend(comment)
    time.sleep(random.normalvariate(4,0.5))
    next_b(driver)
    combined_data=list(zip(dat,aut,tit,rev,rat,com))
    return pd.DataFrame(data=combined_data,columns=['Date','Author','Title','Review','Rating','Comment(s)'])

def next_b(driver):
    id_of_nextb = driver.find_element_by_class_name('a-last')
    try:
        if 'a-disabled a-last' in id_of_nextb.get_attribute('class'):
            return
        else:
            id_of_nextb.click()
            time.sleep(random.normalvariate(3,0.5))
            scrape(driver)
    except:
        pass

driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')
time.sleep(random.normalvariate(4,0.5))
most_rec = Select(driver.find_element_by_css_selector('#sort-order-dropdown'))
most_rec.select_by_visible_text('Most recent')
time.sleep(random.normalvariate(4,0.5))
ver_pur = Select(driver.find_element_by_css_selector('#reviewer-type-dropdown'))
ver_pur.select_by_visible_text('Verified purchase only')
time.sleep(random.normalvariate(4,0.5))
rev_head = scrape(driver)
print(rev_head.head(15))
rev_head.to_json('reviews.json',orient='columns')
