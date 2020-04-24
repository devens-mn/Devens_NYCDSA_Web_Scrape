from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

# go to main TOC page to get years of race
driver.get("https://www.bycmack.com/main_results.cfm")
years = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/div/table/tbody/tr/td[7]/div/table/tbody/tr/td")
# for yr in years[i].text:
#   print(yr)
# initialize array to hold urls for race results by years
race_rslts_urls = []
for i in range(1, len(years)):
    # print(years[i].text)
    # get rid of years without overall finish formatted results
    if (re.search('[OAoa]', years[i].text) != None):
        url_hold = "https://www.bycmack.com/past-results/" + years[i].text[:4] +"-overall.cfm"
        # print(url_hold)
        race_rslts_urls = race_rslts_urls + [url_hold]
#print out urls so I can know I formatted them correctly
print(race_rslts_urls)

# go to a given year's results
driver.get('https://www.bycmack.com/past-results/2017-overall.cfm')

# find the year on the page so I don't have to pass it otherwise
rc_year = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/b[1]")
print(rc_year.text)

# find and printrows of race results by entry / boat
rows = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr")
# iterate over rows in results page, if start at 1 get error, 2nd row is column names
for i in range(2, 100): # just do smallish number for now to avoid long waits with selenium
    # don't collect column header row (sail no = sail)
    # put in try to eliminate mistakes due to misformatting
    try:
        sail_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[2]'
        sail = driver.find_element_by_xpath(sail_path)
        if sail.text != 'Sail':
            boat_name_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[3]'
            boat_name = driver.find_element_by_xpath(boat_name_path)
            finish_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[5]'
            finish_time = driver.find_element_by_xpath(finish_time_path)
            elapse_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[6]'
            elapse_time = driver.find_element_by_xpath(elapse_time_path)
            corrected_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[7]'
            corrected_time = driver.find_element_by_xpath(corrected_time_path)
            class_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[8]'
            boat_class = driver.find_element_by_xpath(class_path)
            div_plc_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[9]'
            div_plc = driver.find_element_by_xpath(div_plc_path)
            print(int(rc_year.text[:4]),' ',sail.text,' ',boat_name.text, ' ',finish_time.text,' ',\
            elapse_time.text, ' ', corrected_time.text, ' ',boat_class.text,' ',div_plc.text)
        else:
            continue
    except:
        continue
driver.close()