import csv
import re
import time
from collections import ChainMap
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import os
import multiprocessing as mp
from datetime import datetime, timedelta
import socket


def is_internet_on():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def scrape_product(args):
    (
        item_main,
        account,
        login_inputs,
        login_button,
        cookie_button,
        Table_click,
        Table_input,
        Table_first_element,
    ) = args
    email, password = account
    # if(item[2]==''):
    #     hscode = ''
    # else:
    hscode = item_main[1]
    item = item_main[2]
    if(item == "Lion's Mane Mushroom"):
        item = 'Lion'
    print(hscode, item)
    print(email, password)
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1280,720")
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver", options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.tridge.c" "om/login")

    dummy = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@placeholder='name@company.com']")
        )
    )
    if len(dummy) > 0:
        dummy[0].send_keys(email)
        print("passed")

    else:
        print("Couldn't find input email or password. Try changing Input XPATH")
    dummy = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@placeholder='Enter password']")
        )
    )
    if len(dummy) > 0:
        dummy[0].send_keys(password)

        print("passed")

    else:
        print("Couldn't find input email or password. Try changing Input XPATH")

    # time.sleep(2000)
    dummy = driver.find_elements(By.XPATH, "//*[@class='" + login_button + "']")
    time.sleep(5)
    dummy = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[type='submit']"))
    )
    if len(dummy) > 0:
        dummy[0].click()
        print("Login successfull")
        time.sleep(5)
        try:
            dummy[0].click()
        except Exception as e:
            print("Couldn't find Login Button. Try changing Login Button XPATH")

    else:
        print("Couldn't find Login Button. Try changing Login Button XPATH")
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    try:
        cookie = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@class='" + cookie_button + "']")
            )
        )
        if len(cookie) > 0:
            cookie[-1].click()
        else:
            print(
                "Couldn't find Cookie Button (Might cause error later on). Try changing Cookie XPATH"
            )
    except Exception as e:
        print(
            "Couldn't find Cookie Button (Might cause error later on). Try changing Cookie XPATH"
        )
        pass

    driver.get("https://www.tridge.com/prices")
    wait.until(EC.url_contains("https://www.tridge.com/prices"))
    df = []
    wait = WebDriverWait(driver, 10)

    try:
        # butt=wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='"+Table_click+"']")))

        butt = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[@id='root']/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div/div/button",
                )
            )
        )
        print("Product clicked")
    except Exception as e:
        print(e)
        print("Couldn't find Product Search Dropdown. Try changing XPATH")
        return
    print(butt[0].text)
    try:
        if len(butt) > 0:
            butt[0].click()
        else:
            print("Couldn't find Product Search Dropdown. Try changing XPATH")
            return
    except Exception as e:
        print(e)
        return
    # time.sleep(2000)
    # /html/body/div[5]/div/div/div/div/div/div[1]/div/div/div/input
    try:
        dummy = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//input[@placeholder='Search']")
            )
        )

        # dummy=wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="TextField-11"]')))
    except Exception as e:
        print("Couldn't find Product Search Input. Try changing XPATH")
        return

    try:
        if len(dummy) > 0:
            dummy[0].send_keys(item)
        else:
            print("Couldn't find Product Search Input. Try changing XPATH")
            return
    except Exception as e:
        print("Click ni hua")
        return

    wait = WebDriverWait(driver, 10)
    # time.sleep(2000)
    try:
        prodIndex = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="menu-item"]'))
        )
    except:
        # print(e)
        print("Couldn't find Searched Product. Try changing XPATH")
        time.sleep(2000)
        return
    if len(prodIndex) > 0:
        prodIndex[0].click()
    else:
        print("Couldn't find Searched Product. Try changing XPATH")
        time.sleep(2000)

    # for Historiicasl data
    # query_string = "&item_Type=w&interval=w&startDate=2020-01-28&endDate=2023-04-28&currency=USD&unit=kg&includeEstimatedPrices=true&includeForecastedPrices=false&"
    query_string = "&item_Type=w&interval=w&startDate=2023-02-08&endDate=2023-05-08&currency=USD&unit=kg&includeEstimatedPrices=true&includeForecastedPrices=false&"
    # for live data
    # query_string = "&item_Type=w&interval=w&dateRange=1m&startDate=2023-02-27&endDate=2023-04-24&currency=USD&unit=kg&includeEstimatedPrices=true&includeForecastedPrices=false&"
    driver.get(str(driver.current_url) + query_string)
    print(driver.current_url)
    print(item)
    # time.sleep(30)
    # return
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    actions.send_keys(Keys.PAGE_DOWN).perform()
    iterate = 0
    # try:c
    count = 0
    pageCheck = True
    while True:
        # sc-lllmON jnyQLi
        try:
            notLoaded = False
            try:
                # table = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='simplebar-content']")))
                table = wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
                )
            except Exception as e:
                print(
                    "Couldn't Find table in element, Please check your internet connection"
                )
                return
            try:
                if len(table) > 0:
                    table[0].click()
                else:
                    print("Table is not a list")
            except Exception as e:
                print('table scroll disable : ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            actions.send_keys(Keys.PAGE_DOWN).perform()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            # time.sleep(1.5)
            headings = table[0].find_elements(By.TAG_NAME, "th")
            try:
                rows = table[0].find_elements(By.TAG_NAME, "tr")
            except NoSuchElementException:
                print("Unexpected error please debug")
                continue
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 6:
                    if len(cells[2].text) <= 0:
                        notLoaded = True
            if notLoaded == True:
                continue
            else:
                pass
            print(len(rows))
            print("Sr\tCountry\tRegion\tVariety\tPrice")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 6:
                    print(count, "\t")
                    count += 1
                    print(
                        hscode,
                        "\t",
                        item,
                        "\t",
                        cells[2].text,
                        "\t",
                        cells[3].text,
                        "\t",
                        cells[4].text,
                        "\t",
                        cells[6].text,
                    )
                    for i in range(6, len(headings)):
                        data = {
                            "CountryName": cells[2].text,
                            "CityName": cells[3].text,
                            "ProductName": item_main[1],
                            "variety": cells[4].text,
                            "Currency/Unit": cells[5].text,
                            "Hscode": hscode,
                        }
                        data["Price Date"] = headings[i].text
                        data["Price"] = cells[i].text
                        df.append(data)
            # if (count>241):
            #     break
            # "sc-lllmON hJKCSX"
            # classname = input("waiting for input")
            # time.sleep(2000)

            end = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[5]/div[2]/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/span",
                    )
                )
            )[-1].text
            end = int(re.findall("\d+", end)[0])
            print("Page entrises : ", end)
            if end < 20:
                break
            # randon_var = input("waiting for input")
            # if (count<end*5):
            #     break
            actions.send_keys(Keys.PAGE_DOWN).perform()
            # time.sleep(1)

            next = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "//button[contains(@class,'soso-icon-button-default-secondary soso-icon-button-s')]",
                    )
                )
            )
            if len(next) > 0:
                if pageCheck == True:
                    next[1].click()
                    pageCheck = False
                else:
                    if len(next) > 1:
                        next[1].click()
                    else:
                        print(item, "Scraping ended")
                        break
            else:
                print("Next Button Not found, Try changing XPATH")
                break
            # time.sleep(1)
            iterate += 1
        except Exception as e:
            print(e)
            print("error in procuct :", item)
            # if isinstance(e, (TimeoutException, StaleElementReferenceException)):
            #     print("Hi, Internet Connection")
            #     start_time = time.time()
            #     time_elapsed = 0
            #     internet_check_interval = 10  # Check for internet every 10 seconds
            #
            #     while time_elapsed < 300:  # 300 seconds = 5 minutes
            #         if is_internet_on():
            #             break
            #
            #         time.sleep(internet_check_interval)
            #         time_elapsed = time.time() - start_time
            # else:

            # while()
            print("Scarping Finished")
            break
    dataOut = pd.DataFrame(df)
    print(dataOut.head())
    # need to edit
    try:
        out_path = 'missing_products_scrapped_files\\'+item_main[2]+'.xlsx'
        dataOut.to_excel(out_path)
    except Exception as e:
        print("E :", e)
        time.sleep(2000)

