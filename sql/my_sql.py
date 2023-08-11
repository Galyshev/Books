from bd.alchemy import db_session
from bd.model_bd import Content, Serie, Author, Genre, Info
from sqlalchemy.sql import text as sa_text

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


# dic_genres = ['2', 'Боевая фантастика', '4', 'Героическая фантастика', '213', 'Самиздат, сетевая литература', '9', 'Ужасы']
# add_to_base(dic_genres)


