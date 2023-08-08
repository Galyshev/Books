

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        title = 'Вітання'
        return render_template('index.html', title=title)
    else:
        title = 'Вітання'
        if request.form['button'] == 'add':
            print('add')
        elif request.form['button'] == 'statistics':
            print('statistics')
        elif request.form['button'] == 'find':
            print('find')
        else:
            print('new')

        return render_template('index.html', title=title)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)