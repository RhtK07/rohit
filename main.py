from flask import Flask, render_template, request, redirect, url_for, session
import os
import pickle
import pandas as pd
import random
from google.cloud import storage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = '546781ui2n@#$j2gv3fu$%^#@'

def upload_to_cloud(source_file_name, destination_blob_name, bucket_name='rohit-ab'):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def download_from_cloud(source_blob_name, destination_file_name, bucket_name='rohit-ab'):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def store_data_to_cloud(blob, file_name, data):
    download_from_cloud(blob, file_name)
    with open(file_name, 'a+') as fp:
        fp.write(data)
    upload_to_cloud(file_name, blob)


def new_session():
    session['new'] = 'no'
    download_from_cloud('sub_ids', '/tmp/sub_ids')
    sub_id = int(open('/tmp/sub_ids', 'r').read())
    session['sub_id'] = sub_id + 1
    open('/tmp/sub_ids', 'w').write(str(sub_id+1))
    upload_to_cloud('/tmp/sub_ids', 'sub_ids')
    return session


@app.route('/')
def home():
    print(session.keys())
    # if 'new' not in session:
    new_session()
    print(session.keys())
    return render_template('index.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    download_from_cloud('subjects.csv', '/tmp/subjects.csv')
    with open('/tmp/subjects.csv', 'a+') as fp:
        fp.write('{},{},{},{}\n'.format(session['sub_id'], request.form['name'], request.form['age'], request.form['gender']))
    upload_to_cloud('/tmp/subjects.csv', 'subjects.csv')

    with open('/tmp/S{}.csv'.format(session['sub_id']), 'w+') as fp:
        fp.write('Test,Response\n')
    upload_to_cloud('/tmp/S{}.csv'.format(session['sub_id']), 'S{}.csv'.format(session['sub_id']))
    
    tests = os.listdir('static/AB_test/')
    return render_template('test.html', audpath='static/AB_test/', tests=tests)


@app.route('/end', methods=['GET', 'POST'])
def end():
    results = '\n'.join(request.form['results'].split('-'))
    store_data_to_cloud('S{}.csv'.format(session['sub_id']), '/tmp/S{}.csv'.format(session['sub_id']), results)
    return render_template('end.html')


if __name__ == "__main__":
    app.run(debug=True)
