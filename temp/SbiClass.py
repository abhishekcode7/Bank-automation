
from flask.sessions import NullSession
from selenium import webdriver
import time
import csv

import os
import sys
import random
from datetime import date
from datetime import timedelta

#selenium libraries

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

# option1 = Options()
# option1.add_argument("--disable-notifications")

class SBI():
	def __init__(self):
		self.path = os.getcwd()
		self.path=self.path+"/chromedriver"
		self.session = 0
		self.driver = None

		self.url = "https://retail.onlinesbi.com/retail/login.htm"


	def start(self):
		# path = os.getcwd()
		# path=path+"/chromedriver"

		self.driver = webdriver.Chrome(executable_path=self.path)

		# url = "https://retail.onlinesbi.com/retail/login.htm"

		self.driver.get(self.url)

		# self.k=1

		# if self.k==1:
		# 	self.driver.find_element_by_class_name("login_button").click()
		# 	time.sleep(1)

		self.driver.find_element_by_class_name("login_button").click()
		time.sleep(1)

		x = self.driver.find_elements_by_xpath("//div[@class='form-group']")
		self.k=0

		username = x[0].find_element_by_id("username").send_keys("waskelyashwant")
		password = x[1].find_element_by_id("label2").send_keys("QXtt*444")
		self.driver.save_screenshot('sbi.png')
		time.sleep(1)

		im = Image.open("sbi.png")

		crop_rectangle = (70, 650, 220, 700)
		cropped_im = im.crop(crop_rectangle)

		cropped_im.save("captcha.png", "png")

		time.sleep(0.5)

	def cap(self,captcha):
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
		date = today.strftime("%d")+ "/" +today.strftime("%m") + "/"+ today.strftime("%y")
		return date

	def sessionVal(self):
    		return self.session

	def otp(self,otp):
		self.driver.find_element_by_id("smsPassword").send_keys(otp)
		time.sleep(1)

		self.driver.find_element_by_id("btContinue").click()
		time.sleep(2)

		current = self.driver.current_url
		if current == "https://retail.onlinesbi.com/retail/loginotpsfa.htm":
			a = self.driver.find_elements_by_id("icon_logout")
			a[1].click()
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
			try:
				ul = self.driver.find_element_by_id("quick_links_nh")
				li = ul.find_elements_by_tag_name("li")
				print(li[1])

				li[1].click()
				# time.sleep(20)

				today = date.today()
				d1 = today.strftime("%d/%m/%Y")
				yesterday = today - timedelta(days = 1)
				d2 = yesterday.strftime("%d/%m/%Y")
				self.driver.find_element_by_id("datepicker1").send_keys(d2)
				self.driver.find_element_by_id("datepicker2").send_keys(d1)

				# self.driver.find_element_by_id("excelformat").click()
				self.driver.find_element_by_id("Submit3").click()
				time.sleep(180)

			except:
				self.session = 0
				try:
					a = self.driver.find_elements_by_id("icon_logout")
					a[1].click()
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

# from flask.sessions import NullSession
# from selenium import webdriver
# import time
# import csv

# import os
# import sys
# import random
# from datetime import date
# from datetime import timedelta

# #selenium libraries

# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException   
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from selenium.webdriver.chrome.options import Options

# from PIL import Image

# # option1 = Options()
# # option1.add_argument("--disable-notifications")
# sbiStatus = 0
# def stat():
#     return sbiStatus
# class SBI():
# 	def __init__(self):
# 		self.path = os.getcwd()
# 		self.path=self.path+"/chromedriver"

# 		self.driver = None

# 		self.url = "https://retail.onlinesbi.com/retail/login.htm"


# 	def start(self):
# 		# path = os.getcwd()
# 		# path=path+"/chromedriver"

# 		self.driver = webdriver.Chrome(executable_path=self.path)

# 		# url = "https://retail.onlinesbi.com/retail/login.htm"

# 		self.driver.get(self.url)
# 		self.k=1

# 		if self.k==1:
# 			self.driver.find_element_by_class_name("login_button").click()
# 			time.sleep(1)

# 		x = self.driver.find_elements_by_xpath("//div[@class='form-group']")
# 		self.k=0

# 		username = x[0].find_element_by_id("username").send_keys("waskelyashwant")
# 		password = x[1].find_element_by_id("label2").send_keys("QXtt*444")
# 		self.driver.save_screenshot('sbi.png')
# 		time.sleep(1)

# 		im = Image.open("sbi.png")

# 		crop_rectangle = (70, 650, 220, 700)
# 		cropped_im = im.crop(crop_rectangle)

# 		cropped_im.save("captcha.png", "png")

# 		time.sleep(0.5)

# 	def cap(self,captcha):
# 		x = self.driver.find_elements_by_xpath("//div[@class='form-group']")

# 		x[2].find_element_by_id("loginCaptchaValue").send_keys(captcha)

# 		time.sleep(0.2)

# 		self.driver.find_element_by_id("Button2").click()

# 		time.sleep(3)
# 		self.driver.close()
# 		try:
# 			self.driver.find_element_by_id("smsPassword")
# 		except:
# 			self.k=0
# 			print("K")
# 			return 0

# 		return 1

# 	def dates(today):
# 		date = today.strftime("%d")+ "/" +today.strftime("%m") + "/"+ today.strftime("%y")
# 		return date

# 	def otp(self,otp):
# 		self.driver.find_element_by_id("smsPassword").send_keys(otp)
# 		time.sleep(1)

# 		self.driver.find_element_by_id("btContinue").click()
# 		time.sleep(5)

# 		current = self.driver.current_url

# 		if current != "https://retail.onlinesbi.com/retail/mypage.htm":
# 			return 0

# 		# fetching transaction history

# 		while(1):
# 			ul = self.driver.find_element_by_id("quick_links_nh")
# 			li = ul.find_elements_by_tag_name("li")
# 			print(li[1])

# 			li[1].click()
# 			# time.sleep(20)

# 			today = date.today()
# 			d1 = today.strftime("%d/%m/%Y")
# 			yesterday = today - timedelta(days = 1)
# 			d2 = yesterday.strftime("%d/%m/%Y")
# 			self.driver.find_element_by_id("datepicker1").send_keys(d2)
# 			self.driver.find_element_by_id("datepicker2").send_keys(d1)

# 			self.driver.find_element_by_id("excelformat").click()
# 			self.driver.find_element_by_id("Submit3").click()
# 			time.sleep(180)


# # sbi = SBI()
# # while(1):
# # 	sbi.start()
# # 	print("Enter captcha")
# # 	captcha = input()
# # 	x = sbi.cap(captcha)
# # 	if x==0:
# # 		print("Invalid Captcha")
# # 		continue
# # 	y=0
# # 	while(y<2):
# # 		print("y = ", y)
# # 		print("Enter OTP")
# # 		otp_no = input()
# # 		z=1
# # 		z = sbi.otp(otp_no)
# # 		if z == 0:
# # 			y=y+1
# # 			print("Wrong OTP")
# # 			continue
	
# # 	if y==2:
# # 		continue


# # driver.close()
# # https://retail.onlinesbi.com/retail/loginsubmit.htm
# # https://retail.onlinesbi.com/retail/loginsubmit.htm
