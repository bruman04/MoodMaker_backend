import requests

def get_music():

    url = "https://api.aimlapi.com/generate"
    headers = {
        "Authorization": "55f5117400a24197a14b9dcb18506e79",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": "Create a relaxing ambient music track",
        "make_instrumental": True,
        "wait_audio": True
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.content)
    return response.content
