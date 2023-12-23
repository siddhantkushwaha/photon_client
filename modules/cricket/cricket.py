import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    match_url = ""

    driver.get(match_url)

    my_team = 'td.liveresults-sports-immersive__lr-imso-ss-wp-ft'
    opp_team = 'td.liveresults-sports-immersive__lr-imso-ss-wp-st'

    while True:
        try:
            driver.get(match_url)
            time.sleep(10)

            my_team_score = int(float(driver.find_element(By.CSS_SELECTOR, my_team).text[:-1]))
            opp_team_score = int(float(driver.find_element(By.CSS_SELECTOR, opp_team).text[:-1]))

            print(my_team_score, opp_team_score)

            time.sleep(50)
        except Exception as e:
            print(e)

            time.sleep(60)


if __name__ == '__main__':
    main()
