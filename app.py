# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 16:03:55 2023

@author: ranaf
"""

from flask import Flask, render_template

app = Flask(__name__)

import sys
print(sys.executable)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)