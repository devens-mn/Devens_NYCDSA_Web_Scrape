from selenium import webdriver
import time
import re
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

csv_file = open('detmacraceresults_2019.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

# driver.get("https://www.bycmack.com/main_results.cfm")
# years = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/div/table/tbody/tr/td[7]/div/table/tbody/tr/td")
# for i in range(len(years)):
#     print(years[i].text[0:5])

driver.get("https://www.bycmack.com/past-results/2019-overall.cfm")

rc_year = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td/div/b[1]")
print(rc_year)
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
            print(hold_lst[div_iter], ' ',rc_year.text[:4], ' ',sail.text,' ',boat_name.text, ' ', finish_time.text,' ',div_plc.text)
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
csv_file.close()
driver.close()

# this returns all the rows as strings
# print('*'*50)
# for i in range(len(row)):
#     print(row[i].text)
# print('*'*50)