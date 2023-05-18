import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from datetime import datetime, timedelta
import socket


def add_varieties(product_name, varieties_string, df):
    varieties_list = varieties_string.strip().split("\n")
    varieties_list.pop(0)
    for variety in varieties_list:
        new_row = pd.DataFrame({"Product name": [product_name], "Varieties": [variety]})
        df = pd.concat([df, new_row], ignore_index=True)

    return df

    return df


def is_internet_on():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def scrape_product(args):
    (
        item,
        account,
        login_inputs,
        login_button,
        cookie_button,
        Table_click,
        Table_input,
        Table_first_element,
    ) = args
    email, password = account
    hscode = item[2].split(" ")[0]
    item = item[1]
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
            cookie[0].click()
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
    products_df = pd.DataFrame(columns=["Product name", "Varieties"])
    wait = WebDriverWait(driver, 10)

    try:
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
    try:
        dummy = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//input[@placeholder='Search']")
            )
        )

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
    try:
        prodIndex = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="menu-item"]'))
        )
    except:
        print("Couldn't find Searched Product. Try changing XPATH")
        time.sleep(2000)
        return
    if len(prodIndex) > 0:
        prodIndex[0].click()
        time.sleep(5)
        v_click = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    '//button[contains(@class, "soso-selector-button") and contains(@class, "soso-selector-button") and contains(@class, "text-align-start")]',
                )
            )
        )

        v_click[3].click()
        time.sleep(2)
        # Create an ActionChains instance
        actions = ActionChains(driver)
        for i in range(2500):
            # Perform Shift + Down Arrow key combination
            actions.key_down(Keys.SHIFT).send_keys(Keys.ARROW_DOWN).key_up(
                Keys.SHIFT
            ).perform()

        time.sleep(1)

        varriety = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "simplebar-content"))
        )[-1]
        print(varriety.text)
        products_df = add_varieties(item, varriety.text, products_df)
        products_df.to_csv("novaritese\\" + item + "_varieties.csv")
        return
    else:
        print("Couldn't find Searched Product. Try changing XPATH")
        time.sleep(2000)


def main():
    accounts = [("talk2saadalam@gmail.com", "123")]
    login_inputs = "sc-gDiTby hdbRSC Polaris-TextField__Input"
    login_button = "sc-pyfCe bZwhCP filled primary m symbol-before "
    Table_click = "sc-cVLQNM iukbRx sc-dMUtCB bBEccC sc-fSDvIO idjeXE"
    Table_input = "sc-gDiTby hdbRSC Polaris-TextField__Input"
    Table_first_element = "sc-hixjlP glKRrx"
    cookie_button = "sc-pyfCe ikqHDV filled primary m symbol-before "

    my_list = []
    with open("fruit.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            my_list.append(row)
    my_list.pop(0)

    def should_process_file(item):
        file_name = "varities\\" + item[1] + "_varieties.csv"
        print("file_mname = ", file_name)
        if os.path.exists(file_name):
            return False
        return True

    my_list = [
        "Kaong",
        "Caja",
        "Olallieberry",
        "Kaffir Lime",
        "Cashew Apple",
        "Doum Palm Fruit",
        "Double Coconut",
        "Maqui Berry",
        "Mexican Hawthorn",
        "Baobab Fruit",
        "Ambarella",
        "Peach Palm",
        "Giant Granadilla",
        "Nipa Palm",
        "Chinese Bayberry",
        "Snowberry",
        "Indochina Dragonplum",
        "Jagua",
        "Calamansi",
        "Guarana",
        "Satkara",
        "Tayberry",
        "Marang",
        "Nance",
        "Borojo",
        "Canistel",
        "Bacuri",
        "Pulasan",
        "Huckleberry",
        "Pitanga",
        "Jabuticaba",
        "Palmyra",
        "Desiccated Coconut",
    ]
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
    for input_tuple in input_tuples:
        scrape_product(input_tuple)

    # Any post-processing or saving of the data here


if __name__ == "__main__":
    main()
