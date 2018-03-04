import time
import random
from selenium import webdriver
import csv
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import bs4
import pandas as pd
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from pprint import pprint
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



def reset_driver():
    driver = webdriver.Firefox(executable_path = r'C:\Users\Akshay\Downloads\geckodriver-v0.19.1-win64\geckodriver.exe')
    driver.get('http://mlb.mlb.com/stats/')
    return driver

def reset_list():
    col_head[:]=[]
    col_val[:]=[]

def random_delay():
    time.sleep(random.uniform(0.5,5))

def regular_seaon(driver):
    select_reg_season = Select(driver.find_element_by_id('st_hitting_game_type'))
    select_reg_season.select_by_visible_text('Regular Season')


def answer_01():
    driver = reset_driver()
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




def answer_02():
    driver = reset_driver()
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
    regular_seaon(driver)
    random_delay()
    #Creating a pandas dataframe for AL:
    df_al_team = read_data_stats(driver)
    #Clearing the global variables col_val and col_head
    reset_list()

    #Clicking the NL widget
    nl_sel = driver.find_element_by_css_selector('#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6)')
    nl_sel.click()
    random_delay()
    regular_seaon(driver)
    random_delay()
    df_nl_team = read_data_stats(driver)
    reset_list()
    al_hr = df_al_team['HR']
    num_al = pd.to_numeric(al_hr, errors='ignore')
    mean_al = num_al.mean()
    nl_hr = df_nl_team['HR']
    num_nl = pd.to_numeric(nl_hr, errors='ignore')
    mean_nl = num_nl.mean()
    # al_team = df_al_team['Team']
    # al_hr   = pd.to_numeric(df_al_team['HR'])
    # num_al = pd.concat([al_team,al_hr])
    # mean_al = num_al['HR'].mean()
    # nl_team = df_nl_team['Team']
    # nl_hr   = pd.to_numeric(df_nl_team['HR'])
    # num_nl = pd.concat([nl_team,nl_hr])
    # mean_nl = num_nl['HR'].mean()
    # print(pd.to_numeric(df_al_team['HR']))
    # print(pd.to_numeric(df_nl_team['HR']))
    #
    # mean_al= df_al_team["HR"].mean()
    # mean_nl = df_nl_team["HR"].mean()

    print('The average HR for AL teams is: {}'.format(mean_al))
    print('The average HR for NL teams is: {}'.format(mean_nl))

    if mean_al>mean_nl:
        print('AL has a higher average than NL')
    else:
        print('NL has a higher average than AL')

    driver.back()

    select_inning = Select(driver.find_element_by_css_selector('#st_hitting_hitting_splits'))
    select_inning.select_by_visible_text('First Inning')
    regular_seaon(driver)
    time.sleep(random.normalvariate(2,0.5))
    df_al_first = read_data_stats(driver)
    reset_list()

    driver.find_element_by_css_selector('#st_hitting-0 > fieldset:nth-child(2) > label:nth-child(6)').click()
    regular_seaon(driver)
    time.sleep(random.normalvariate(2,0.5))
    df_nl_first = read_data_stats(driver)
    reset_list()
    al_hr_first = df_al_first['HR']
    num_al_first = pd.to_numeric(al_hr_first, errors='ignore')
    mean_al_first = num_al_first.mean()
    nl_hr_first = df_nl_first['HR']
    num_nl_first = pd.to_numeric(nl_hr_first, errors='ignore')
    mean_nl_first = num_nl_first.mean()
    # al_team_first = df_al_first['Team']
    # al_hr_first   = pd.to_numeric(df_al_first['HR'])
    # num_al_first = pd.concat([al_team_first,al_hr_first])
    # mean_al_first = num_al_first['HR'].mean()
    # nl_team_first = df_nl_first['Team']
    # nl_hr_first   = pd.to_numeric(df_nl_first['HR'])
    # num_nl_first = pd.concat([nl_team_first,nl_hr_first])
    # mean_nl_first = num_nl_first['HR'].mean()
    # pd.to_numeric(df_al_first['HR'])
    # pd.to_numeric(df_nl_first['HR'])
    # mean_al_first= df_al_first["HR"].mean()
    # mean_nl_first = df_nl_first["HR"].mean()

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


