# Toll Scraper
import time
import csv
from selenium import webdriver
from datetime import datetime
from datetime import time as dtime
from selenium.webdriver.firefox.options import Options


def loadDriver():
    global driver
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(400, 800)


def whatTimeIsIt():
    global east
    global west
    global now
    global date
    global text_time
    now = datetime.now()
    now_time = now.time()
    date = datetime.today().strftime('%Y-%m-%d')
    text_time = datetime.now().strftime('%H:%M:%S')
    east = ((now.isoweekday() in range(1, 6)) & ((now_time >= dtime(5, 30))& (now_time <= dtime(10, 30))))
    west = ((now.isoweekday() in range(1, 6)) & ((now_time >= dtime(15))& (now_time <= dtime(19))))


def clickxpath(xpath):
    driver.find_element_by_xpath(xpath).click()
    time.sleep(1)


def run(direction):
    global commute
    if direction is east:
        commute = "Eastbound I66 West to Washington"
        driver.get("https://vai66tolls.com/")
        clickxpath("/html/body/form/div[4]/ul/li[1]/a/span[1]")  # Current Toll Estimate
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[1]/span")  # Eastbound AM Tolls
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]")  # Enter I-66West
        clickxpath("//*[@id='btnUpdateBeginSel']")  # Select
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[8]")  # Exit Washington
        clickxpath("//*[@id='btnUpdateEndSel']")  # Select
    elif direction is west:
        commute = "Westbound Washington to I66West"
        driver.get("https://vai66tolls.com/")
        clickxpath("/html/body/form/div[4]/ul/li[1]/a/span[1]")  # Current Toll Estimate
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[4]/div[2]/span")  # Westbound PM Tolls
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[6]/div/select/option[2]")  # Enter Washington
        clickxpath("//*[@id='btnUpdateBeginSel']")  # Select
        clickxpath("/html/body/form/div[5]/div/div/div/div/div[2]/div[7]/div/select/option[6]")  # Exit I-66West
        clickxpath("//*[@id='btnUpdateEndSel']")  # Select
    else:
        print("[Error] direction '", direction, "' not supported")
        driver.close()
        driver.quit()


def collect_toll():
    whatTimeIsIt()
    clickxpath("//*[@id='tollRefreshBtn']")
    toll = driver.find_element_by_xpath("//*[@id='spanTollAmt']").text
    if toll[0] == "N":
        toll = 0
    with open('Output.csv', 'a') as newFile:
        newfilewriter = csv.writer(newFile)
        newfilewriter.writerow([commute, date, text_time, toll])
    print(commute, date, text_time, toll)
    print("CSV Updated\n")
    time.sleep(60)


def main():
    if __name__ == "__main__":
        loadDriver()
        while True:
            whatTimeIsIt()
            if east is True:
                run(east)
                collect_toll()
            elif west is True:
                run(west)
                collect_toll()
            else:
                print("No tolls right now. Waiting 60 seconds and trying again\n")
                time.sleep(60)


if __name__ == "__main__":
    main()
