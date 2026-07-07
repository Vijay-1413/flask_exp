from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/inputpage")
def inputpage():
    return render_template("inputpage.html")


@app.route("/statuspage",methods=["POST"])
def statuspage():
    status = request.args.get("textinput")
    return render_template("statuspage.html", status=status)


if __name__ == "__main__":
    app.run(debug=True)