def answer_03():
    driver = reset_driver()
    select_year = Select(driver.find_element_by_class_name('season_select'))
    select_year.select_by_visible_text('2017')
    time.sleep(random.normalvariate(3,0.5))
    select_navbar_class = driver.find_element_by_id('top_nav')
    nav_bar = select_navbar_class.find_elements_by_tag_name('li')
    nav_bar[4].click()

    time.sleep(random.normalvariate(2,0.5))
    driver.find_element_by_css_selector('tr.odd:nth-child(12) > td:nth-child(2) > a:nth-child(1)').click()
    random_delay()

    regular_seaon(driver)
    df_player_ny_yank = read_data_stats(driver)
    bats_ov_30 = pd.to_numeric(df_player_ny_yank['AB'])>30

    df_accepted = df_player_ny_yank[bats_ov_30]
    df_accepted_sorted = df_accepted.sort_values('AVG',ascending=False)
    df_accepted_sorted.to_csv('Question_3a.csv')

    max_avg_player = df_accepted_sorted['Player'].iloc[0]
    max_avg_player_pos = df_accepted_sorted['Pos'].iloc[0]

    driver.find_element_by_link_text(max_avg_player).click()
    max_avg_full_name = driver.find_element_by_css_selector('.player-name').text
    print('The player with the highest average having bats more than 30 is {} and the position he plays is {}'.format(max_avg_full_name,max_avg_player_pos))
    random_delay()
    driver.back()
    random_delay()
    reset_list()
    positions = ['RF','CF','LF']
    df_accepted_pos = df_player_ny_yank[df_player_ny_yank['Pos'].isin(positions)]
    df_accepted_avg = pd.to_numeric(df_accepted_pos['AVG'])
    df_player_avg = pd.concat([df_accepted_pos['Player'],df_accepted_avg], axis=1)
    df_player_pos = pd.concat([df_accepted_pos['Player'],df_accepted_pos['Pos']],axis=1)
    df_player_avg_pos = pd.merge(df_player_avg,df_player_pos,on='Player')
    df_accepted_pos_sorted = df_player_avg_pos.sort_values('AVG', ascending=False)
    df_player_avg_pos.to_csv('Question_3b.csv')
    max_outfield_player = df_accepted_pos_sorted['Player'].iloc[0]
    max_outfield_player_pos = df_accepted_pos_sorted['Pos'].iloc[0]
    driver.find_element_by_link_text(max_outfield_player).click()
    max_avg_out_name = driver.find_element_by_css_selector('.player-name').text
    print('The outfield player who has the highest average is {} and plays in {} postion'.format(max_avg_out_name,max_outfield_player_pos))


def answer_04():
    reset_list()
    driver = reset_driver()
    select_year = Select(driver.find_element_by_class_name('season_select'))
    select_year.select_by_visible_text('2015')
    random_delay()
    driver.find_element_by_css_selector('#sp_hitting-1 > fieldset:nth-child(1) > label:nth-child(4)').click()
    random_delay()
    driver.find_element_by_css_selector('#sp_hitting-0 > fieldset:nth-child(5) > label:nth-child(2)').click()
    random_delay()
    regular_seaon(driver)
    select_reg_season = Select(driver.find_element_by_id('st_hitting_game_type'))
    select_reg_season.select_by_visible_text('Regular Season')
    df_al_2015 = read_data_stats(driver)
    df_ab_2015 = pd.to_numeric(df_al_2015['AB'],errors='ignore')
    df_al_ab_2015 = pd.concat([df_al_2015['Player'],df_ab_2015], axis=1)
    al_sorted = df_al_ab_2015.sort_values('AB',ascending=False)
    player = al_sorted['Player'].iloc[0]
    random_delay()
    while True:
        elem = driver.find_elements_by_link_text(player)
        random_delay()
        if not elem:
            driver.find_element_by_css_selector('.paginationWidget-previous').click()
            random_delay()
            continue
        else:
            elem[0].click()
            break
    player_name = driver.find_element_by_css_selector('.full-name').text
    player_pos = df_al_2015['Pos'].iloc[0]
    player_team = driver.find_element_by_css_selector('div.dropdown:nth-child(3) > span:nth-child(1)').text
    print('The player with the most number of bats in the AL plays is {} who plays in {} position for {}'.format(player_name,player_pos,player_team))
    df_al_2015.to_csv('Question_4.csv')

