import re
import requests
from bs4 import BeautifulSoup
from sql import my_sql

def parser_add(link, status, interest):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(link, headers=headers)
    except:
        dic_rez = 'error'
        return dic_rez
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
        if serie != None:
            serie = soup.find("a", {'href':re.compile('\/s/[0-9]+')}).text
            id_serie = soup.find("a", {'href': re.compile('\/s/[0-9]+')})['href'].split('/')[-1]
        else:
            serie = 'без серії'
            id_serie = "000000000000"

        title = soup.find("img", {'src': re.compile('\/img/zn*')}).next.strip()

        genres = soup.findAll("a", {'href': re.compile('\/g/[0-9]+')})

        ls_genres = []
        for g in genres:
            id_genre = g['href'].split('/')[-1]
            ls_genres.append(id_genre)
            genre = g.text
            ls_genres.append(genre)

        date_update = soup.find("div", {"class": "fb2info-content"}).next.next
        if date_update != None:
            date_update = date_update.split(":")[-1].strip()
        else:
            date_update = 'no_date'

        cover = soup.find("img", {'src': re.compile('\/i/+')})['src']
        cover = 'https://flibusta.is/' + cover

        tmp_content = soup.find("h2").find_next_siblings("p")
        try:
            for i in tmp_content:
                info = i.text.strip()
        except:
            info = 'без аннотации'

        my_sql.add_to_base(id_book, author, id_author, serie, id_serie, title, ls_genres, date_update, cover, info, link, status, interest)
        rez = {'title': title, 'cover': cover}
        return rez




# parser_add('https://flibusta.is/b/744170')
# parser_add('https://flibusta.is/b/744163')
# parser_add('https://flibusta.is/b/743121')
# parser_add('https://flibusta.is/b/742199')

# parser_add('http://flibusta.is/b/744170')