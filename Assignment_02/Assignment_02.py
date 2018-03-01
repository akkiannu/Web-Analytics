import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import bs4
import pandas as pd

def read_data_stats(driver):
    data_div = driver.find_element_by_id('datagrid')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html,'html5lib')
    col_head = []
    col_val = []
    for th in soup.thead.tr.findAll('th'):
        col_head.append(th.text.replace('▲','').replace('▼',''))
    for tr in soup.tbody.findAll('tr'):
        row = [td.text.replace(u'\xa0',u'') for td in tr.findAll('td')]
        col_val.append(row)

    return col_head,col_val

driver = webdriver.Firefox(executable_path = r'C:\Users\Akshay\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
driver.get('http://www.mlb.com')
stats_header = driver.find_element_by_class_name('megamenu-navbar-overflow__menu-item-link--stats')
stats_header.click()
time.sleep(1)
stats_line = stats_header.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/nav[2]/ul/li[5]/div/div[2]/div/ul/li[1]/a')
stats_line.click()
time.sleep(2)
col_head_2017,col_val_2017 = read_data_stats(driver)
#df = pd.DataFrame(col_val_2017, columns=col_head_2017)
# df = pd.DataFrame(columns=col_head_2017)

