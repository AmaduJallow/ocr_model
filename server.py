from fastapi import FastAPI
import pytesseract
import PIL.Image
import cv2
from starlette.middleware.cors import CORSMiddleware
import urllib.request
import numpy as np

# import pillow
from model import Model


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image):
    return cv2.medianBlur(image, 5)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def imagegetter(url):
    text = None
    myconfig = r"--psm 6 --oem 1"
    if url.__contains__("http://") or url.__contains__("https://"):
        urllib.request.urlretrieve(url, "placeholder.jpg")
        img2 = np.array(PIL.Image.open("placeholder.jpg"))
        img2 = get_grayscale(img2)
        img2 = remove_noise(img2)
        img2 = thresholding(img2)
        text = pytesseract.image_to_string(img2)
    else:
        img2 = np.array(PIL.Image.open(url))
        img2 = get_grayscale(img2)
        img2  = remove_noise(img2)
        img2 = thresholding(img2)
        text = pytesseract.image_to_string(img2)
    return text


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', )
async def get_data():
    return {"Hello"}


@app.post('/url')
async def imager(data: Model):
    text_data = imagegetter(data.url)
    return text_data


print(imagegetter('./everything-has-beauty-confucius-quote.jpg'))
