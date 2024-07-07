from IPython.display import display, Image, Audio

import cv2  
import base64
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests


def get_vid_desc(video):
    # Load environment variables from .env file
    load_dotenv()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    # change this
    video = cv2.VideoCapture(video)

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
                "You are a musician that wants to generate music for frames from this video. Generate a one sentence prompt of the description of the atmosphere of the video to instruct an AI music generator to create music.",
                *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
            ],
        },
    ]
    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 30,
    }

    result = client.chat.completions.create(**params)
    description = result.choices[0].message.content
    print(description)

    return (description)

# video = "./test_data/test_vid.mp4"
# get_vid_desc(video)
