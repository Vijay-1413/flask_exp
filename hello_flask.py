from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/input')
def home():
    return render_template('inputpage.html')

@app.route('/output', methods=['POST'])
def output():

    name = request.form['name']

    students = ["Arun", "Bala", "Kumar"]

    return render_template(
        'outputpage.html',
        name=name,
        students=students
    )

if __name__ == '__main__':
    app.run(debug=True)