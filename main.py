from flask import Flask, redirect, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000)