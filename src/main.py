from typing import Union
from flask import Flask, request
import prework
import data_analysis as da
from models import Root

app = Flask(__name__)
the_root: Union[Root, None] = None


@app.route("/health", methods=["GET"])
def health():
    return "OK"


@app.route("/init", methods=["GET"])
def init():
    global the_root
    the_root, _ = prework.init()
    return "OK"


@app.route("/addData", methods=["POST"])
def addData():
    pass


@app.route("/frequency", methods=["GET"])
def frequency():
    args = request.args
    if the_root is None:
        return "No data", 404
    return da.wordCnt(the_root, args)


@app.route("/kMeans", methods=["GET"])
def kMeans():
    k = int(request.args.get("k") or 3)
    if the_root is None:
        return "No data", 404
    return da.kMeans_tree(the_root, k)


@app.route("/fmap", methods=["GET"])
def fmap():
    args = request.args
    if the_root is None:
        return "No data", 404
    return da.kMeans_map(the_root, args)


@app.route("/emo", methods=["GET"])
def emo():
    args = request.args
    if the_root is None:
        return "No data", 404
    return {"emo2": da.emo2(the_root, args), "emo5": da.emo5(the_root, args)}


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
