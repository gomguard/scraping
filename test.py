from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
import os
import time
import csv
import subprocess
import datetime



driver_path = 'C:/Users/kx682tw/Downloads/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

## proxy option
# US Proxy : https://www.proxynova.com/proxy-server-list/country-us/
# PROXY = "68.251.250.193:8080"
# options.add_argument('--proxy-server=%s' % PROXY)

## open browser
browser = webdriver.Chrome(driver_path, chrome_options = options)

url = 'https://eraspace.com/erafone/samsung-galaxy-note10-256gb'
browser.get(url)
    #browser.refresh()
click_xp  = '//*[@id="select_58"]/option[2]'
browser.find_element_by_xpath(click_xp).click()
time.sleep(1)
click_xp  = '//*[@id="select_58"]/option[3]'
browser.find_element_by_xpath(click_xp).click()
time.sleep(1)
click_xp  = '//*[@id="select_58"]/option[4]'
browser.find_element_by_xpath(click_xp).click()
time.sleep(1)
click_xp  = '//*[@id="select_58"]/option[5]'
browser.find_element_by_xpath(click_xp).click()

browser.close()