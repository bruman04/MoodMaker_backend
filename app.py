import os
from flask import Flask, request, redirect, url_for, jsonify, Response, session
import requests
import tempfile
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import boto3
from s3_helper import upload, download
from chatgpt_helper import get_vid_desc
from overlay import audio_overlay
from music_helper import get_music, get_audio_file
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.secret_key =  os.getenv("SESSION_SECRET_KEY")
UPLOAD_FOLDER = "upload_files"
CORS(app, resources={r'/*': {"origins": "https://moodmaker-app-db41d8cd5ed4.herokuapp.com"}})

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
    return jsonify({'messsage' : 'index page'})

# endpoint to upload video file to AWS
@app.route("/upload", methods=['POST'])
def upload_video():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'status':'failure'}), 400
        
        f = request.files['file']
        
        session['filename'] = f.filename
        upload(f, S3_BUCKET, f.filename)

    return jsonify({'status':'success'})
    

@app.route("/download/<filename>", methods=['GET'])
def get_video(filename):
    try:
        processed_filename = f"processed_{filename}"
        
        # Generate presigned URL for the processed video
        presigned_url = download(S3_BUCKET, processed_filename)
        if presigned_url:
            return jsonify({'status': 'success', 'url': presigned_url})
        else:
            return jsonify({'status': 'failure', 'message': 'Could not generate URL'}), 500

    except Exception as e:
        print(e)
        return jsonify({'status': 'failure', 'message': str(e)}), 500


@app.route("/overlay/<filename>", methods=['GET'])
def get_overlay(filename):
    print("calling get overlay")

    try:
        # Download video from S3 to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as input_video_file:
            s3.download_file(S3_BUCKET, filename, input_video_file.name)
            input_video_path = input_video_file.name
        
        audio_url = get_music(input_video_path)
        temp_audio_path = get_audio_file(audio_url)

        if not temp_audio_path:
            raise Exception("Failed to download audio file")
        
        print(temp_audio_path)
        # Overlay audio onto video
        processed_video_path = audio_overlay(input_video_path, temp_audio_path)
        
        # Upload processed video back to S3
        processed_filename = f"processed_{filename}"

        print("Session data after storing", dict(session))  # Debug print
        s3.upload_file(processed_video_path, S3_BUCKET, processed_filename)

    except:
        return jsonify({'status' : 'failure', 'message' : 'Unable to save overlay to S3'}), 500
    
    return jsonify({'status' : 'success'})

if __name__ == "__main__":
    app.run(debug=True)