def main():
    # accounts = [("johndelle554@gmail.com", "123asd123"), ("tayyab@tazahtech.com", "123123123123"), ("talk2saadalam@gmail.com", "123")]
    #             ]
    accounts = [
        ("hohibif942@in2reach.com", "112233"),
        ("rihayay626@pixiil.com", "112233"),
        ("shahzadiqbal0774570@gmail.com", "112233"),

    ]
    # accounts = [("raoali1525@gmail.com", "Raoali1525")]
    # accounts = [("alishahid161@hotmail.com", "123123123123")]
    login_inputs = "sc-gDiTby hdbRSC Polaris-TextField__Input"
    login_button = "sc-pyfCe bZwhCP filled primary m symbol-before "
    Table_click = "sc-cVLQNM iukbRx sc-dMUtCB bBEccC sc-fSDvIO idjeXE"
    # sc-dpJOxQ eKbxVu sc-DRkuH cQpbiD sc-cRcKHx dxsiWA
    Table_input = "sc-gDiTby hdbRSC Polaris-TextField__Input"
    Table_first_element = "sc-hixjlP glKRrx"
    cookie_button = "sc-dmqHEX ioIdjU interaction-statelayer"

    my_list = []
    with open(
        "filter_missing_products.csv", mode="r"
    ) as file:
        reader = csv.reader(file)
        for row in reader:
            my_list.append(row)
    # input_tuples = [(item, accounts, login_inputs, login_button, cookie_button, Table_click, Table_input, Table_first_element) for item in my_list[0]]
    # Set up a process pool with the number of processes equal to the number of available CPU cores

    my_list.pop(0)
    current_time = datetime.now()

    def should_process_file(item):
        file_name = 'missing_products_scrapped_files\\'+item[2]+'.xlsx'
        print("file_mname = ", file_name)
        if os.path.exists(file_name):
            # last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_name))
            # if (current_time - last_modified_time) < timedelta(hours=48):
            return False
        return True

    # input_tuples = [
    #     (item, account, login_inputs, login_button, cookie_button, Table_click, Table_input, Table_first_element)
    #     for item in my_list for account in accounts if should_process_file(item)]
    input_tuples = []
    ajeeb_item = []
    for item in my_list:
        for account in accounts:
            if should_process_file(item):
                if item not in ajeeb_item:
                    input_tuple = (
                        item,
                        account,
                        login_inputs,
                        login_button,
                        cookie_button,
                        Table_click,
                        Table_input,
                        Table_first_element,
                    )
                    input_tuples.append(input_tuple)
                    ajeeb_item.append(item)

    # print(input_tuples)
    # for input_tuple in input_tuples:
    #     for item in input_tuple:
    #         print(item)
    #     print('

    # To use max cpu available mp.Pool(1) - > mo.Pool(mp.cpu_count())
    with mp.Pool(3) as pool:
        # Use the pool.map() function to run the scrape_product function for each product in parallel
        pool.map(scrape_product, input_tuples)

    # Any post-processing or saving of the data here


if __name__ == "__main__":
    main()

#     print(input_tuples)
#     # for input_tuple in input_tuples:
#     #     for item in input_tuple:
#     #         print(item)
#     #     print('
#
#     # To use max cpu available mp.Pool(1) - > mo.Pool(mp.cpu_count())
#     with mp.Pool(3) as pool:
#         # Use the pool.map() function to run the scrape_product function for each product in parallel
#         pool.map(scrape_product, input_tuples)
#
#     # Any post-processing or saving of the data here
#
#
# if __name__ == "__main__":
#     main()
