# MoodMaker Backend

This is the submission from the group EyeLadies for TikTok Jam 2024

This project was built using Flask and uses AWS S3 as our database.

## Project Setup
Create a virtual env on your machine

```sh
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```
## Create a .env file
```sh
FLASK_APP=app.py
FLASK_ENV=development
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
S3_BUCKET=your-s3-bucket-name
```

## Run the app locally 
```sh
flask --debug run
```

Note: This application is also hosted on https://moodmaker-flask-backend-944549f9ef80.herokuapp.com but not fully functioning due to lack of memory.
