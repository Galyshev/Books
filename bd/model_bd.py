from sqlalchemy import Column, Integer, Text
from bd.alchemy import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True)
    id_book = Column(Text)
    id_author = Column(Text)
    id_serie = Column(Text)
    title = Column(Text)
    id_genre = Column(Text)
    status = Column(Text)  # прочитано / не начинал / не понравилось
    date_update = Column(Text)
    link = Column(Text)  # для скачивания
    cover = Column(Text)  # обложка

    def __init__(self, id_book, id_author, title, id_genre, status, date_update, link, cover, id_serie):
        self.id_book = id_book
        self.id_author = id_author
        self.title = title
        self.id_genre = id_genre
        self.status = status
        self.date_update = date_update
        self.link = link
        self.cover = cover
        self.id_serie = id_serie


class Serie(Base):
    __tablename__ = "serie"

    id = Column(Integer, primary_key=True)
    id_serie = Column(Text)
    serie = Column(Text)
    interesting = Column(Text)  # следить / не следить

    def __init__(self, id_serie, serie, interesting):
        self.id_serie = id_serie
        self.serie = serie
        self.interesting = interesting


class Info(Base):
    __tablename__ = "info"

    id = Column(Integer, primary_key=True)
    id_book = Column(Text)
    info = Column(Text)

    def __init__(self, id_book, info):
        self.id_book = id_book
        self.info = info


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    id_author = Column(Text)
    author = Column(Text)

    def __init__(self, id_author, author):
        self.id_author = id_author
        self.author = author


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    genre = Column(Text)
    id_genre = Column(Text)

    def __init__(self, genre, id_genre):
        self.genre = genre
        self.id_genre = id_genre
