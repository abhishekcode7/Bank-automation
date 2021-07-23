from flask.sessions import NullSession
from selenium import webdriver
import time
import csv

import os
import sys
import random
from datetime import date
from datetime import timedelta
from datetime import datetime

# selenium libraries

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

from PIL import Image

import mysql.connector

# option1 = Options()
# option1.add_argument("--disable-notifications")


def history(gdate):
    # mydb = mysql.connector.connect(
    #     host="localhost", user="root", passwd="123456", database="sbi")
    mycursor = mydb.cursor()
    query = """SELECT SUM(credit) FROM transcript WHERE dates=%s"""
    t = (gdate)
    mycursor.execute(query, (t,))
    sums = 0
    for tb in mycursor:
        sums = tb[0]
    return sums


class SBI():
    def __init__(self):
        self.path = os.getcwd()
        self.path = self.path+"/chromedriver"
        self.session = 0
        self.driver = None

        self.url = "https://retail.onlinesbi.com/retail/login.htm"
        # self.mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     passwd="123456",
        #     database="sbi"
        # )
        # self.mycursor = self.mydb.cursor()
        self.sums = 0
        self.logid = ""
        self.logpass = ""

    def checkCred(self):
        if self.logid == "" or self.logpass=="":
            return 0
        return 1

    def start(self):

        if self.driver != None:
            self.driver.quit()

        self.driver = webdriver.Chrome(executable_path=self.path)

        self.driver.get(self.url)

        self.driver.find_element_by_class_name("login_button").click()
        time.sleep(1)

        x = self.driver.find_elements_by_xpath("//div[@class='form-group']")
        self.k = 0

        username = x[0].find_element_by_id(
            "username").send_keys(self.logid)
        password = x[1].find_element_by_id("label2").send_keys(self.logpass)
        self.driver.save_screenshot('sbi.png')
        time.sleep(1)

        im = Image.open("sbi.png")

        crop_rectangle = (70, 650, 220, 700)
        cropped_im = im.crop(crop_rectangle)

        cropped_im.save("captcha.png", "png")

        time.sleep(0.5)
    def updateSettings(self,idd,passs):
        self.logid = idd
        self.logpass = passs
        
    def cap(self, captcha):
        x = self.driver.find_elements_by_xpath("//div[@class='form-group']")
        os.remove("captcha.png")

        x[2].find_element_by_id("loginCaptchaValue").send_keys(captcha)

        time.sleep(0.2)

        self.driver.find_element_by_id("Button2").click()

        time.sleep(3)

        try:
            self.driver.find_element_by_id("smsPassword")
        except:
            self.driver.close()
            return 0

        return 1

    def dates(today):
        date = today.strftime("%d") + "/" + \
            today.strftime("%m") + "/" + today.strftime("%y")
        return date

    def sessionVal(self):
        return self.session

    def otp(self, otp):
        self.driver.find_element_by_id("smsPassword").send_keys(otp)
        time.sleep(1)

        self.driver.find_element_by_id("btContinue").click()
        time.sleep(2)

        current = self.driver.current_url
        if current == "https://retail.onlinesbi.com/retail/loginotpsfa.htm":
            a1 = self.driver.find_elements_by_id("icon_logout")
            a1[1].click()
            self.driver.close()
            return 0

        time.sleep(3)

        current = self.driver.current_url

        if current != "https://retail.onlinesbi.com/retail/mypage.htm":
            return 0

        return 1

    def loop3(self):
        # fetching transaction history

        self.session = 1
        while(1):
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            try:
                data = "INSERT INTO transcript (dates, narration, ref_cheque_no, debit, credit, balance) VALUES(%s, %s, %s, %s, %s, %s)"

                self.mycursor.execute("SELECT * FROM transcript")

                count = 0
                for row in self.mycursor:
                    count += 1

                ul = self.driver.find_element_by_id("quick_links_nh")
                li = ul.find_elements_by_tag_name("li")
                print(li[1])

                li[1].click()
                # time.sleep(20)

                today = date.today()
                d1 = today.strftime("%d/%m/%Y")
                yesterday = today - timedelta(days=8)
                d2 = yesterday.strftime("%d/%m/%Y")
                self.driver.find_element_by_id("datepicker1").send_keys(d2)
                self.driver.find_element_by_id("datepicker2").send_keys(d1)

                self.driver.find_element_by_id("Submit3").click()
                time.sleep(1)

                data = "INSERT IGNORE INTO transcript (id, dates, narration, ref_cheque_no, debit, credit, balance) VALUES(%s, %s, %s, %s, %s, %s, %s)"

                try:
                    content = self.driver.find_elements_by_class_name(
                        "content_area")
                    tbody = content[1].find_element_by_tag_name("tbody")
                    trans_list = tbody.find_elements_by_tag_name("tr")

                    for i in range(0, len(trans_list)-1):
                        td = trans_list[i].find_elements_by_tag_name("td")
                        td1 = ["", "", "", "", "", ""]
                        # print(td[2].text)
                        # print(len(td[2].text))
                        for i in range(0, 6):
                            if len(td[i].text) == 0:
                                td1[i] = ""
                            else:
                                td1[i] = td[i].text

                            if i == 0:
                                td1[i] = td1[i].split('\n')[0]

                            td1[i] = td1[i].replace(',', '')
                        # print(td1)
                        count += 1
                        b1 = (count, td1[0], td1[1], td1[2],
                              td1[3], td1[4], td1[5])
                        self.mycursor.execute(data, b1)
                        self.mydb.commit()
                        # print("success")
                except:
                    pass

                time.sleep(180)

            except:
                self.session = 0

                try:
                    a = self.driver.find_elements_by_id("icon_logout")
                    a[1].click()
                    time.sleep(1)
                    g = self.driver.find_element_by_class_name("modal-body")
                    bt = g.find_elements_by_tag_name("button")
                    bt[1].click()
                    time.sleep(3)
                    self.driver.close()
                except:
                    print("Session out")
                    self.driver.close()

                break


# while(1):
# 	sbi = SBI()
# 	sbi.start()
# 	print("Enter captcha")
# 	captcha = input()
# 	x = sbi.cap(captcha)
# 	if x==0:
# 		print("Invalid Captcha")
# 		continue

# 	print("Enter OTP")
# 	otp_no = input()

# 	z = sbi.otp(otp_no)
# 	if z == 0:
# 		print("Wrong OTP")
# 		continue


# driver.close()
# https://retail.onlinesbi.com/retail/loginsubmit.htm
# https://retail.onlinesbi.com/retail/loginsubmit.htm
