# Toll Scraper
import time
import datetime
import csv
from selenium import webdriver


def loadDriver():
    global driver
    driver = webdriver.Firefox()
    driver.set_window_position(0, 0)
    driver.set_window_size(400, 800)
    driver.get("https://vai66tolls.com/")


def whatTimeIsIt():
    global east
    global west
    global now
    now = datetime.datetime.now()
    east = ((now.isoweekday() in range(1, 6)) & (now.hour in range(5, 10)))
    west = (now.weekday() < 5) & (now.hour in range(15, 19))


def clickXPATH(XPATH):
    driver.find_element_by_xpath(XPATH).click()
    time.sleep(1)

def run(direction):
    global commute
    if direction is east:
        commute = "Eastbound I66 West to Washington"
        clickXPATH("/html/body/form/div[4]/ul/li[1]/a/span[1]")  # Current Toll Estimate
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[1]/span")  # Eastbound AM Tolls
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]")  # Enter I-66West
        clickXPATH("//*[@id='btnUpdateBeginSel']")  # Select
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[8]")  # Exit Washington
        clickXPATH("//*[@id='btnUpdateEndSel']")  # Select
    elif direction is west:
        commute = "Westbound Washington to I66West"
        clickXPATH("/html/body/form/div[4]/ul/li[1]/a/span[1]")  # Current Toll Estimate
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[2]/span")  # Westbound PM Tolls
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]")  # Enter Washington
        clickXPATH("//*[@id='btnUpdateBeginSel']")  # Select
        clickXPATH("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[6]")  # Exit I-66West
        clickXPATH("//*[@id='btnUpdateEndSel']")  # Select
    else:
        print("[Error] direction '", direction, "' not supported")
        driver.close()
        driver.quit()
    clickXPATH("//*[@id='tollRefreshBtn']")
    toll = driver.find_element_by_xpath("//*[@id='spanTollAmt']").text
    whatTimeIsIt()
    if toll[0] == "N":
        toll = 0
    with open('Output.csv', 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([commute, now, toll])
    print(commute, toll, now)
    print("CSV Updated")
    time.sleep(60)


def main():
    if __name__ == "__main__":
        loadDriver()
        whatTimeIsIt()
        while True:
            if east is True:
                run(east)
            elif west is True:
                run(west)
            else:
                print("No tolls right now. Waiting 60 seconds and trying again")
                time.sleep(60)


if __name__ == "__main__":
    main()