def answer_05():
    reset_list()
    driver = reset_driver()

    select_year = Select(driver.find_element_by_class_name('season_select'))
    select_year.select_by_visible_text('2014')
    random_delay()

    select_game_type = Select(driver.find_element_by_id('sp_hitting_game_type'))
    select_game_type.select_by_visible_text('All-Star Game')
    random_delay()

    with open('latin_america.csv') as f:
        reader= csv.reader(f)
        latin = list(reader)
        latin_countries = [l for country in latin for l in country]

    df_all_star = read_data_stats(driver)
    list_all_star_name = df_all_star['Player'].tolist()
    latin_player = {}
    for name in list_all_star_name:
        player_name_find = driver.find_elements_by_link_text(name)
        if not player_name_find:
            driver.back()
            random_delay()
            continue
        else:
            player_name_find[0].click()
            random_delay()
            label_table = driver.find_elements_by_css_selector('div.player-bio:nth-child(2) > ul:nth-child(2)')
            for label in label_table:
                if any(country in label.text for country in latin_countries):
                    latin_player[driver.find_element_by_css_selector('.full-name').text]= driver.find_element_by_css_selector('div.dropdown:nth-child(3) > span:nth-child(1)').text
                    driver.back()
                else:
                    driver.back()
                    continue

    df_latin_player_team = pd.DataFrame(list(latin_player.items()),columns=['Player Name','Team'])
    print('Players born in latin america with their corresponding team name:')
    print(df_latin_player_team)
    df_latin_player_team.to_csv('Quesstion_5.csv')

def answer_06():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '6b8d9a0f4038484897bfb02929b65e4f',
    }

    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/mlb/stats/JSON/Games/2016?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    try:
        conn1 = http.client.HTTPSConnection('api.fantasydata.net')
        conn1.request("GET", "/v3/mlb/stats/JSON/Stadiums?%s" % params, "{body}", headers)
        response = conn1.getresponse()
        data1 = response.read()
        conn1.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    try:
        conn2 = http.client.HTTPSConnection('api.fantasydata.net')
        conn2.request("GET", "/v3/mlb/stats/JSON/AllTeams?%s" % params, "{body}", headers)
        response = conn2.getresponse()
        data2 = response.read()
        conn2.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    data_json_games = json.loads(data)
    data_stadiums = json.loads(data1)
    data_teams = json.loads(data2)

    opponnent = []
    game_dates = []
    stadiumID = []
    stadiumName = []
    game_city = []
    game_state = []
    opp_name = []

    for game in data_json_games:
        if game['HomeTeam']=="HOU":
            opponnent.append(game["AwayTeam"])
            game_dates.append(game["DateTime"])
            stadiumID.append(game["StadiumID"])
        elif game['AwayTeam']=="HOU":
            opponnent.append(game["HomeTeam"])
            game_dates.append(game["DateTime"])
            stadiumID.append(game["StadiumID"])
    for ID in stadiumID:
        for stadium in data_stadiums:
            if ID == stadium['StadiumID']:
                stadiumName.append(stadium['Name'])
                game_city.append(stadium['State'])
                game_state.append(stadium["City"])
    for opp in opponnent:
        for team in data_teams:
            if opp==team["Key"]:
                opp_name.append(team['Name'])

    dic_hou = {'Opponents': opp_name,'Date':game_dates,'Stadium Name': stadiumName, 'City': game_city,'State':game_state}
    df_games = pd.DataFrame(dic_hou)
    print(df_games)
    with open('Games_info.json', 'w') as fp:
        json.dump(data_json_games, fp)
    with open('Stadium_info.json', 'w') as fp:
        json.dump(data_stadiums, fp)
    with open('Teams_info.json', 'w') as fp:
        json.dump(data_teams, fp)
answer_06()