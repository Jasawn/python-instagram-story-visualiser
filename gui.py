from flask import Flask, url_for, render_template, request, redirect
from stories import *
from getCookiesIG import *
import json
import os
import threading
import time

scraper = Flask(__name__, static_folder='static')
## function to read json file, returns dict with file data
def open_json(abs_filepath):
    try:
        with open(abs_filepath) as file:
            file_data = json.load(file)
            return file_data
    except Exception as e:
        print(e)

@scraper.route("/")
def landingPage():
    return render_template("index.html")

@scraper.route("/enterParams")
def enterParams():
    return render_template("searchParams.html")

@scraper.route("/searchParams", methods=['POST'])
def searchParams():
    username = request.form['username']
    pickle_file = username + ".pickle"
    userPass = request.form['pass']
    frequency = int(request.form['frequency'])
    userlst = request.files['userlst'].filename

    createJsonData(pickle_file,frequency,userlst)

    if not os.path.exists(pickle_file):
        if loginIG(username,userPass) == 0:
            ## Show error saying that login is unsuccessful
            return render_template("loginFailed.html")


    ## Should display an empty map here
    return render_template("map.html", freq=frequency, data="")

@scraper.route("/startScraping", methods=['POST'])
def startScrape():
    print("Inside")
    thread = threading.Thread(target=startScraping)
    thread.start()
    return ''

@scraper.route("/selectPreviousJSON")
def selectPreviousJSON():
    return render_template("previous.html")

@scraper.route("/loadSearch", methods=['POST'])
def loadSearch():
    ## To implement load map and running search in the background
    fileName = request.files['jsonFile'].filename
    data = open_json(fileName)
    frequency = data[0]["parameters"]["frequency"]
    return render_template(
        "map.html", freq = frequency,
        data=data[1]
    )

@scraper.route("/map")
def mapView():
    data = open_json('data.json')
    return render_template(
        "map.html",
        data=data[1]
        )

def createJsonData(pickle_file,frequency,userlst):
    data = [{"parameters": {"pickle_file":pickle_file,"frequency":frequency,"users_file":userlst}},{}]
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    scraper.run()