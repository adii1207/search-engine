import sys
import os
from time import sleep
import requests, re, datetime, mysql.connector
from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobStore = {
    "default": SQLAlchemyJobStore(url='mysql+pymysql://scrapper:scrappy@localhost:3306/webpage_data?charset=utf8')
}

# scheduler = BackgroundScheduler({
#     'apscheduler.jobstores.default': {
#         'type': 'sqlalchemy',
#         'url': 'mysql://scrapper:scrappy@localhost:3306/scrapper_jobs?charset=utf8'
#     }
# })

scheduler = BackgroundScheduler({
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': 'mysql+pymysql://scrapper:scrappy@localhost:3306/webpage_data?charset=utf8'
    }
})

# scheduler.configure(jobStore=jobStore)
scheduler.start()

mydb = mysql.connector.connect(
  host="localhost",
  user="scrapper",
  password="scrappy",
  database="webpage_data"
)

cursor = mydb.cursor()
Attributes = ['description','Description','keywords','keyword','Keywords','Keyword']

parsedLinks = []

def parseLink(URL):
    r = requests.get(URL)
    print('[{}]: {} - {}'.format(datetime.datetime.now(), r.status_code, URL))
    if r.status_code == 200:
        parsedLinks.append(URL)

        #add_to_db(link, URL)

        c = r.content
        parsed_content = BeautifulSoup(c,"html.parser")
        meta_list  = parsed_content.find_all("meta")

        for meta in meta_list:
            if 'name' in meta.attrs:
                name = meta.attrs['name']
                if name in Attributes:
                    #Extracting description and keywords from meta tags and adding to database 
                        #Extracting description and keywords from meta tags and adding to database 
                    #Extracting description and keywords from meta tags and adding to database 
                        #Extracting description and keywords from meta tags and adding to database 
                    #Extracting description and keywords from meta tags and adding to database 
                    if len(meta.attrs['content']) >= 1:
                        collected_data = []
                        collected_data.append(meta.attrs['content'])
                        
                        #Storing collected link and data to database
                        add_to_db(URL, 'adw', 'Abc')
                        collected_data.clear()
                    else:
                        print('could not find all required attributes for URl')

        linkArray = parsed_content.find_all('a', attrs = {'href': re.compile("^https://")})

        for idx, link in enumerate(linkArray):
            if link.get('href') and link.get('href') not in parsedLinks:
                nextExecTime = datetime.datetime.now() + datetime.timedelta(0, 3 * (idx+1))
                # print('Next execution: {} - {}'.format(nextExecTime, link.get('href')))
                #scheduler.add_job(parseLink, nextExecTime, [link.get('href')])
                scheduler.add_job(parseLink, run_date = nextExecTime, args=[link.get('href')])
    else:
        nextExecTime = datetime.datetime.now() + datetime.timedelta(0, 60)
        # print('Next execution: {} - {}'.format(nextExecTime, link.get('href')))
        # scheduler.add_job(parseLink, nextExecTime, [URL])
        scheduler.add_job(parseLink, run_date=nextExecTime, args=[URL])


def add_to_db(link, description, keywords):
    sql = "INSERT INTO collected_links (webpages, description, keywords) VALUES (%s, %s, %s)"
    val = (link, description, keywords)
    cursor.execute(sql, val)


if __name__ == '__main__':
    try:
        if scheduler.get_jobs() is None:
            parseLink('https://www.geeksforgeeks.org/')

        while True:
            sleep(2)
            if scheduler.get_jobs() is None:
                break
    except:
        scheduler.shutdown()
        # mydb.commit()
