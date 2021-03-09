from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import numpy as np
from PIL import Image
import uvicorn
from SentenceDetection import underlined_sentences
import cv2

app = FastAPI()
 
@app.get('/test')
async def testing():
    return "Hello World"

@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "JPG")
    if not extension:
        return {"Error" : "Image must be jpg or png format!"}
        
    image = await file.read()
    nparr = np.fromstring(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    sentences = underlined_sentences(img)

    return sentences

if __name__ == "__main__":
    uvicorn.run(app, debug = True)