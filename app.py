from flask import Flask, render_template, request
from search import searchFor

app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def searchPOST():
    text = request.form["srch"]
    print(text)
    return searchFor(text)


if __name__ == "__main__":
    app.run(debug=True)
