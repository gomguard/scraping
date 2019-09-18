from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
import os
import time
import csv
import subprocess
import datetime
import os
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


now = datetime.datetime.now()
date = now.strftime('%Y%m%d')
subsi_list = os.listdir('./shot')

print(subsi_list)

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()  # say Hello
smtp.starttls()  # TLS 사용시 필요


smtp.login('knholic@gmail.com', 'npwvucvzkznguere')

msg = MIMEBase('multipart', 'mixed')

cont = MIMEText('본문 테스트 메시지 - - - - - - - -')
cont['Subject'] = '테스트'
cont['To'] = 'knholic@gmail.com'
msg.attach(cont)

file_path = './shot/seau_20190918.zip'
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(file_path, 'rb').read())

encoders.encode_base64(part)
part.add_header('Content-Disposition',
                'attachment; filename="%s"'% os.path.basename(file_path))
msg.attach(part)

smtp.sendmail('knholic@gmail.com', msg['To'], msg.as_string())

smtp.quit()

'''
driver_path = 'C:/Users/kx682tw/Downloads/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

## proxy option
# US Proxy : https://www.proxynova.com/proxy-server-list/country-us/
PROXY = "35.224.38.98:8080"
options.add_argument('--proxy-server=%s' % PROXY)

## open browser
browser = webdriver.Chrome(driver_path, chrome_options = options)

# url = 'https://www.optus.com.au/shop/mobile/phones/iphone/iphone-11'
url = 'https://www.sprint.com'
browser.get(url)
#     #browser.refresh()
# click_xp  = '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[1]/div/div/a[1]'
# browser.find_element_by_xpath(click_xp).click()
# time.sleep(1)
# click_xp  = '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[1]/div/div/a[2]'
# browser.find_element_by_xpath(click_xp).click()
# time.sleep(1)
# click_xp  = '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[1]/div/div/a[3]'
# browser.find_element_by_xpath(click_xp).click()
# time.sleep(1)
# click_xp  = '//*[@id="main"]/div[1]/div/div[1]/div[2]/div[1]/div/div/a[2]'
# browser.find_element_by_xpath(click_xp).click()
#
# browser.close()



for subsi in subsi_list:
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
'''