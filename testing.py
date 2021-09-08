import requests, re, datetime, mysql.connector
from bs4 import BeautifulSoup

r = requests.get('https://www.geeksforgeeks.org/')
c = r.content
parsed_content = BeautifulSoup(c,"html.parser")
#meta_list  = parsed_content.find_all("meta")
#title = parsed_content.find(".//title").string
title = parsed_content.find("title").text
print(title)