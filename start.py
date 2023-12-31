import os
from datetime import date
from flask import Flask, render_template, request, redirect, session, url_for
from BS import BS_add, BS_new
from sql import my_sql
import urllib.request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", 'FLSK_SECRET_KEY')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        title = 'Вітання'
        return render_template('index.html', title=title)
    else:
        title = 'Вітання'
        if request.form['button'] == 'add':
            return redirect('/add')
        elif request.form['button'] == 'statistics':
            return render_template('index.html', title=title)
        elif request.form['button'] == 'find':
            return redirect('/find')
        elif request.form['button'] == 'new_for_date':
            return redirect('/new_for_date')
        else:
            return redirect('/new_book')

@app.route("/find", methods=['GET', 'POST'])
def find():
    title = ''
    flag = ''

    if request.method == 'GET':
        title = 'Шукати по базі'
        flag = 'get'
        return render_template('find.html', title=title, flag=flag)
    else:
        inp_txt = request.form['find_text']
        if request.form['find_block'] == 'author':
            authors = my_sql.search_by_author(inp_txt)
            session['authors'] = authors
            session['title'] = 'Автори'
            session['flag'] = 'autor'
            return redirect(url_for('.output_book_authors', authors=authors, title=title, flag=flag))
        elif request.form['find_block'] == 'serie':
            series = my_sql.search_by_series(inp_txt)
            session['series'] = series
            session['title'] = 'Серія'
            session['flag'] = 'series'
            return redirect(url_for('.output_book_serie', series=series, title=title, flag=flag))
        else:
            session['inp_txt'] = inp_txt
            return redirect(url_for('.output_book_books', inp_txt=inp_txt))


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        title = 'Додати до бази'
        flag_link = 'no_link'
        return render_template('add.html', title=title, flag_link=flag_link)
    else:
        flag_link = 'link'
        title = 'Додати до бази'
        link = request.form['link']
        status = request.form['status']
        interest = request.form['interest']
        dic_rez = BS_add.parser_add(link, status, interest)
        if dic_rez != 'error':
            return render_template('add.html', title=title, flag_link=flag_link, dic_rez=dic_rez)
        else:
            return render_template('add.html', title='error', flag_link='error')


@app.route("/output_book_authors", methods=['GET', 'POST'])
def output_book_authors():
    if request.method == 'GET':
        authors = session['authors']
        title = session['title']
        flag = session['flag']
        return render_template('find.html', title=title, flag=flag, authors=authors)
    else:
        id_author = request.form['cont_author']
        title = 'Книги автора'
        rez = my_sql.boks_by_author(id_author)
        return render_template('find_out.html', title=title, rez=rez)


@app.route("/output_book_serie", methods=['GET', 'POST'])
def output_book_serie():
    if request.method == 'GET':
        series = session['series']
        title = session['title']
        flag = session['flag']
        return render_template('find.html', title=title, flag=flag, series=series)
    else:
        id_serie = request.form['cont_series']
        title = 'Книги у серії'
        rez = my_sql.boks_by_series(id_serie)
        return render_template('find_out.html', title=title, rez=rez)


@app.route("/output_book_books", methods=['GET', 'POST'])
def output_book_books():
    if request.method == 'GET':
        title = "Книга"
        inp_txt = session['inp_txt']
        inp_txt = inp_txt.capitalize()
        books_up = my_sql.book_by_books(inp_txt)
        inp_txt = inp_txt.lower()
        books_lo = my_sql.book_by_books(inp_txt)
        books = set(books_up + books_lo)
        return render_template('find_out.html', title=title, rez=books)
    else:
        inp_txt = request.form['btn_out']
        session['inp_txt'] = inp_txt
        return redirect(url_for('.detail_book', inp_txt=inp_txt))

@app.route("/detail_book", methods=['GET', 'POST'])
def detail_book():
    if request.method == 'GET':
        title = "Подробиці"
        inp_txt = session['inp_txt']
        rez = my_sql.detail_books(inp_txt)

        return render_template('detail_book.html', title=title, genre=rez['genre'], serie=rez['serie'],
                               autor=rez['autor'], annot=rez['annot'], book_title=rez['title'], cover=rez['cover'],
                               status=rez['status'], interest=rez['interest'])
    else:
        title = 'Книги'
        return render_template('index.html', title=title)

@app.route("/new_book", methods=['GET', 'POST'])
def new_book():
    if request.method == 'GET':
        title = "Книга"
        rez = BS_new.new_books()
        return render_template('find_out_new_books.html', title=title, rez=rez)
    else:
        title = "Книга"
        inp_txt = request.form['btn_out']
        session['inp_txt'] = inp_txt
        return redirect(url_for('.detail_new_book', inp_txt=inp_txt))

@app.route("/detail_new_book", methods=['GET', 'POST'])
def detail_new_book():
    if request.method == 'GET':
        title = "Подробиці"
        link = session['inp_txt']
        status = 'Новая книга'
        interest = ''
        rez = BS_new.parser_new_book(link, status, interest)
        return render_template('detail__new_book.html', title=title, genre=rez['genre'], serie=rez['serie'],
                               autor=rez['autor'], annot=rez['annot'], book_title=rez['title'], cover=rez['cover'],
                               status=rez['status'], interest=rez['interest'], link=link)
    else:
        link = request.form['btn_out']
        webUrl = urllib.request.urlopen(link)
        title = "Подробиці"
        link = session['inp_txt']
        status = 'Новая книга'
        interest = ''
        rez = BS_new.parser_new_book(link, status, interest)
        return render_template('detail__new_book.html', title=title, genre=rez['genre'], serie=rez['serie'],
                               autor=rez['autor'], annot=rez['annot'], book_title=rez['title'], cover=rez['cover'],
                               status=rez['status'], interest=rez['interest'], link=link)
@app.route("/new_for_date", methods=['GET', 'POST'])
def new_for_date():
    if request.method == 'GET':
        title = "Книги з бази по даті"
        date_start = '2023-09-06'
        date_today = date.today()
        return render_template('calendar.html', title=title, date_start=date_start, date_today=date_today)
    else:
        input_date = request.form['date']
        title = "Книги з бази по даті"

        rez = BS_new.new_book_for_date(input_date)
        return render_template('find_out_new_books.html', title=title, rez=rez)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
