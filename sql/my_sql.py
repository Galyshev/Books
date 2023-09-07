from bd.alchemy import db_session
from bd.model_bd import Content, Serie, Author, Genre, Info, New_books
from datetime import date

def add_to_base(id_book, author, id_author, serie, id_serie, title, genres, date_update, cover, info,
                  link, status, interest):

    genre = '/'.join(genres)
    tmp = db_session.query(Content).filter(Content.id_book == id_book).all()
    if len(tmp) == 0:
        cont_add = Content(id_book=id_book, id_author=id_author, title=title, genre=genre, status=status,
                           date_update=date_update, link=link, cover=cover, id_serie=id_serie)
        db_session.add(cont_add)
        db_session.commit()

        annot = Info(id_book=id_book, info=info)
        db_session.add(annot)
        db_session.commit()

    tmp = db_session.query(Serie).filter(Serie.id_serie == id_serie).all()
    if len(tmp) == 0:
        serie_add = Serie(id_serie=id_serie, serie=serie, interesting=interest)
        db_session.add(serie_add)
        db_session.commit()

    tmp = db_session.query(Author).filter(Author.id_author == id_author).all()
    if len(tmp) == 0:
        author_add = Author(id_author=id_author, author=author)
        db_session.add(author_add)
        db_session.commit()

    for i in range(0, len(genres), 2):
        id_genre = genres[i]
        genre = genres[i+1]
        tmp = db_session.query(Genre).filter(Genre.id_genre == id_genre).all()
        if len(tmp) == 0:
            genre_add = Genre(genre=genre, id_genre=id_genre)
            db_session.add(genre_add)
            db_session.commit()

def search_by_author(txt):
    search = "%{}%".format(txt)
    authors = Author.query.filter(Author.author.like(search)).all()
    rez = {}
    if len(authors) != 0:
        for i in authors:
            id_author = i.id_author
            author = i.author
            rez[id_author] = author
    else:
        return 'Не знайдено'
    return rez

def boks_by_author(id_author):
    books = Content.query.filter(Content.id_author == id_author ).all()
    rez = []
    if len(books) != 0:
        for i in books:
            rez.append(i)
    else:
        return 'Не знайдено'

    return rez

def search_by_series(txt):
    search = "%{}%".format(txt)
    series = Serie.query.filter(Serie.serie.like(search)).all()
    rez = {}
    if len(series) != 0:
        for i in series:
            id_serie = i.id_serie
            serie = i.serie
            rez[id_serie] = serie
    else:
        return 'Не знайдено'
    return rez

def boks_by_series(id_serie):
    books = Content.query.filter(Content.id_serie == id_serie).all()
    rez = []
    if len(books) != 0:
        for i in books:
            rez.append(i)
    else:
        return 'Не знайдено'

    return rez

def book_by_books(txt):
    search = "%{}%".format(txt)
    books = Content.query.filter(Content.title.like(search)).all()
    return books

def detail_books(txt):
    # (id_book, author, id_author, serie, id_serie, title, genres, date_update, cover, info,
    #  link, status, interest):
    rez = {}
    books = Content.query.filter(Content.id_book == txt).all()
    rez['books'] = books
    for i in books:
        id_book = i.id_book
        id_serie= i.id_serie
        id_author = i.id_author
        genres = str(i.genre).split('/')
        genre = ''
        for g in range(1, len(genres), 2):
            genre = genre + ' / ' + genres[g]
        genre = genre.strip()
        rez['genre'] = genre
        title = i.title
        rez['title'] = title
        cover = i.cover
        rez['cover'] = cover
        status = i.status
        rez['status'] = status

        series = Serie.query.filter(Serie.id_serie == id_serie).all()
        for tmp in series:
            serie = tmp.serie
            rez['serie'] = serie
            interest = tmp.interesting
            rez['interest'] = interest
        autors = Author.query.filter(Author.id_author == id_author).all()
        for tmp in autors:
            author = tmp.author
            rez['autor'] = author
        annots = Info.query.filter(Info.id_book == id_book).all()
        for tmp in annots:
            annot = tmp.info
            rez['annot'] = annot

    return rez

def check_books(id_book):
    books = New_books.query.filter(New_books.id_book == id_book).all()
    return books
def add_to_new_books_base(id_book):
    today = date.today()
    cont_add = New_books(id_book=id_book, date_update=today)
    db_session.add(cont_add)
    db_session.commit()

def check_serie(id_serie):
    books = Content.query.filter(Content.id_serie == id_serie).all()
    rez = []
    if len(books) != 0:
        for i in books:
            rez.append(i)
    else:
        return 'Не знайдено'

    return rez

def check_book_from_date(date):
    books = New_books.query.filter(New_books.date_update == date).all()
    rez = []
    if len(books) != 0:
        for i in books:
            rez.append(i.id_book)
    else:
        return 'Не знайдено'

    return rez