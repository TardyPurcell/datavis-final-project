from typing import Union
from flask import Flask, request
import prework
import data_analysis as da
from models import Root
import calendar, time
from urllib import parse

app = Flask(__name__)
the_root: Union[Root, None] = None


@app.route("/health", methods=["GET"])
def health():
    return "OK"


@app.route("/init", methods=["GET"])
def init():
    global the_root
    the_root, _ = prework.init()
    return the_root.toOption()


@app.route("/addData", methods=["POST"])
def addData():
    file = request.files.get("file")
    if file is None:
        return "upload failed", 400
    filename = file.filename
    if filename is None:
        return "filename empty", 400
    suffix = filename.split(".")[-1]
    if suffix != "csv":
        return "please upload a csv file", 400
    filepath = f"./upload/{calendar.timegm(time.gmtime())}.csv"
    file.save(filepath)
    global the_root
    the_root, _ = prework.addData(filepath)
    return the_root.toOption()


@app.route("/frequency", methods=["GET"])
def frequency():
    args = {k: parse.unquote(v) for k, v in request.args.items()}
    if the_root is None:
        return "No data", 404
    return da.wordCnt(the_root, args)


@app.route("/kMeans", methods=["GET"])
def kMeans():
    k = 0
    try:
        k = int(request.args.get("k") or 3)
    except ValueError:
        return "k must be an integer", 400
    if k <= 0:
        return "k must be greater than 0", 400
    if the_root is None:
        return "No data", 404
    return da.kMeans_tree(the_root, k)


@app.route("/fmap", methods=["GET"])
def fmap():
    args = {k: parse.unquote(v) for k, v in request.args.items()}
    if the_root is None:
        return "No data", 404
    return da.kMeans_map(the_root, args)


@app.route("/emo", methods=["GET"])
def emo():
    args = {k: parse.unquote(v) for k, v in request.args.items()}
    if the_root is None:
        return "No data", 404
    return {"emo2": da.emo2(the_root, args), "emo5": da.emo5(the_root, args)}


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
