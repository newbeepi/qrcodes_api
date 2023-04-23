import cv2
import pyzbar.pyzbar as pyzbar
import requests

import io
from PIL import Image
import json

img = cv2.imread('1.png')  # type here path to your qrcode

decoded_objects = pyzbar.decode(img)

urls = decoded_objects[0].data.decode('utf-8').split("\n")
base_url = "http://127.0.0.1:8000" # change it if you have different link
image_url = base_url + urls[0]
data_url = base_url + urls[1]


img_response = requests.get(image_url)
data_response = requests.get(data_url)

data = json.loads(data_response.content)
print(
    """
    Item: {name}
    Description: {description}
    Price: {price}
    """.format(name=data["name"], description=data["description"], price=data["price"])
)
img = Image.open(io.BytesIO(img_response.content))
img.show()

