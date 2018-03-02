import time
import random
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import bs4
import pandas as pd
col_head = []
col_val = []
def read_data_stats(driver):
    wait = WebDriverWait(driver, 10)
    data_div = wait.until(EC.visibility_of_element_located((By.ID,'datagrid')))
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html,'html5lib')
    for th in soup.thead.tr.findAll('th'):
        if len(col_head)<=33:
            col_head.append(th.text.replace('▲','').replace('▼',''))
        else:
            break
    for tr in soup.tbody.findAll('tr'):
        row = [td.text.replace(u'\xa0',u'') for td in tr.findAll('td')]
        col_val.append(row)
    time.sleep(random.normalvariate(3,0.5))
    next_b(driver)
    return col_head,col_val
def next_b(driver):
    id_of_pagination_div = driver.find_element_by_class_name('paginationWidget-next')
    if 'display: none;' in id_of_pagination_div.get_attribute("style"):
        return
    else:
        id_of_pagination_div.click()
        time.sleep(random.normalvariate(3,0.5))
        read_data_stats(driver)

driver = webdriver.Firefox(executable_path = r'C:\Users\Akshay\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
driver.get('http://mlb.mlb.com/stats/')
select_year = Select(driver.find_element_by_class_name('season_select'))
select_year.select_by_visible_text('2015')
col_head_2015,col_val_2015 = read_data_stats(driver)
df = pd.DataFrame(col_val_2015,columns=col_head_2015)
df.to_csv('2015-hitting.csv')

# time.sleep(7)
# # select_year.select_by_visible_text('2015')
# select_year.select_by_visible_text('2015')
# col_head_2017,col_val_2017 = read_data_stats(driver)
# df = pd.DataFrame(col_val_2017, columns=col_head_2017)
# df = pd.DataFrame(columns=col_head_2017)

