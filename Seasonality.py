from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from collections import ChainMap
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import json
import re
import openpyxl


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def scrape_products(login_inputs, login_button, cookie_button, single_table_line, harvest_line, element):
    df = []
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    mahinay = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "August", "September", "Oct", "Nov", "Dec"]

    driver = webdriver.Chrome('chromedriver', desired_capabilities=caps)

    driver.get("https://www.tridge.com/login?next=%252Fsellers/browse")
    # time.sleep(2000)
    # time.sleep(4000)
    wait = WebDriverWait(driver, 10)
    dummy = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='name@company.com']")))
    if (len(dummy) > 0):
        dummy[0].send_keys("bazilsb7@gmail.com")
    else:
        print("Couldn't find input")

    dummy = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='Enter password']")))
    dummy[0].send_keys("Bazil123")
    time.sleep(3)

    dummy = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[type='submit']")))
    if (len(dummy) > 0):
        dummy[0].click()
    else:
        print("Not Found")

    time.sleep(6)
    driver.get("https://www.tridge.com/seasons/browse?")
    time.sleep(1)
    cookie = driver.find_elements(By.XPATH, "//*[@class='" + cookie_button + "']")
    if (len(cookie) > 0):
        cookie[0].click()
    else:
        print("Nahi mila")
    time.sleep(3)

    i = 0

    while (i < 600):
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        i += 1

    lines = driver.find_elements(By.XPATH, "//*[@class='" + single_table_line + "']")
    harvest = driver.find_elements(By.XPATH, "//*[@class='" + harvest_line + "']")
    if (len(harvest) <= 0):
        print("Harvesting line not found.")
        harvest_line = input("Enter updated XPATH: ")
        harvest = driver.find_elements(By.XPATH, "//*[@class='" + harvest_line + "']")

    time.sleep(5)
    i = 1
    for line in lines:
        # line.click()
        print(len(harvest))
        data = line.get_attribute('outerHTML')
        soup = BeautifulSoup(data, 'html.parser')
        # sc-oZIhv PSCLB sc-hiDMwi sc-eJNOVp brQzCE bNxFIk data-table-cell
        data_divs = soup.find_all('div', attrs={'class': re.compile(r'\bsc-oQLfA\b')})
        name = data_divs[0].text.strip()
        country = data_divs[1].text.strip()
        variety = data_divs[2].text.strip()
        region = data_divs[3].text.strip()

        months = harvest[i].get_attribute('outerHTML')
        i += 1
        # print(months)

        soup = BeautifulSoup(months, 'html.parser')

        divs = soup.find_all('div', class_='sc-cVLQNM foqXGg')
        avail_months = []
        for ite, div in enumerate(divs):
            if div.find('div', {'color': 'seasonIn'}):
                # print(f"Found at index {mahinay[ite]}")
                avail_months.append(mahinay[ite])

        lis = {"CropName": name, 'Country': country, 'CropProcess': 'Harvesting', "variety": variety, "region": region,
               'HarvestMonths': avail_months}
        df.append(lis)
        print(lis)

    # print(df)
    dataOut = pd.DataFrame(df)

    print("Yahan end ho gya")
    print(dataOut.head())
    dataOut.to_excel("Seasonailty.xlsx", index=False)
    time.sleep(4000)
    driver.quit()


def main():
    login_inputs = "sc-gDiTby hdbRSC Polaris-TextField__Input"
    login_button = "sc-pyfCe bZwhCP filled primary m symbol-before "

    single_table_line = "sc-irTswW dcarTY sc-fYdXmn iVypFZ data-table-row sc-UxxwN gAnoEt"
    harvest_line = ""
    cookie_button = "sc-qRumB RlRVV soso-button soso-button-default-primary soso-button-m soso-button-symbol-before "
    element = "sc-oQLfA"
    scrape_products(login_inputs, login_button, cookie_button, single_table_line, harvest_line, element)


# if name == "main":
main()