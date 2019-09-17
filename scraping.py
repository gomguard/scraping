from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
import os
import time
import csv
import subprocess
import datetime

def fullpage_screenshot(driver, file):
        print("Starting chrome full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True

# subprocess.run(['test.py'], shell = True)

driver_path = 'C:/Users/kx682tw/Downloads/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

## proxy option
# US Proxy : https://www.proxynova.com/proxy-server-list/country-us/
# PROXY = "68.251.250.193:8080"
# options.add_argument('--proxy-server=%s' % PROXY)

## open browser
browser = webdriver.Chrome(driver_path, chrome_options = options)

now = datetime.datetime.now()
date = now.strftime('%Y%m%d')

f = open('./url_list.csv', 'r', encoding = 'UTF-8')
rdr = csv.reader(f)

for line in rdr:
    print(line)

    subsi = line[0]
    account	 = line[1]
    url = line[2]
    mkt_name = line[3]
    page_type = line[4]
    slide_YN = line[5]
    slide_path = line[6]
    toolbar_YN	 = line[7]
    toolbar_xpath = line[8]
    click_YN = line[9]
    click_xpath = line[10]
    desc = line[11]

    try:
        browser.get(url)
        #browser.refresh()
        if toolbar_YN == 'Y':
            print(toolbar_xpath)
            browser.find_element_by_xpath(toolbar_xpath).click()
            print('remove toolbar')

        if click_YN == 'Y':
            print(click_xpath)
            browser.find_element_by_xpath(click_xpath).click()
            print('action click')

        dir_path = './{}/{}'.format(subsi, date)
        print(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Directory ", dir_path, " Created ")


        fullpage_screenshot(browser, './{}/{}/{}_{}_{}.png'.format(subsi, date, account, page_type, mkt_name))
    except:
        print('error : {}'.format(line[0]))


browser.close()

## click part
# print('click')
# browser.find_element_by_xpath('//*[@id="9f1a4688a6330a5fcacee51f8b6b220ae13b4af0"]/div[1]/div[2]/div[1]/a').click()
#
# x_path = '//*[@id="main-content"]/div/div/ng-component/tmo-view-component/div/div/div/div/product-details-element/div[1]/div[2]/div/tmo-sku-picker/div/div[1]/div/button[1]'
#
# browser.find_element_by_xpath(x_path).click()
# print('sleep')
# time.sleep(3)
# x_path = '//*[@id="main-content"]/div/div/ng-component/tmo-view-component/div/div/div/div/product-details-element/div[1]/div[2]/div/tmo-sku-picker/div/div[1]/div/button[2]'
#
# browser.find_element_by_xpath(x_path).click()
