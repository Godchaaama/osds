import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import  By
import time
import regex as re

#Contain links and output

data  =pd.DataFrame({'name:': [],
                    'birth': [],
                    'death': [],
                    'nationality':[]
                    })

all_links = []
file_name = "Crawl_data_hogiathanh_2286400029.xlsx"
#get chrome
for i in range(65, 91):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    driver.get(url)
    try:
        time.sleep(4)
        ul_tags = driver.find_elements(By.TAG_NAME, 'ul')
        ul_painters = ul_tags[20]
        li_tags = driver.find_elements(By.TAG_NAME, 'li')
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)

    except:
        print('Error!')

    driver.quit()

#get painter info
count = 0
for link in all_links:
    print(link)
    try: 
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(4)

        #get name
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            name = ""


        #get dob
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]
        except:
            birth = ""


        #get death

        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except:
            death = ""

        #get Nationality

        try:
            nationality  = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
        except:
            nationality = ""

        
        painter = {'name:': name,
                    'birth': birth,
                    'death': death,
                    'nationality': nationality
                    }
        
        painter_df = pd.DataFrame([painter])
        data = pd.concat([data, painter_df], ignore_index= True)
        driver.quit()
    except:
        print("Error!!")

data.to_excel(file_name)  
print('Successful')      

