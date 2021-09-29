from Screenshot import Screenshot_Clipping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
import base64
import io
import os
from PIL import Image
import datetime
import pytz


psw = os.environ['PW']
usn = os.environ['UN']
utctime = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
latz = pytz.timezone('America/Los_Angeles')
latime = latz.normalize(utctime.astimezone(latz))
curtime = latime.strftime('%H')
ob=Screenshot_Clipping.Screenshot()
chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1680x1050')
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)


# Login to the account.
loginurl = "https://000000000000.signin.aws.amazon.com/console"  #Change account number to your actual AWS account number.
driver.get(loginurl)

un = driver.find_element_by_id("username")
un.send_keys(usn)
pw = driver.find_element_by_id("password")
pw.send_keys(psw)
time.sleep(5)
button = driver.find_element_by_id("signin_button")
button.click()

# Go to the dashboard to get the screenshot.
time.sleep(3)
url = os.environ['DASH_URL']  #page or dashboard we  are getting the screenshot from.
driver.get(url)
time.sleep(5)

# Take the screenshot of only the element we want.
element = driver.find_element_by_class_name('react-grid-layout') #change this to the element you need to grab a picture of.
img_path = ob.get_element(driver, element, r'.')

driver.close()

driver.quit()

#Do what you need to with this image or the byte array of the image use curtime to append a timestamp adjusting timezone as needed.

img = Image.open(img_path, mode='r')
imgByteArr = io.BytesIO()
img.save(imgByteArr, format='PNG')


#Delete the image from the system so we can do it again on the next CRON job
os.remove(img_path)
os.remove(".\\clipping_shot.png")
