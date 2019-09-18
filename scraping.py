from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
import os
import time
import csv
import subprocess
import datetime
import zipfile

def fullpage_screenshot(driver, file):
        print("Starting chrome full page screenshot workaround ...")
        driver.execute_script("window.scrollTo({0}, {1})".format(0, 0))

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        # print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        # x-min, y-min, x-max, y-max
        rectangles = []

        # 스크린샷 찍을 사각형 부분 좌표 따기
        # x, y 가득 찰 때까지 반복
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

                # print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        # 구한 좌표 기반으로 스크린샷 및 합치기
        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                # print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            # print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            # print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True

# subprocess.run(['test.py'], shell = True)

subsi_zip_list = []
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
    idx = line[0]
    subsi	= line[1]
    account = line[2]
    url = line[3]
    mkt_name = line[4]
    page_type = line[5]
    slide_YN = line[6]
    slide_path	 = line[7]
    toolbar_YN = line[8]
    toolbar_xpath = line[9]
    click_YN = line[10]
    click_xpath = line[11]
    desc = line[12]

    # filter idx
    try:
        if int(idx) < 58:
            continue
    except:
        continue

    print(idx)

    try:
        browser.get(url)
        #browser.refresh()

        try:
            if toolbar_YN == 'Y':
                print(toolbar_xpath)
                browser.find_element_by_xpath(toolbar_xpath).click()
                print('remove toolbar')
        except:
            print('toolbar error : {}'.format(toolbar_xpath))

        try:
            if click_YN == 'Y':
                click_xpath_list = click_xpath.split(',')
                for click_xp in range(len(click_xpath_list)):
                    print(click_xpath_list[click_xp])
                    browser.find_element_by_xpath(click_xpath_list[click_xp]).click()
                print('action click')
        except:
            print('click action error : {}'.format(click_xpath))

            for click_xp_ex in click_xpath_list[click_xp:]:
                time.sleep(3)
                try:
                    print('inner : {}'.format(click_xp_ex))

                    driver.execute_script("window.scrollTo({0}, {1})".format(0, 0))
                    browser.find_element_by_xpath(click_xp_ex).click()
                except:
                    continue
                    print('ERROR-ERROR-CLICK-{}'.format(click_xp_ex))
            print('click again')


        dir_path = './shot/{}/{}'.format(subsi, date)
        print(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("Directory ", dir_path, " Created ")


        fullpage_screenshot(browser, './shot/{}/{}/{}_{}_{}.png'.format(subsi, date, account, page_type, mkt_name))
        subsi_zip_list.append(subsi)

    except:
        print('error : {}'.format(line[0]))

browser.close()

subsi_zip_list = list(set(subsi_zip_list))

print(subsi_zip_list)

for subsi in subsi_zip_list:
    zip_path = './shot/{}_{}.zip'.format(subsi, date)
    dir_path = './shot/{}/{}'.format(subsi, date)
    print('zip_path : {}, dir_path : {}'.format(zip_path, dir_path))
    fantasy_zip = zipfile.ZipFile(zip_path, 'w')

    for folder, subfolders, files in os.walk(dir_path):
        for file in files:
            fantasy_zip.write(os.path.join(folder, file),
                              os.path.relpath(os.path.join(folder, file), dir_path),
                              compress_type=zipfile.ZIP_DEFLATED)

    fantasy_zip.close()


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
