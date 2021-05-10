from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pyttsx3
import time
import smtplib
from email.mime.text import MIMEText

vaccineFound = False
driver = webdriver.Chrome("/Users/keerthika/Downloads/chromedriver")
driver.get("https://www.cowin.gov.in")
checkBox = driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div/label/div')
checkBox.click();
search=driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[3]/button')
engine = pyttsx3.init()
engine.setProperty('rate',145)
for i in range(100):
   print('Started searching')
   state=driver.find_element_by_xpath('//*[@id="mat-select-0"]')
   state.click()
   tn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'//*[@id="mat-option-31"]'))
   )
   tn.click()
   district=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[2]')))
   district.click()
   chennai=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mat-option-41"]/span')))
   chennai.click()
   search.click()
   ageBlock = driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[3]/div/div[1]')
   ageBlock.click()
   covishield = driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[3]/div/div[3]')
   covishield.click()
   table = driver.find_element_by_xpath('/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[6]')
   hospName=table.find_elements_by_tag_name('h5.center-name-title')
   bookingStatus=table.find_elements_by_tag_name('a')
   rows = table.find_elements_by_tag_name('div.col-sm-12.col-md-12.col-lg-12')
   for row in rows:
      bookstatus = row.find_elements_by_tag_name('a')
      hospname = row.find_elements_by_tag_name('h5.center-name-title')
      for status,name in ((x,y) for x in bookstatus for y in hospname):
         if status.text != 'Booked' and status.text != 'NA':
            engine.say('Alert: Vaccine found!')
            engine.say(str(name.text))
            vaccineFound  = True
            msg = MIMEText(str('Found vaccine at '+str(name.text)))
            email = "your mail"
            msg['Subject'] = 'Vaccine Alert'
            msg['From'] = email
            msg['To'] = email
            password = "***"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, email, text)
            server.quit()
            engine.runAndWait()
            break
      if vaccineFound:
         break
   if not vaccineFound:
      engine.say('No vaccine found this time, better luck next time')
      engine.runAndWait()
   if i == 99 or vaccineFound:
      engine.say('Reset Program to continue searching')
      engine.runAndWait()
      break
   time.sleep(400)


