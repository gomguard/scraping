from io import StringIO
import time
import datetime
import os
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image

# https://yeolco.tistory.com/93 - send mail
# https://brunch.co.kr/@jk-lab/31 - python attach file
now = datetime.datetime.now()
date = now.strftime('%Y%m%d')
subsi_list = os.listdir('./shot')
subsi_list = 'SEIN'

print(subsi_list)

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()  # say Hello
smtp.starttls()  # TLS 사용시 필요

# create app password
# https://devanswers.co/create-application-specific-password-gmail/
# https://security.google.com/settings/security/apppasswords
smtp.login('knholic@gmail.com', 'npwvucvzkznguere')

msg = MIMEBase('multipart', 'mixed')

cont = MIMEText('test : attach zip file')
cont['Subject'] = '테스트'
cont['To'] = 'knholic@gmail.com'
msg.attach(cont)


dir_path = './shot/SEIN/20190918/'
dir_path_resize = './shot/SEIN/20190918/resize/'

file_list = [file for file in os.listdir(dir_path) if file.endswith(".png")]

for file_path in file_list:
    print(file_path)
    source_image = dir_path + file_path
    target_image = dir_path_resize + file_path

    image = Image.open(source_image)
    # resize 할 이미지 사이즈
    width, height = image.size
    resize_image = image.resize((int(width / 1.5), int(height / 1.5)))


    if not os.path.exists(dir_path_resize):
        os.makedirs(dir_path_resize)
    try:
        os.remove(target_image)
    except:
        print('no file')
    resize_image.save(target_image, "JPEG", quality=75)

# subsi_list = 'seau'
# for subsi in subsi_list:
subsi = subsi_list
zip_path = './shot/{}_{}.zip'.format(subsi, date)
dir_path = './shot/{}/{}/resize'.format(subsi, date)
print('zip_path : {}, dir_path : {}'.format(zip_path, dir_path))
fantasy_zip = zipfile.ZipFile(zip_path, 'w')

for folder, subfolders, files in os.walk(dir_path):
    for file in files:
        fantasy_zip.write(os.path.join(folder, file),
                          os.path.relpath(os.path.join(folder, file), dir_path),
                          compress_type=zipfile.ZIP_DEFLATED)

fantasy_zip.close()

## file 일경우
# part = MIMEBase('application', 'octet-stream')
# part.set_payload(open(fantasy_zip, 'rb').read())
## zip 일 경우
part = MIMEBase('application', 'zip')
part.set_payload(open(zip_path, 'rb').read())

encoders.encode_base64(part)
part.add_header('Content-Disposition',
                'attachment; filename="%s"'% os.path.basename(zip_path))
msg.attach(part)

smtp.sendmail('knholic@gmail.com', cont['To'], msg.as_string())

smtp.quit()

