from flask import Flask, render_template, request
from search import searchFor
import linecache

app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def homePOST():
    text = request.form["srch"]
    print(text)
    return searchFor(text)


@app.route("/search")
def searched():
    return render_template("searched.html")


@app.route("/search", methods=["POST"])
def searchedPOST():
    text = request.form["srch"]
    print(text)
    return searchFor(text)


if __name__ == "__main__":
    linecache.getline("id.txt", 0)
    app.run(debug=True)
