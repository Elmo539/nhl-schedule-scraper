import pprint
from pymongo import MongoClient
from time import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = MongoClient('localhost', 27017)
schedule_db = client['schedule']
record = schedule_db['record']

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
path = Service("/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(service=path, options=options)
driver.get("https://www.espn.com/nhl/team/_/name/bos/boston-bruins")
wait = WebDriverWait(driver, 5)

def pastGames():
    schedule_page = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div[2]/nav/ul/li[4]/a')))
    schedule_page.click()

    global rows
    rows = driver.find_elements(By.CLASS_NAME, "Table__TR.Table__TR--sm.Table__even")

    global row
    for row in range(len(rows)):
        if "TIME" in rows[row].text:
            break
        else:
            pass

    for i in range(row - 5, row):
        raw_str = repr(rows[i].text)
        new_str1 = raw_str.replace(r"\n", "_")
        new_str2 = new_str1.replace("'", "")
        list_str = new_str2.split('_')
        result_record_goalie = list_str[3]
        result_split = result_record_goalie.split(' ')

        game_dict = {
                'game #': "",
                'date': "",
                'opponent': "",
                'result': "",
                'record': "",
                'goalie': "",
                }

        game_dict['game #'] = str(i)
        game_dict['date'] = list_str[0]
        game_dict['opponent'] = list_str[2]
        game_dict['result'] = result_split[0]
        game_dict['record'] = result_split[1]
        game_dict['goalie'] = result_split[2]
        pprint.pprint(game_dict, width=30, sort_dicts=False)
        print()


def futureGames():
    global rows
    global row
    for i in range(row + 1, row + 6):
        raw_str = repr(rows[i].text)
        new_str1 = raw_str.replace(r"\n", "_")
        new_str2 = new_str1.replace("'", "")
        list_str = new_str2.split('_')

        game_dict = {
                'game #': "",
                'date': "",
                'opponent': "",
                'time': "",
                }

        game_dict['game #'] = str(i)
        game_dict['date'] = list_str[0]
        game_dict['opponent'] = list_str[1] + ' ' + list_str[2]
        game_dict['time'] = list_str[3]
        pprint.pprint(game_dict, width=30, sort_dicts=False)
        print()


def main():
    print()
    print("-------- PAST GAMES --------")
    pastGames()
    print()
    print("-------- FUTURE GAMES --------")
    futureGames()
    driver.close()


if __name__ == '__main__':
    start_time = float(time())
    main()
    end_time = float(time())
    print()
    print('completed in:', (end_time - start_time))

