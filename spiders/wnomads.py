import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

from webdriver_manager.chrome import ChromeDriverManager

opt = Options()
opt.add_experimental_option("excludeSwitches",["enable-logging"])
""" opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36') """
opt.add_argument("--window-size=1366,768")
""" opt.add_argument("--headless") """
db = {
    'cname':[],
    'role':[],
    'link':[],
    'salary':[],
    'location':[],
    'jd':[],
    'shift':[],
    'skills':[],
    'ptime':[],
   
}
driver = Chrome(service=Service(ChromeDriverManager().install()),options=opt)
driver.get("https://www.workingnomads.com/jobs")
sec = 10
for i in range(1,11):
    
    i = str(i)
    #driver.implicitly_wait(sec)
    rolepath = f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/div[2]/div[2]/div[{i}]/div[2]/h4/a[2]"
    try:role = driver.find_element(By.XPATH,rolepath).text
    except:role = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,rolepath))).text
    print(role)
    
    #driver.implicitly_wait(sec)
    pathx = f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/div[2]/div[2]/div[{i}]/div[2]/h4/a[2]"
    try:path = driver.find_element(By.XPATH,pathx).get_attribute('href')
    except:path = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,pathx))).get_attribute('href')
    print(path)

    #driver.implicitly_wait(sec)
    jd = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]"+
    f"/div[2]/div[2]/div[{i}]/div[2]/div[1]/span[1]").text
    #driver.implicitly_wait(sec)
    salary = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]"+
    f"/div[2]/div[2]/div[{i}]/div[2]/div[1]/div[7]/span").text
    #print(salary)
    #driver.implicitly_wait(sec)
    location = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]"+
    f"/div[2]/div[2]/div[{i}]/div[2]/div[1]/div[4]/span").text
    #print(location)
    #driver.implicitly_wait(sec)
    shift = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/div[2]"+
    f"/div[2]/div[{i}]/div[2]/div[1]/div[5]/span").text
    #print(shift)
    #driver.implicitly_wait(sec)
    skil_1 = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/"+
    f"div[2]/div[2]/div[{i}]/div[2]/div[1]/div[1]/a").text
    #print(skil_1)
    #driver.implicitly_wait(sec)
    skil_2 = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/"+
    f"div[2]/div[2]/div[{i}]/div[2]/div[1]/div[2]/a").text
    #print(skil_2)
    #driver.implicitly_wait(sec)
    skil_3 = driver.find_element(By.XPATH,f"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/"+
    f"div[2]/div[2]/div[{i}]/div[2]/div[1]/div[3]/a").text
    #print(skil_3)
    #driver.implicitly_wait(sec)
    cname = driver.find_element(By.XPATH,"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]/div[2]"+
    f"/div[2]/div[{i}]/div[1]/div").text
    #driver.implicitly_wait(sec)
    ptime = driver.find_element(By.XPATH,"/html/body/div/div[2]/div[1]/div[2]/div[2]/main/section/div[2]"+
    f"/div[2]/div[2]/div[{i}]/div[1]/span").text
    #driver.implicitly_wait(sec)
    skills = f"{skil_1}, {skil_2}, {skil_3}"

    db['cname'].append(cname)
    db['role'].append(role)
    db['skills'].append(skills)
    db['location'].append(location)
    db['shift'].append(shift)
    db['jd'].append(jd)
    db['link'].append(path)
    db['ptime'].append(ptime)
    db['salary'].append(salary)

import pandas as pd
pd.DataFrame(db).to_csv("output.csv")