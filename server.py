from fastapi import FastAPI
import pytesseract
import PIL.Image
from starlette.middleware.cors import CORSMiddleware
import urllib.request

# import pillow
from model import Model


def imagegetter(url):
    myconfig = r"--psm 6 --oem 1"
    if url.__contains__("http://") or url.__contains__("https://"):
        urllib.request.urlretrieve(url, "placeholder.jpg")
        text = pytesseract.image_to_string(
            PIL.Image.open("placeholder.jpg"), config=myconfig)
    else:
        text = pytesseract.image_to_string(
            PIL.Image.open(url), config=myconfig)

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


print(imagegetter('./image_4.png'))
