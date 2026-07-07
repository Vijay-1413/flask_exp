from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    name="Vijay"
    notification=10
    mail=8
    return render_template("dashboard.html",name_temp=name,notification_temp=notification,mail_temp=mail)

if __name__ == "__main__":
    app.run(debug=True)