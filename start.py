from flask import Flask, render_template, request, redirect
from BS import BS_add
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        title = 'Вітання'
        return render_template('index.html', title=title)
    else:
        if request.form['button'] == 'add':
            return redirect('/add')
        elif request.form['button'] == 'statistics':
            title = 'Вітання'
            return render_template('index.html', title=title)
        elif request.form['button'] == 'find':
            title = 'Вітання'
            return render_template('index.html', title=title)
        else:
            title = 'Вітання'
            return render_template('index.html', title=title)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        title = 'Додати до бази'
        flag_link = 'no_link'
        return render_template('add.html', title=title, flag_link=flag_link)
    else:
        title = 'Додати до бази'
        link = request.form['link']
        rez = BS_add.parser_add(link)
        print("rez   " + rez)

        return render_template('add.html', title=title, rez=rez)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)