from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

def get_vid_desc():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    # change this
    video = cv2.VideoCapture("test_data/test_vid.mp4")

    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    video.release()
    print(len(base64Frames), "frames read.")

    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                "You are a musician that wants to generate music for frames from this video. Generate a prompt of the description of the atmosphere of the video under sixty words to instruct an AI music generator to create music.",
                *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
            ],
        },
    ]
    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 60,
    }

    result = client.chat.completions.create(**params)
    print(result.choices[0].message.content)
    description = result.choices[0].message.content
    return (description)
