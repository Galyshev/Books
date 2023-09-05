import re
import requests
from bs4 import BeautifulSoup
from sql import my_sql

def new_books():
    link = 'https://flibusta.is/new'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find("div", {"id": "main"}).findAll("div")
    like_genres = ['/g/81', '/g/166', '/g/2', '/g/4', '/g/124', '/g/5', '/g/7', '/g/253', '/g/254', '/g/226', '/g/11', '/g/230', '/g/3']
    new_sorted_books = []
    for line in content:
        genres = line.findAll("a", {'href': re.compile('\/g/[0-9]+')})
        id_book = 'NO'
        for g in genres:
            if g['href'] in like_genres:
                id_book = line.find("a", {'href': re.compile('\/b/[0-9]+')})['href']
        if id_book != 'NO':
            chk_books = my_sql.check_books(id_book)
            if len(chk_books) == 0:
                new_sorted_books.append(id_book)
                # my_sql.add_to_new_books_base(id_book)
    rez = []
    for id in new_sorted_books:
        link = 'https://flibusta.is' + id
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        cover = soup.find("img", {'src': re.compile('\/i/+')})['src']
        cover = 'https://flibusta.is/' + cover
        tmp_dic = {'link': link, 'cover': cover}
        rez.append(tmp_dic)
    return rez

def parser_new_book(link, status, interest):
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
        cover = 'https://flibusta.is' + cover

        tmp_content = soup.find("h2").find_next_siblings("p")
        try:
            for i in tmp_content:
                info = i.text.strip()
        except:
            info = 'без аннотации'

        chk_serie = my_sql.check_serie(id_serie)
        if chk_serie == 'Не знайдено':
            interest = 'No'
        else:
            interest = 'Yes'
        rez = {'title': title, 'cover': cover, 'serie': serie, 'autor': author, 'annot': info, 'book_title': title, 'status': 'status', 'interest': interest, 'genre': ls_genres}
        return rez

# new_books()
