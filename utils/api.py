import json

import cv2
import requests


def ocr_space_file(
    filename,
    overlay=True,
    api_key="Enter your api key",
    language="eng",
    detectOrientation=True,
    scale=True,
):

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
        "detectOrientation": detectOrientation,
        "scale": scale,
        "OCREngine": 2,
    }

    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.content.decode()
