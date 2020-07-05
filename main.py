from flask import Flask, render_template, request, redirect, url_for
import os
import sys
import pickle
import pandas as pd
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('rohit.html', audpath=audpath, tests=tests)


@app.route('/end',methods=['GET', 'POST'])
def end():
	results = '\n'.join(request.form['results'].split('-'))
	print(results)
	return render_template('end.html')


if __name__ == "__main__":
	audpath = 'static/AB_test/'
	tests = os.listdir(audpath)
	app.run(debug=True)
