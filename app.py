import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import boto3
from s3_helper import upload, download
from chatgpt_helper import get_vid_desc
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
UPLOAD_FOLDER = "upload_files"
CORS(app, resources={r'/*': {'origins' : '*'}})


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

@app.route("/home")
def index():
    return render_template("index.html")

# endpoint to upload video file to AWS
@app.route("/upload", methods=['POST'])
def upload_video():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'status':'failure'}), 400
        
        f = request.files['file']
        upload(f, S3_BUCKET, f.filename)


    return jsonify({'status':'success'})

@app.route("/description", methods=["GET", "POST"])
def video_desc():
    # get video from s3 

    # plug video into function below
    gpt_desc = get_vid_desc()
    return jsonify({'status' : 'sucess'}, {'prompt' : gpt_desc})

# download completed file from s3
@app.route("/download/<filename>", methods=['GET'])
def get_video(filename):
    url = download(S3_BUCKET, filename)
    print("URL: ",url)
    if url:
        return jsonify({'status': 'success', 'url': url})
    else:
        return jsonify({'status': 'failure', 'message': 'Could not generate URL'}), 500


if __name__ == "__main__":
    app.run(debug=True)