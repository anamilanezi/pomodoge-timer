# import tkinter as tk
import json
import requests
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from pprint import pprint

from random import choice
from dotenv import load_dotenv
import os


load_dotenv("D:/Usuarios/Usuario/ENV/.env")

API = os.getenv("ABSTRACT_API_KEY_2")

print("Datafile being executed")


def create_list(pet):
    URL = f"https://shibe.online/api/{pet}"
    parameters = {
        "count": 30,
    }

    response = requests.get(URL, params=parameters)
    print(response.status_code)

    return response.json()


# URL = "https://shibe.online/api/cats"
# parameters = {
#     "count": 30,
# }
#
# response = requests.get(URL, params=parameters)
# print(response.status_code)
#
# images_list = response.json()


# ------ Resize image from URL ------ #
def resize_random(images_list):
    # params = {
    #     "width": 300,
    #     "height": 300,
    #     "strategy": 'auto',
    # }
    params = {
        "width": 300,
        "height": 300,
        "strategy": 'fit',
        "crop_mode": 't',
    }

    data = {
        "api_key": API,
        "url": choice(images_list),
        "lossy": True,
        "resize": params,
    }

    request = Request(
        'https://images.abstractapi.com/v1/url/',
        data=json.dumps(data).encode('ascii'),
        headers={"Content-Type": 'application/json'},
        method='POST',
    )

    with urlopen(request) as response:
        image = json.load(response)['url']
        imageURL = Request(image,
                           headers={'User-Agent': 'Mozilla/5.0'})
        u = urlopen(imageURL)
        raw_data = u.read()
        u.close()

        return raw_data

