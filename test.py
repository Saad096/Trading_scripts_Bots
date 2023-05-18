from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.tridge.com/sellers/browse"
driver_path = "chromedriver"
driver = webdriver.Chrome(driver_path)
driver.maximize_window()
options = Options()

options.add_argument('--disable-notifications')
options.add_argument('start-maximized')
webdriver.Chrome(service=Service(driver_path), chrome_options=options)


driver.get(url)
driver.implicitly_wait(5)

time.sleep(1)
# driver.execute_script("window.scrollBy(0, 700)", "")
# driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
Cooki_but = driver.find_element(By.XPATH, "//*[@id='fixedBottomBar']/div/div/div/div/div/div/div[2]/div/div/div[1]/button/div[1]")
Cooki_but.click()
# while True:
#     time.sleep(1)
#     actions = ActionChains(driver)
#     actions.send_keys(Keys.PAGE_DOWN).perform()
#     actions.send_keys(Keys.PAGE_DOWN).perform()
print("Premmium both")

actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN).perform()

Premmium_both = driver.find_elements(By.XPATH, "div[@class='sc-eDWCr eonJnV sc-ikjiJv gkQDgr']")




i = 1

# Element = driver.find_element(By.XPATH, '//*[@id="mp-other-content"]/ul/li[5]')
# driver.execute_script("arguments[0].scrollIntoView();", Element)
time.sleep(3000)
driver.quit()






