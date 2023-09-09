import time
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


db = {
        'title':[],
        'company':[],
        'salary':[],
        'location':[],
        'jd':[],
        'link':[],
        'htime':[],
        'ptime':[],
    }

#Custom option
opt = Options()
opt.add_experimental_option("excludeSwitches",["enable-logging"])
opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
opt.add_argument("--window-size=1366,768")
""" opt.add_argument("--headless") """

driver = Chrome(service=Service(ChromeDriverManager().install()),options=opt)
link = "https://in.indeed.com/Tirupur-jobs-in-Tamil-Nadu"
driver.get(link)
driver.save_screenshot('ss.jpeg')
#jobcard index
jobcard=1
#seconds for waitdriver
waitsec = 5
#extented sleep sec to wait
sleepsec = 0
#page index
thres = 0

try:
    for j in tqdm(range(100)):
        
        #only by 17 index is there in a page
        if jobcard == 18:
            #incrementing page for nextbtn time
            thres += 10
            #reset jobcard index for another page
            jobcard=1
            #different nextbtn button for different page
            curl = driver.current_url
            driver.get(curl+f"&start={thres}")

        if jobcard == 6 or jobcard == 12: #6 and 12 is undefined index element
            #incrementing to skip this page
            jobcard += 1 
        jobcard = str(jobcard)
    
        titlepath= f'//*[@id="mosaic-provider-jobcards"]/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/a/span'
        try:title = driver.find_element(By.XPATH,titlepath).text
        except:
            try:
                title = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,titlepath))).text
            except:
                time.sleep(sleepsec)
                title = driver.find_element(By.XPATH,titlepath).text
        print(f'{title}-title')

        cnamepath =f'//*[@id="mosaic-provider-jobcards"]/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/span[1]/a'
        try:cname = driver.find_element(By.XPATH,cnamepath).text
        except:
            try:cname = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,cnamepath))).text
            except:
                time.sleep(sleepsec)
                cname = driver.find_element(By.XPATH,cnamepath).text

        """ print(f'{cname}-cname') """

        locationpath = f"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div"
        try:location = driver.find_element(By.XPATH,locationpath).text
        except:
            try:location = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,locationpath))).text
            except:location = 'null'
        """ print(f'{location}-location') """

        salxpath = f"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[3]/div[1]/div"
        try:salary = driver.find_element(By.XPATH,salxpath).text
        except: 
            try:salary= WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,salxpath))).text
            except:salary ='null'

        if salary != 'null':
            
            if 'a month' in salary:#₹15,000 - ₹25,000 a month
                #removing INR sign
                salary = salary.replace('₹','')
                #extracting salary range
                salary = salary[:salary.find(' a')]

            elif 'Up to' in salary:#'Up to ₹9,97,280 a year'
                salary = salary[salary.find('₹')+1:]
                salary = salary[:salary.find(' a')]
        
        print(f'{salary}-salary')

        jdpath_1 = f"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div/div/ul/li[1]"
        try:jd = driver.find_element(By.XPATH,jdpath_1).text
        except:
            try:jd = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,jdpath_1))).text
            except:jd='null'
        """ print(f'{jd}-jd') """


        jdpath_2 = f"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div/div/ul/li[2]"
        try:jd_2 = driver.find_element(By.XPATH,jdpath_2).text
        except:
            try:jd_2 = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,jdpath_2))).text
            except:jd_2="null" 
        """ print(f'{jd_2}-jd_2') """

        linkpath = f"/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/a"
        try:link = driver.find_element(By.XPATH,linkpath).get_attribute("href")
        except:
            try:link = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,jdpath_2))).get_attribute("href")
            except:link = 'null'
        """ print(f'{link}-link') """

        htpath = f'//*[@id="mosaic-provider-jobcards"]/ul/li[{jobcard}]/div/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div/span'
        try:htime = driver.find_element(By.XPATH,htpath).text
        except:
            try:htime = WebDriverWait(driver,waitsec).until(EC.presence_of_element_located((By.XPATH,htpath))).text
            except:htime = 'null'
        print(f'{htime}-posted time')

        jobcard= int(jobcard)+1

        db['title'].append(title)
        db['company'].append(cname)
        db['salary'].append(salary)
        db['location'].append(location)
        db['jd'].append(f"{jd}, {jd_2}")
        db['link'].append(link)
        db['htime'].append(htime)
        ptime = htime
        db['ptime'].append(ptime)
except:
    print(traceback.print_exc())

df = pd.DataFrame(db)
df.to_csv('indeed_db.csv')
