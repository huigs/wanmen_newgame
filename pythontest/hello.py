# -*- coding:utf-8 -*-
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'This is my project index!'
app.run(host='127.0.0.1', port=5000)
print("hello python")