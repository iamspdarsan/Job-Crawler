from datetime import datetime
import mysql.connector as sql
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
import selenium


def getdatetime():
    return datetime.now().strftime('%d:%m:%Y - %I:%M:%S:%p')


def logwriter(log):
    with open('..//logs//naukri_log.txt','a') as logfile:
        logfile.writelines(f"{log} | {getdatetime()}\n")


def linkupdate(link,page):
    fpos = link.find('-jobs?')
    link1 = link[:fpos+5]
    link2 = link[fpos+5:]
    newlink = f"{link1}-{str(page)}{link2}"
    return newlink


def naukri_spider(link,file,scrapcount=False):
    opt = Options()
    opt.add_experimental_option("excludeSwitches", ["enable-logging"])
    opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    opt.add_argument("--window-size=1366,768")
    opt.add_argument("--headless")

    #driver = Chrome(service=Service(ChromeDriverManager().install()),options=opt)
    driver = Chrome()
    driver.get(link)

    sec = 10 #wait sec in waitdriver

    db = {
        'title':[],
        'company':[],
        'skills':[],
        'jd':[],
        'link':[],
        'salary':[],
        'salary_range':[],
        'exp':[],
        'min_exp':[],
        'location':[],
        'ptime':[],
        'htime':[],
        'time(real)':[]
        }

    jobs=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/section[2]/div[1]/div[1]/span').text
    fp=jobs.find('of ')
    jobscount = int(jobs[fp+len('of '):])
    logwriter(f"Overall jobs count: {jobscount}")

    jobcap = 0 #captured job init
    jobcard = 1 #job card index 1-20
    page = 2
    if scrapcount:
        itrcount = scrapcount+1
    else:
        itrcount = jobscount+1
    try:
        for i in tqdm(range(1,itrcount),"Crawling"):
            if jobcard == 21: #jobcard reached max
                driver.get(linkupdate(link,page)) #next page switching
                page += 1 #index to switch next page
                jobcard = 1 #job card reset
            
            #Extracting job link
            linkxpath = f"//div[@class='list']/article[{str(jobcard)}]/div/div/a"
            try:link = driver.find_element(By.XPATH,linkxpath).get_attribute("href")
            except:
                link = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,linkxpath)))
                try:link = link.get_attribute("href")
                except:
                    logwriter(f"Link not scrapped in page {page}: jobcard {jobcard}")
                    link = 'null'
            """ if link in db['link']:
                continue """
            #Extracting job role
            rolexpath = f"//div[@class='list']/article[{str(jobcard)}]/div/div/a"
            try:role= driver.find_element(By.XPATH,rolexpath).text
            except:
                role = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,rolexpath)))
                try:role= role.text
                except:
                    logwriter(f"Role not scrapped in page {page}: jobcard {jobcard}")
                    role = 'null'
            
            #Extracting Company name
            cnamexpath = f"//div[@class='list']/article[{str(jobcard)}]/div/div/div/a"
            try:cname= driver.find_element(By.XPATH,cnamexpath).text
            except:
                cname = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,cnamexpath)))
                try:cname = cname.text
                except:
                    logwriter(f"Cname not scrapped in page {page}: jobcard {jobcard}")
                    cname = 'null'

            #Extracting experience
            try:exp= driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/div/ul/li[@class='fleft br2 placeHolderLi experience']/span[@class='ellipsis fleft expwdth']").text
            except:
                logwriter(f"Exp not scrapped in page {page}: jobcard {jobcard}")
                exp='null'

            #Extracting salary
            try:salary= driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/div/ul/li[@class='fleft br2 placeHolderLi salary']/span[@class='ellipsis fleft ']").text
            except:
                logwriter(f"Salary not scrapped in page {page}: jobcard {jobcard}")
                salary='null'
            db['salary_range'].append(salary)
            if 'Not disclosed' in salary:
                salary = '0'
            elif ' -' in salary:
                salary = salary[:salary.find(' -')]
                salary = salary.replace(',','')  

            #Extracting location
            try:location= driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/div/ul/li[@class='fleft br2 placeHolderLi location']/span[@class='ellipsis fleft locWdth']").text
            except:
                logwriter(f"Location not scrapped in page {page}: jobcard {jobcard}")
                location = "null"
            
            #Extracting skills
            try:skil_1 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li").text 
            except:
                logwriter(f"Skill1 not scrapped in page {page}: jobcard {jobcard}")
                skil_1='null'
            
            try:skil_2 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li[2]").text
            except:
                logwriter(f"Skill2 not scrapped in page {page}: jobcard {jobcard}")
                skil_2='null'
            
            try:skil_3 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li[3]").text
            except:
                logwriter(f"Skill3 not scrapped in page {page}: jobcard {jobcard}")
                skil_3='null'
            
            try:skil_4 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li[4]").text 
            except:
                logwriter(f"Skill4 not scrapped in page {page}: jobcard {jobcard}")
                skil_4='null'
            
            try:skil_5 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li[5]").text
            except:
                logwriter(f"Skill5 not scrapped in page {page}: jobcard {jobcard}")
                skil_5='null'
            
            try:skil_6 = driver.find_element(By.XPATH,f"//div[@class='list']/article[{str(jobcard)}]/ul/li[6]").text
            except:
                logwriter(f"Skill6 not scrapped in page {page}: jobcard {jobcard}")
                skil_6='null'
            
            #Combining skills
            skills = f'{skil_1}, {skil_2}, {skil_3}, {skil_4}, {skil_5}, {skil_6}'

            #Extracting Job desc
            jdxpath = f"//div[@class='list']/article[{str(jobcard)}]/div[2]"
            try:jd = driver.find_element(By.XPATH,jdxpath).text
            except:
                jd = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,jdxpath)))
                try:jd = jd.text
                except:
                    logwriter(f"JD not scrapped in page {page}: jobcard {jobcard}")
                    jd = 'null'
            
            #Extracting posted time
            ptimexpath = f"//div[@class='list']/article[{str(jobcard)}]/div[3]/div[1]/div/span"
            try:ptime = driver.find_element(By.XPATH,ptimexpath).text
            except:
                ptime = WebDriverWait(driver,sec).until(EC.presence_of_element_located((By.XPATH,ptimexpath)))
                try:ptime = ptime.text
                except:
                    logwriter(f"Ptime not scrapped in page {page}: jobcard {jobcard}")
                    ptime = 'null'
            
            db['time(real)'].append(ptime) #Real time ref
            
            if ptime == 'Just Now':
                ptime = int(time.time()) #current time

            elif 'Few' in ptime: #few hours ago
                ptime = int(time.time())-7200 #2hours subtract from now

            elif 'Today' in ptime:#today
                ptime = int(time.time())-43200 #half day subtract from now

            else:
                ptime = ptime[:ptime.find(' Day')] #extracting num of days from string 
                try:ptime = int(time.time())-int(ptime)*24*60*60 #subtracting days from now
                except ValueError: #30+ days error / (+) plus sign error
                    try:ptime=int(time.time())-int(ptime[:-1])*24*60*60 #removing + sign and subtract days from now
                    except:ptime='null' #otherswise it will null
            
            db['title'].append(role)
            db['company'].append(cname)
            db['exp'].append(exp)
            min_exp=exp[:exp.find('-')]
            db['min_exp'].append(min_exp)
            db['salary'].append(salary)
            db['location'].append(location)
            db['skills'].append(skills)
            db['jd'].append(jd)
            db['link'].append(link)
            try:htime = datetime.fromtimestamp(ptime).strftime("%Y-%m-%d %H:%M:%S")
            except:pass
            db['htime'].append(htime)
            db['ptime'].append(ptime)
            jobcap +=1
            jobcard+=1

    except Exception as e:
       logwriter(traceback.format_exc())

    logwriter(f"{jobcap} jobs are scraped")
    df = pd.DataFrame(db)
    df.to_csv(file)


