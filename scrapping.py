import sys
import os
import requests, re, time, mysql.connector
from bs4 import BeautifulSoup
from justbackoff import Backoff

mydb = mysql.connector.connect(
  host="localhost",
  user="scrapper",
  password="scrappy",
  database="webpage_data"
)

cursor = mydb.cursor()

def crawling_indexing(URL):
    Attributes = ['description','Description','keywords','keyword','Keywords','Keyword']
    parsed_links = set()
    #entry = {}
    #collected_data = []
    link_stack = []
    link_stack.append(URL)
    while len(link_stack) != 0:   # traversing all the links
        #try:
        #    r = requests.get(link_stack[0])
        #except Exception as e:
        #    print("could not load page ")
        currentUrl = link_stack[0]
        r = requests.get(currentUrl)
        print('{}: {}'.format(r.status_code, currentUrl))
        #b = Backoff(min_ms=300000, max_ms=3600000, factor=2, jitter=False)
        if r.status_code == 200:
            c = r.content
            parsed_content = BeautifulSoup(c,"html.parser")
            meta_list  = parsed_content.find_all("meta")
            for meta in meta_list:
                if 'name' in meta.attrs:
                    name = meta.attrs['name']
                    if name in Attributes:
                        #entry = {}
                        #entry[name.lower()] = meta.attrs['content']
                        #print(entry)
                        #Extracting description and keywords from meta tags and adding to database 
                        if len(meta.attrs['content']) >= 1:
                            collected_data = []
                            collected_data.append(meta.attrs['content'])
                            #Storing collected link and data to database
                            add_to_db(currentUrl, 'adw', 'Abc')
                            collected_data.clear()
                        else:
                            print('could not find all required attributes for URl')
            #if len(entry) >= 1:
            #    if entry not in collected_data:
            #        collected_data.append(entry)
                #print(collected_data)
           #else:
           #    print('could not find all required attributes for URL ')
            
            for link in parsed_content.find_all('a',attrs = {'href': re.compile("^https://")}):
                if link.get('href') not in link_stack and link.get('href') not in parsed_links:
                    link_stack.append(link.get('href'))
            
            parsed_links.add(link_stack.pop(0))
            #time.sleep(15) # Halting the loop for 15 second

            #for link in parsed_content.find_all('a'):
            #    if (link != None and link != '#') and link not in link_stack:
                #if link.startswith('http') == True or link.startswith('https') == True:
            #        link_stack.append(link.get('href'))
            #        print(link_stack)
        
        else:
            link_stack.append(currentUrl)


def add_to_db(link, description, keywords):
    sql = "INSERT INTO collected_links (webpages, description, keywords) VALUES (%s, %s, %s)"
    val = (link, description, keywords)
    cursor.execute(sql, val)


if __name__ == '__main__':
    try:
        crawling_indexing('https://www.geeksforgeeks.org/')
    except KeyboardInterrupt:
        try:
            mydb.commit()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
