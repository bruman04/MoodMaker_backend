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
OPENAI_API_KEY="YOUR OPENAI API KEY"
SESSION_SECRET_KEY="YOUR SESSION SECRET KEY"

```

## Create a .config file
```sh
import os

DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_NAME = os.getenv('DB_NAME', '')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

```

## Run the app locally 
```sh
flask --debug run
```

Note: This application is also hosted on https://moodmaker-flask-backend-944549f9ef80.herokuapp.com but not fully functioning due to lack of memory.
