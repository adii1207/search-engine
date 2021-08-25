
import requests, re, time, sqlite3
from bs4 import BeautifulSoup
from justbackoff import Backoff


def crawling_indexing(URL):
    Attributes = ['description','Description','keywords','keyword','Keywords','Keyword']
    parsed_links = set()
    #entry = {}
    #collected_data = []
    link_stack = []
    link_stack.append(URL)
    print(link_stack)
    while len(link_stack) != 0:   # traversing all the links
        #try:
        #    r = requests.get(link_stack[0])
        #except Exception as e:
        #    print("could not load page ")
        r = requests.get(link_stack[0])
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
                            add_to_db(link_stack[0], collected_data[0], collected_data[1])
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
                #print(link_stack)
            
            parsed_links.add(link_stack.pop(0))
            #time.sleep(15) # Halting the loop for 15 second

            #for link in parsed_content.find_all('a'):
            #    if (link != None and link != '#') and link not in link_stack:
                #if link.startswith('http') == True or link.startswith('https') == True:
            #        link_stack.append(link.get('href'))
            #        print(link_stack)
        
        elif r.status_code == 429:
            #print("stop the program for 5 minutes......")
            #time.sleep(1800)
            #print("halts the program for :", b.duration(),"seconds")
            #time.sleep(b.duration())
            continue
        else:
            print('could not load page: error {}'.format(r.status_code))


def add_to_db(link, description, keywords):    
    conn = sqlite3.connect('webpage_data')
    cursor = conn.cursor()
    cursor.execute("""INSERT into collected_links(webpages, description, keywords) values (?,?,?)""", (link, description, keywords))
    conn.commit()
    return cursor.execute("""SELECT * from webpage_data""") 


crawling_indexing('https://www.geeksforgeeks.org/')

