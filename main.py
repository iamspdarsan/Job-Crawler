import spiders.foundit as foundit
import spiders.naukri as naukri
import spiders.indspi as indeed
import spiders.wnomads as wnomad


file1 = "naukri_db.csv"
java = 'https://www.naukri.com/java-jobs?k=java&nignbevent_src=jobsearchDeskGNB'
php = 'https://www.naukri.com/php-jobs?k=php&nignbevent_src=jobsearchDeskGNB'
go = 'https://www.naukri.com/go-jobs?k=go&nignbevent_src=jobsearchDeskGNB'
cs = 'https://www.naukri.com/c-sharp-jobs?k=c%23&nignbevent_src=jobsearchDeskGNB'
python = 'https://www.naukri.com/python-jobs?k=python&nignbevent_src=jobsearchDeskGNB'
cpp = 'https://www.naukri.com/c-plus-plus-jobs?k=c%2B%2B&nignbevent_src=jobsearchDeskGNB'
js = 'https://www.naukri.com/javascript-jobs?k=javascript&nignbevent_src=jobsearchDeskGNB'
ruby = 'https://www.naukri.com/ruby-jobs?k=ruby&nignbevent_src=jobsearchDeskGNB'
se = 'https://www.naukri.com/software-jobs?k=software&nignbevent_src=jobsearchDeskGNB'
fr = 'https://www.naukri.com/fresher-jobs?k=fresher&nignbevent_src=jobsearchDeskGNB'
web = 'https://www.naukri.com/web-jobs?k=web&nignbevent_src=jobsearchDeskGNB'
andr = 'https://www.naukri.com/android-jobs?k=android&nignbevent_src=jobsearchDeskGNB'
ios = 'https://www.naukri.com/ios-jobs?k=ios&nignbevent_src=jobsearchDeskGNB'
tester = 'https://www.naukri.com/tester-jobs?k=tester&nignbevent_src=jobsearchDeskGNB'
links = [java,php,go,cs,python,cpp,js,ruby,se,fr,web,andr,ios,tester]
#links = [web]
#truncate
naukri.truncate_tab('jobs')

try:
    for link in links:
        #starting spider
        naukri.naukri_spider(link,file1)

        #migrate data to mysql database
        naukri.migrate_to_sql_naukri(file1)
except Exception as e:
    print(e)