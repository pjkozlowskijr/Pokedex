from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html.j2")

@app.route("/lookup", methods = ['GET', 'POST'])
def lookup():
    