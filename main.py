from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def update():
    return render_template("update.html")
if __name__=="__main__":
     app.run()    