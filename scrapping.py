import sys
import os
from time import sleep
import requests, re, datetime, mysql.connector
from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

#scheduler = BackgroundScheduler()
jobStore = {
    "default": SQLAlchemyJobStore(url='mysql+pymysql://scrapper:scrappy@localhost:3306/webpage_data?charset=utf8')
}

#scheduler = BackgroundScheduler({
#     'apscheduler.jobstores.default': {
#         'type': 'sqlalchemy',
#         'url': 'mysql://scrapper:scrappy@localhost:3306/webpage_data?charset=utf8'
#         #'url': 'mysql://scrapper:scrappy@localhost:3306/scrapper_jobs?charset=utf8'
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
#Attributes = ['description','Description','keywords','keyword','Keywords','Keyword']
Attributes = ['description','Description']

parsedLinks = []

def parseLink(URL):
    print("stating the program....")
    r = requests.get(URL)
    print('[{}]: {} - {}'.format(datetime.datetime.now(), r.status_code, URL))
    if r.status_code == 200:
        parsedLinks.append(URL)
        collected_data = []
        collected_data.append(URL)
        #add_to_db('webpages', URL)

        c = r.content
        parsed_content = BeautifulSoup(c,"html.parser")
        meta_list  = parsed_content.find_all("meta")
        title = parsed_content.find("title").text
        collected_data.append(title)
        #print(title)

        for meta in meta_list:
            if 'name' in meta.attrs:
                name = meta.attrs['name']
                #New database logic
                #collected_data = []
                #collected_data.append(meta.attrs['content'])
                #if name == 'keyword' or 'Keyword' or 'Keywords' or 'keywords':        
                       #add_to_db('Keywords', collected_data)
                #       db_where_condition(URL,'Keywords', collected_data)
                #       collected_data.clear()
                #elif name == 'Description' or 'description':
                       #add_to_db('Description', collected_data)
                #       db_where_condition(URL,'Description', collected_data)
                #       collected_data.clear()
                if name in Attributes:
                    #Extracting description and keywords from meta tags and adding to database  
                    if len(meta.attrs['content']) >= 1:
                        #collected_data = []
                        collected_data.append(meta.attrs['content'])
                        
                        #Storing collected link and data to database
                        add_to_db(collected_data[0], collected_data[1], collected_data[2])
                        collected_data.clear()
                    else:
                        print('could not find all required attributes for URl')

        linkArray = parsed_content.find_all('a', attrs = {'href': re.compile("^https://")})

        for idx, link in enumerate(linkArray):
            if link.get('href') and link.get('href') not in parsedLinks:
                nextExecTime = datetime.datetime.now() + datetime.timedelta(0, 3 * (idx+1))
                # print('Next execution: {} - {}'.format(nextExecTime, link.get('href')))
                #scheduler.add_job(parseLink, nextExecTime, [link.get('href')])
                scheduler.add_job(parseLink, run_date = nextExecTime, args = [link.get('href')])
    else:
        nextExecTime = datetime.datetime.now() + datetime.timedelta(0, 60)
        # print('Next execution: {} - {}'.format(nextExecTime, link.get('href')))
        # scheduler.add_job(parseLink, nextExecTime, [URL])
        scheduler.add_job(parseLink, run_date = nextExecTime, args = [URL])


def add_to_db(link, title, description):
    sql = "INSERT INTO collected_links (webpages, Title, Description) VALUES (%s, %s, %s)"
    val = (link, title, description)
    cursor.execute(sql, val)

#def add_to_db(column_name, data):
#    sql = "INSERT INTO collected_links ({}) values (%s)".format(column_name)
#    val = (data)
#    cursor.execute(sql, val)

#def db_where_condition(link,column,data):
#    sql = "INSERT INTO collected_links ({}) values (%s) WHERE 'webpage' = {}'".format(column,link)
#    val = (data)
#    cursor.execute(sql, val)


if __name__ == '__main__':
    try:
        #print("Just after try block.......")
        if len(scheduler.get_jobs()) == 0:
            print("Try block execution...") #This print statement not working 
            parseLink('https://www.geeksforgeeks.org/')

        while True:
            sleep(2)
            if len(scheduler.get_jobs()) == 0:
                break
            #print("In Try block....")
    except Exception as e:
        print("Try block did not worked....",e)
        scheduler.shutdown()
        # mydb.commit()
