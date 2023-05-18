# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time


import csv
from datetime import date
import scrapy
from scrapy.crawler import CrawlerProcess
fields = [
    "Country Name",
   ]
file = open("fruites_names_data.csv", "w", newline="", encoding="UTF8")
writer = csv.DictWriter(file, fieldnames=fields)
writer.writeheader()
file.flush()
file.close()

file = open("walmart_data.csv", "a", newline="", encoding="UTF8")
writer = csv.DictWriter(file, fieldnames=fields)

class fruites(scrapy.Spider):
    name = "fruite"
    allowed_domains = ["tridge.com/"]
    start_url= "https: // www.tridge.com / browse / category?code = fruits"
    def start_requests(self):
        yield scrapy.Request(url=self.start_url)
    def parse(self, response):
        print(response)


        name = response.css("div.sc-iOdfRm.dpuIb::text").get()
        print(name)

Process = CrawlerProcess()
Process.crawl(fruites)
Process.start()