def migrate_to_sql_naukri(file):
    #import data
    naukri_df = pd.read_csv(file)
    logwriter(f"Total rows in DF : {len(naukri_df)}")

    #remove duplicates and null vals rows
    naukri_df = naukri_df.drop_duplicates(subset=['link'],keep='first')
    naukri_df = naukri_df.dropna()
    logwriter(f"After removing na's : {len(naukri_df)}")

    #connecting mysql server
    db = sql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'mysql',
        database = 'jobraid',
    )

    #cursur for query operation
    cur = db.cursor()

    #resetting ai val
    cur.execute("ALTER TABLE jobs AUTO_INCREMENT = 1")
    db.commit()

    #insert all DF-rows to mysql database
    logwriter("Starting to insert rows into DB")
    for index in naukri_df.index:
        qry = "INSERT INTO jobs(title, company, skills, jd, link, salary, exp, min_exp, location, ptime, htime , salary_range) VALUES\
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:salary = int(naukri_df['salary'][index])
        except:salary = 0
        val =(naukri_df['title'][index],naukri_df['company'][index],naukri_df['skills'][index],naukri_df['jd'][index],naukri_df['link'][index],salary,naukri_df['exp'][index],int(naukri_df['min_exp'][index]),naukri_df['location'][index],int(naukri_df['ptime'][index]),naukri_df['htime'][index],naukri_df['salary_range'][index])
        try:cur.execute(qry,val)
        except:logwriter(f"Error at inserting index: {index} \n{traceback.format_exc()}\n")
        db.commit()
    #apply changes to database and close the connection
    db.close()
    logwriter(f"All rows were inserted\n")

def truncate_tab(table):
    #connecting mysql server
    db = sql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'mysql',
        database = 'jobraid',
    )

    #cursur for query operation
    cur = db.cursor()
    cur.execute(f"TRUNCATE TABLE {table}")
    db.commit()
