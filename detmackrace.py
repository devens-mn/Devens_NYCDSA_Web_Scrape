from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

driver.get("https://www.bycmack.com/main_results.cfm")
years = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td/div/table/tbody/tr/td[7]/div/table/tbody/tr/td")
for yr in years[i].text:
	print(yr)