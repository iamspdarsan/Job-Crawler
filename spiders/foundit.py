from datetime import datetime
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import traceback
from webdriver_manager.chrome import ChromeDriverManager



opt = Options()
opt.add_experimental_option("excludeSwitches", ["enable-logging"])
opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
#opt.add_argument("--window-size=1366,768")
#opt.add_argument("--headless")

driver = Chrome(service=Service(ChromeDriverManager().install()),options=opt)
driver.get('https://www.foundit.in/srp/results?query=python&searchId=4d9adb0c-3675-4f8f-ad29-fcaff6e98c22')

db = {
    'role':[],
    'cname':[],
    'exp':[],
    'salary':[],
    'location':[],
    'skills':[],
    'jd':[],
    'link':[],
    'datetime':[],
    'time(real)':[],
    }

jobs=driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[5]/div[1]/div/div[1]/div/section/div/p').text
fp=jobs.find('Showing ')+len('Showing ')
lp = jobs.find(' results')
jobscount = int(jobs[fp:lp])

sec = 5
try:
    for i in tqdm(range(1,jobscount+1),"Crawling"):        
        #Extracting job role
        rolexpath = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[1]/div/div[1]"
        try:role= driver.find_element(By.XPATH,rolexpath).text
        except:
            try:role= WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,rolexpath))).text
            except:role = 'null'
        print(role)
        
        #Extracting Company name
        cnamexpath = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/p"
        try:cname= driver.find_element(By.XPATH,cnamexpath).text
        except:
            try:cname = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,cnamexpath))).text
            except:cname = 'null'
        print(cname)

        exppath='/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]'
        #Extracting experience
        try:exp= driver.find_element(By.XPATH,exppath).text
        except:
            try:exp = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,exppath)))
            except:exp='null'
        print(exp)

        salarypath='/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[4]/div[2]'
        #Extracting salary
        try:salary= driver.find_element(By.XPATH,salarypath).text
        except:
            try:WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,salarypath))).text
            except:salary='null'
        print(salary)
        
        #Extracting location
        locxpath = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]"
        try:location= driver.find_element(By.XPATH,locxpath).text
        except:
            try:WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,locxpath))).text
            except:location = "null"
        print(location)
        
        skill1path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]"
        #Extracting skills
        try:skil_1 = driver.find_element(By.XPATH,skill1path).text 
        except:
            try:skil_1 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill1path)))
            except:skil_1='null'
        print(skil_1)
        
        skill2path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[2]/div"
        #Extracting skills
        try:skil_2 = driver.find_element(By.XPATH,skill2path).text 
        except:
            try:skil_2 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill2path)))
            except:skil_2='null'
        print(skil_2)
        
        skill3path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[3]/div"
        #Extracting skills
        try:skil_3 = driver.find_element(By.XPATH,skill3path).text 
        except:
            try:skil_3 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill3path)))
            except:skil_3='null'
        print(skil_3)
        
        skill4path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[4]/div"
        #Extracting skills
        try:skil_4 = driver.find_element(By.XPATH,skill4path).text 
        except:
            try:skil_4 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill4path)))
            except:skil_4='null'
        print(skil_4)
        
        skill5path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[5]/div"
        #Extracting skills
        try:skil_5 = driver.find_element(By.XPATH,skill5path).text 
        except:
            try:skil_5 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill5path)))
            except:skil_5='null'
        print(skil_5)
        
        skill6path = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[6]/div"
        #Extracting skills
        try:skil_6 = driver.find_element(By.XPATH,skill6path).text 
        except:
            try:skil_6 =WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,skill6path)))
            except:skil_6='null'
        print(skil_6)
        
        #Combining skills
        skills = f'{skil_1}, {skil_2}, {skil_3}, {skil_4}, {skil_5}, {skil_6}'


        """#Extracting job link
            linkxpath = f"//div[@class='list']/article[{str(jobcard)}]/div/div/a"
            try:link = driver.find_element(By.XPATH,linkxpath).get_attribute("href")
            except:
                link = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,linkxpath)))
                try:link = link.get_attribute("href")
                except:link = 'null'"""
    
        #Extracting posted time
        ptimexpath = f"/html/body/div[2]/div[1]/div[5]/div[1]/div/div[2]/div/div/div[2]/div[5]/div[2]/div[6]/div"
        try:ptime = driver.find_element(By.XPATH,ptimexpath).text
        except:
            try:ptime = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,ptimexpath))).text
            except:ptime = 'null'
        print(ptime)
        

except Exception as e:
    print("errror")