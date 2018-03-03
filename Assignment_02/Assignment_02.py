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
    for tr in soup.tbody.findAll('tr'):
        row = [td.text.replace(u'\xa0',u'') for td in tr.findAll('td')]
        col_val.append(row)
    for th in soup.thead.tr.findAll('th'):
        if len(col_head)<len(col_val[0]):
            col_head.append(th.text.replace('▲','').replace('▼',''))
        else:
            break
    time.sleep(random.normalvariate(3,0.5))
    next_b(driver)
    df = pd.DataFrame(col_val, columns=col_head)
    return df
def next_b(driver):
    id_of_pagination_div = driver.find_element_by_class_name('paginationWidget-next')
    try:
        if 'display: none;' in id_of_pagination_div.get_attribute("style"):
            return
        else:
            id_of_pagination_div.click()
            time.sleep(random.normalvariate(3,0.5))
            read_data_stats(driver)
    except:
        pass
def reset_all():
    driver.get('http://mlb.mlb.com/stats/')
    col_head[:]=[]
    col_val[:]=[]
def reset_list():
    col_head[:]=[]
    col_val[:]=[]
driver = webdriver.Firefox(executable_path = r'C:\Users\Akshay\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
driver.get('http://mlb.mlb.com/stats/')

def answer_01():
    select_year = Select(driver.find_element_by_class_name('season_select'))
    select_year.select_by_visible_text('2015')
    time.sleep(random.normalvariate(3,0.5))
    select_navbar_class = driver.find_element_by_id('top_nav')
    nav_bar = select_navbar_class.find_elements_by_tag_name('li')
    nav_bar[4].click()

    time.sleep(random.normalvariate(3, 0.5))
    df_team_2015 = read_data_stats(driver)
    df_team_2015.to_csv('Question_1.csv')

    team_HR = df_team_2015.sort_values('HR',ascending=False)
    max_HR_team = team_HR['Team'].iloc[0]
    print(max_HR_team)

    reset_all()

def answer_02():
    select_year = Select(driver.find_element_by_class_name('season_select'))
    select_year.select_by_visible_text('2015')
    time.sleep(random.normalvariate(3,0.5))

    #Clicking the Team button:
    select_navbar_class = driver.find_element_by_id('top_nav')
    nav_bar = select_navbar_class.find_elements_by_tag_name('li')
    nav_bar[4].click()
    time.sleep(random.normalvariate(2,0.5))

    #Clicking the AL widget
    al_sel = driver.find_element_by_css_selector('#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(4)')
    al_sel.click()
    time.sleep(random.normalvariate(2,0.5))

    #Creating a pandas dataframe for AL:
    df_al_team = read_data_stats(driver)
    #Clearing the global variables col_val and col_head
    reset_list()

    #Clicking the NL widget
    nl_sel = driver.find_element_by_css_selector('#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6)')
    nl_sel.click()
    time.sleep(random.normalvariate(2,0.5))
    df_nl_team = read_data_stats(driver)
    reset_list()

    pd.to_numeric(df_al_team['HR'])
    pd.to_numeric(df_nl_team['HR'])

    mean_al= df_al_team["HR"].mean()
    mean_nl = df_nl_team["HR"].mean()

    print('The average HR for AL teams is: {}'.format(mean_al))
    print('The average HR for NL teams is: {}'.format(mean_nl))

    if mean_al>mean_nl:
        print('AL has a higher average than NL')
    else:
        print('NL has a higher average than AL')

    driver.back()

    select_inning = Select(driver.find_element_by_css_selector('#st_hitting_hitting_splits'))
    select_inning.select_by_visible_text('First Inning')

    time.sleep(random.normalvariate(2,0.5))
    df_al_first = read_data_stats(driver)
    reset_list()

    driver.find_element_by_css_selector('#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6)').click()
    time.sleep(random.normalvariate(2,0.5))
    df_nl_first = read_data_stats(driver)
    reset_list()

    pd.to_numeric(df_al_first['HR'])
    pd.to_numeric(df_nl_first['HR'])
    mean_al_first= df_al_first["HR"].mean()
    mean_nl_first = df_nl_first["HR"].mean()

    print('The average HR for AL teams is: {}'.format(mean_al_first))
    print('The average HR for NL teams is: {}'.format(mean_nl_first))

    if mean_al_first>mean_nl_first:
        print('AL has a higher average than NL')
    else:
        print('NL has a higher average than AL')

    df_a = pd.concat([df_al_team,df_nl_team])
    df_b = pd.concat([df_al_first,df_nl_first])

    df_a.to_csv('Question_2a.csv')
    df_b.to_csv('Question_2b.csv')
answer_02()