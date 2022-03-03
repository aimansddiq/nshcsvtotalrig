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
    option.add_argument("user-data-dir=C:\\Users\\AIMAN\\AppData\\Local\\Google\\Chrome\\User Data")
    web = webdriver.Chrome('D:\AIMAN\OneDrive - Universiti Teknologi MARA\AIMAN\Project\Last Hope Business\Mining\chromedriver.exe',options=option)
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

links = {"Bada":"https://www.nicehash.com/my/mining/rigs/0-vZj1jM6rFFKzh3pbRbz3lA",
"Harith":'https://www.nicehash.com/my/mining/rigs/0-uvxX6MUGk1265e6g6mdo2Q',
"Bocah":'https://www.nicehash.com/my/mining/rigs/0-hp4pZlSfKViq5mqKJvTx4A', 
"Imam":'https://www.nicehash.com/my/mining/rigs/0-r+uWIja1JlaEi2FO4lmyNQ',
"Jai":'https://www.nicehash.com/my/mining/rigs/0-8RTx0tRORl6BnV2tqWdIKA',
#"Mika":'https://www.nicehash.com/my/mining/rigs/0-G4m7LPA291G8d3KOZHYAEg',
"Danial":'https://www.nicehash.com/my/mining/rigs/0-OU6rBCuv3lKrF8POu5tcyg',
"Mija":'https://www.nicehash.com/my/mining/rigs/0-oDjL8Wuxhly94FhJYO6akA',
"Qidds":'https://www.nicehash.com/my/mining/rigs/0-nP5nfUi5fFGZZ1thfIqaOw',
"Aqil":'https://www.nicehash.com/my/mining/rigs/0-EBRHlXtZvleXVAoF8QZ6sg'}

extraction_function(links)