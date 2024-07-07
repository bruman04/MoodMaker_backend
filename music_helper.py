import requests
import os
import tempfile
from sunoai_helper import *
from chatgpt_helper import get_vid_desc

# def get_audio_file(audio_url):
#     try:
#         response = requests.get(audio_url, stream=True)
#         response.raise_for_status()

#         # Store the audio file in a temporary file
#         temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#         for chunk in response.iter_content(chunk_size=8192):
#             temp_audio_file.write(chunk)
#         # temp_audio_file.close()

#         return temp_audio_file.name
#     except Exception as e:
#         print(f"Error downloading audio file: {e}")
#         return None

def get_audio_file(audio_url, save_dir):
    try:
        response = requests.get(audio_url, stream=True)
        response.raise_for_status()

        # Extract filename from URL or use a predefined name
        filename = os.path.join(save_dir, "audio.mp3")

        # Write audio content to a local file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return filename

    except Exception as e:
        print(f"Error downloading audio file: {e}")
        return None


def get_music(vid_path):
    print("get music")

    data = generate_audio_by_prompt({
    "prompt": get_vid_desc(vid_path),
    "make_instrumental": True,
    "wait_audio": True
    })
    
    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            break

        time.sleep(5)

    return data[0]['audio_url']

