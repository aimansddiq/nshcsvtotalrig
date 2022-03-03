#NSH-Extractor-AimanSiddiq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
def extraction_function(links):
    option = webdriver.ChromeOptions()
    option.add_argument('log-level=3')
    option.add_argument("")
    web = webdriver.Chrome('',options=option)
    for i in links:
        web.get(links[i])
        delay = 30 # seconds
        try:
            export = WebDriverWait(web, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[4]/div/div[4]/div[4]/div[1]')))        
        except TimeoutException:
            print("Loading took too much time!")
        finally:
            try:
                export = web.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/div/div[4]/div[1]/div[3]/button')
                export.click()
                time.sleep(5)
            except Exception:
                print("Unable to extract",i)
    web.close()

links = {}
extraction_function(links)
