from flask import Flask, render_template, request, url_for, redirect
from search import run
import linecache

app = Flask(__name__, template_folder="templates", static_folder="statics")


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        query = request.form["srch"]
        listOfUrls = run(query)
        return redirect(url_for("search"))
    return render_template("index.html")


@app.route("/search", methods=["POST", "GET"])
def searched():
    if request.method == "POST":
        query = request.form["srch"]
        listOfUrls = run(query)
    return render_template("searched.html", urlsList=listOfUrls)



if __name__ == "__main__":
    app.run(debug=True)
