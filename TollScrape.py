# Toll Scraper

import time, datetime, csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Open window and set Resolution
driver = webdriver.Firefox()
driver.set_window_position(0, 0)
driver.set_window_size(400, 800)
driver.get("https://vai66tolls.com/")

# Select Toll Route (Washington to 66-West)
time.sleep(1)
driver.find_element_by_xpath("/html/body/form/div[4]/ul/li[1]/a/span[1]").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[2]/span").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]").click()
driver.find_element_by_xpath("//*[@id='btnUpdateBeginSel']").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[6]").click()
driver.find_element_by_xpath("//*[@id='btnUpdateEndSel']").click()
time.sleep(1)

#Scrape the Toll Amount and Append to CSV
count=0
while count < 100:
	driver.find_element_by_xpath("//*[@id='tollRefreshBtn']").click()
	toll = driver.find_element_by_xpath("//*[@id='spanTollAmt']").text
	now = str(datetime.datetime.now())
	print(toll,now)
	count += 1

	#Write to csv
	with open('Output.csv' , 'a') as newFile:
		newFileWriter = csv.writer(newFile)
		newFileWriter.writerow([now,toll])
	print("CSV Updated")
	time.sleep(60)

time.sleep(10)
driver.close()
