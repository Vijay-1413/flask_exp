from flask import Flask, render_template

app = Flask(__name__)

@app.route("/pageone")
def firstpage():
    return render_template("firstpage.html")

@app.route("/pagetwo")
def secondpage():
    return render_template("secondpage.html")

if __name__ == "__main__":
    app.run()