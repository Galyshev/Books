import re

from sqlalchemy.sql import text as sa_text
from bd.alchemy import db_session
import requests
from bs4 import BeautifulSoup
from bd import model_bd
def parser_add(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.findAll("div", {"id": "main"})
    for row in content:
        id_book = link.split("/")[-1]

        author = soup.find("a", {'href': re.compile('\/a/[0-9]+')})
        if author != None:
            author = soup.find("a", {'href':re.compile('\/a/[0-9]+')}).text
            id_author = soup.find("a", {'href':re.compile('\/a/[0-9]+')})['href'].split('/')[-1]
        else:
            author = 'без автора'
            id_author = "00000000000"

        serie = soup.find("a", {'href': re.compile('\/s/[0-9]+')})
        if serie !=None:
            serie = soup.find("a", {'href':re.compile('\/s/[0-9]+')}).text
            id_serie = soup.find("a", {'href': re.compile('\/s/[0-9]+')})['href'].split('/')[-1]
        else:
            serie = 'без серії'
            id_serie = "000000000000"

        title = soup.find("img", {'src': re.compile('\/img/zn*')}).next.strip()
        print(title)
        # print(id_author)
        print('//////////////////////////////////////////////////////////')


    rez = {"a": "11"}
    return rez



parser_add('https://flibusta.is/b/744170')
parser_add('https://flibusta.is/b/744163')
parser_add('https://flibusta.is/b/743121')
parser_add('https://flibusta.is/b/742199')