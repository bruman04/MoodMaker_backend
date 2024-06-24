import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import boto3
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)


#configure AWS S3 bucket
S3_BUCKET = 'moodmaker-media'
S3_REGION = 'ap-southeast-2'
S3_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
S3_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3',
                  region_name=S3_REGION,
                  aws_access_key_id=S3_ACCESS_KEY,
                  aws_secret_access_key=S3_SECRET_KEY)

#configure SQLalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)