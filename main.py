from io import BytesIO

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
from PIL import Image

from SentenceDetection import underlined_sentences


app = FastAPI()


@app.get('/test')
async def testing():
    return "Hello World"


@app.post("/predict/image")
async def predict_api(file: UploadFile=File(...)):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "JPG")
    if not extension:
        return {"Error": "Image must be jpg or png format!"}

    image = await file.read()
    nparr = np.fromstring(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    sentences = underlined_sentences(img)

    return sentences

if __name__ == "__main__":
    uvicorn.run(app, debug=True)
