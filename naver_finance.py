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
import csv
import pandas as pd


'''
# url maker
code_list = pd.read_csv('./naver_finance_code.csv')
print(code_list)

lv = list()
for idx in range(1, 8):
    lv.append(code_list[code_list.type == idx])
url_list = list()
with open('url_list_3.txt', 'w') as f:
    for lv1_idx in range(0, len(lv[0])):
        for lv2_idx in range(0, len(lv[1])):
            for lv3_idx in range(0, len(lv[2])):
                for lv6_idx in range(0, len(lv[5])):
                        url = f'https://finance.naver.com/fund/fundFinderList.nhn?search=' \
                              f'{lv[0].iloc[lv1_idx, 2]}'\
                              f',{lv[1].iloc[lv2_idx, 2]}'\ 
                              f',{lv[2].iloc[lv3_idx, 2]}'\
                              f',{lv[5].iloc[lv6_idx, 2]}&pageSize=10000&page=' 

                        f.write(f"{url}\n")


f.close()


'''
def scraping_data(line):
    line = line.strip()
    url = line + '1'

    browser.get(url)
    # get info

    # browser.switch_to_frame('fundList')

    fund_cnt = browser.find_element_by_xpath(f'/html/body/div[1]/h3/em/strong').text
    fund_info = url[url.find('=') + 1:url.find('&')].split(',')
    with open(output_file_name, 'a', newline = '') as f_csv:
        wr = csv.writer(f_csv)
        if fund_cnt == '0':
            print('nothing')
            wr.writerow(fund_info)

            return 0
        else:

            # fund_cnt = int(fund_cnt)
            # page_cnt = fund_cnt // 20 + 1
            # fund_cnt_rest = fund_cnt % 20

            # for page_idx in range(1, (page_cnt + 1)):
            #     url = line + str(page_idx)
            #     browser.get(url)

                # if page_idx == page_cnt:
                #     fund_range = fund_cnt_rest
                # else:
                #     fund_range = 20
                # print(url)
                # browser.switch_to_frame('fundList')
            idx = 1
            for fund_idx in range(1, int(fund_cnt) + 1):
                page_info = list(fund_info)
                mkt_nm = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/thead/tr/th').get_attribute('title')
                init_dt = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[1]/td[1]').text
                init_price = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[2]/td[1]').text
                fund_type = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[1]/td[2]').text
                try:
                    fund_type_lv1, fund_type_lv2 = fund_type.split('>')
                except:
                    fund_type_lv1 = fund_type
                    fund_type_lv2 = '-'
                operator = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[2]/td[2]').text
                commission = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[3]/td[1]').text
                profit = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/table/tbody/tr[{fund_idx}]/td[2]/table/tbody/tr[3]/td[2]').text
                page_info.append(mkt_nm)
                page_info.append(init_dt)
                page_info.append(init_price)
                page_info.append(fund_type_lv1)
                page_info.append(fund_type_lv2)
                page_info.append(operator)
                page_info.append(commission)
                page_info.append(profit)
                idx = idx + 1
                if idx % 100 == 0:
                    print(idx)
                #print(mkt_nm, init_dt, init_price, fund_type_lv1, fund_type_lv2, operator, commission, profit)
                wr.writerow(page_info)



# tot url : 2,150,400 line
f = open("./url_list_4.txt", 'r')

# driver setting
driver_path = 'C:/Users/kx682tw/Downloads/chromedriver.exe'
options = webdriver.ChromeOptions()

## open browser
browser = webdriver.Chrome(driver_path, chrome_options=options)

output_file_name = 'output_4.csv'
if os.path.exists(output_file_name):
    os.remove(output_file_name)

idx = 1
while True:
    print(idx, '/ 1,200 - {} % complete'.format(round(idx / 1200 * 100, 2)))
    idx = idx + 1

    line = f.readline()
    if not line: break
    scraping_data(line)
f.close()


browser.close()
