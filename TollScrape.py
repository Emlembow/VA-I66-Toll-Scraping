# Toll Scraper

import time
import datetime
import csv
from selenium import webdriver


def loadDriver():

    # Open window and set Resolution
    global driver
    driver = webdriver.Firefox()
    driver.set_window_position(0, 0)
    driver.set_window_size(400, 800)
    driver.get("https://vai66tolls.com/")


def whatTimeIsIt():
    global now
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def clickXPATH(XPATH):
    driver.find_element_by_xpath(XPATH).click()
    time.sleep(1)

def run():
    # Select Toll Route (Washington to 66-West)
    clickXPATH("/html/body/form/div[4]/ul/li[1]/a/span[1]")
    clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[2]/span")
    clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]")
    clickXPATH("//*[@id='btnUpdateBeginSel']")
    clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[6]")
    clickXPATH("//*[@id='btnUpdateEndSel']")

    # Scrape the Toll Amount and Append to CSV
    var = 1
    while var == 1:
        clickXPATH("//*[@id='tollRefreshBtn']")
        toll = driver.find_element_by_xpath("//*[@id='spanTollAmt']").text
        whatTimeIsIt()
        if toll[0] == "N":
            toll = 0
        with open('Output.csv', 'a') as newFile:
            newFileWriter = csv.writer(newFile)
            newFileWriter.writerow([now, toll])
        print(toll, now)
        print("CSV Updated")
        time.sleep(60)


def main():
    if __name__ == "__main__":
        loadDriver()
        run()


if __name__ == "__main__":
    main()
