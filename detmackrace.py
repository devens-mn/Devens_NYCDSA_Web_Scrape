# import selenium drivers, regex, csv to write the output
from selenium import webdriver
import time
import re
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

# start the webdriver
driver = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

# open the csv file to write
csv_file = open('detmacraceresults.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

# go to main results page, with links to all years
driver.get("https://www.bycmack.com/main_results.cfm")
years = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/div/table/tbody/tr/td[7]/div/table/tbody/tr/td")
# create list to hold urls 
race_rslts_urls = []
for i in range(1, len(years)):
    # get rid of years without overall finish formatted results
    if (re.search('[OAoa]', years[i].text) != None):
        url_hold = "https://www.bycmack.com/past-results/" + years[i].text[:4] +"-overall.cfm"
        # print(url_hold)
        race_rslts_urls = race_rslts_urls + [url_hold]

# in 2019 they changed format so will collect from that indpendently and first
driver.get("https://www.bycmack.com/past-results/2019-overall.cfm")
rc_year = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/b[1]")
# show progress
print("https://www.bycmack.com/past-results/2019-overall.cfm")
div_hdrs = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/b")
hold_lst = []
for i in range(len(div_hdrs)):
    if 'division' in div_hdrs[i].text.lower().split():
        hold_lst = hold_lst + [div_hdrs[i].text]
    else:
        continue
rows = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr")
# try to return the fields from each row
div_iter = 0
for i in range(3, len(rows)+1):
    race_dict = {}
    try:
        sail_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[2]'
        sail = driver.find_element_by_xpath(sail_path)
        if sail.text != 'Sail':
            boat_name_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[3]'
            boat_name = driver.find_element_by_xpath(boat_name_path)
            # design_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[5]'
            # design = driver.find_element_by_xpath(design_path)
            finish_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[7]'
            finish_time = driver.find_element_by_xpath(finish_time_path)
            elapse_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[8]'
            elapse_time = driver.find_element_by_xpath(elapse_time_path)
            corrected_time_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[9]'
            corrected_time = driver.find_element_by_xpath(corrected_time_path)
            class_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[10]'
            boat_class = driver.find_element_by_xpath(class_path)
            div_plc_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[11]'
            div_plc = driver.find_element_by_xpath(div_plc_path)
        else:
            div_iter = div_iter + 1
            continue
    except:
        continue
    race_dict['division'] = hold_lst[div_iter] 
    race_dict['rc_year'] = rc_year.text[:5]
    race_dict['sail'] = sail.text
    race_dict['boat_name'] = boat_name.text
    # race_dict['design'] = design.text
    race_dict['finish_time'] = finish_time.text
    race_dict['elapse_time'] = elapse_time.text
    race_dict['corrected_time'] = corrected_time.text
    race_dict['boat_class'] = boat_class.text
    race_dict['div_plc'] = div_plc.text
    writer.writerow(race_dict.values())

# now iterate from 2018 backward to end of list gathered in lines 20-30
for j in range(1, len(race_rslts_urls)): #fill in with len race_rslts_urls
# show progress
    print(race_rslts_urls[j])
    driver.get(race_rslts_urls[j])
    # find division headers
    div_hdrs = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/b")
    hold_lst = []
    for i in range(len(div_hdrs)):
        if 'division' in div_hdrs[i].text.lower().split():
            hold_lst = hold_lst + [div_hdrs[i].text]
        else:
            continue

    rc_year = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/b[1]")
    rows = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr")
    # for i in range(1, len(rows)):
    #     print(rows[i].text)
    # set iterator for division header list to -1 since it trips right out
    div_iter = -1
    # try to return the fields from each row
    for i in range(2, len(rows)+1):
        #len(rows)+1
        race_dict = {}
        try:
            # print(i)
            sail_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[2]'
            sail = driver.find_element_by_xpath(sail_path)
            if sail.text != 'Sail':
                boat_name_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[3]'
                boat_name = driver.find_element_by_xpath(boat_name_path)
                # design_path = '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[' +str(i) + ']/td[5]'
                # design = driver.find_element_by_xpath(design_path)
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
                # print(int(rc_year.text[:4]),' ',sail.text,' ',boat_name.text, ' ', finish_time.text, '')
            else:
                div_iter = div_iter + 1
                continue
        except:
            continue

        race_dict['division'] = hold_lst[div_iter] 
        race_dict['rc_year'] = rc_year.text[:5]
        race_dict['sail'] = sail.text
        race_dict['boat_name'] = boat_name.text
        race_dict['finish_time'] = finish_time.text
        race_dict['elapse_time'] = elapse_time.text
        race_dict['corrected_time'] = corrected_time.text
        race_dict['boat_class'] = boat_class.text
        race_dict['div_plc'] = div_plc.text
        writer.writerow(race_dict.values())
csv_file.close()
driver.close()