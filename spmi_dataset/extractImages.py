

import pandas as pd
import re


df=pd.read_csv("datasets_articles.csv")

import requests
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    """
    Downloads an image from the specified URL and saves it to the given path.

    Parameters:
    - url: str, the URL of the image to download.
    - save_path: str, the file path where the image should be saved.
    """
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Open the response content as an image
        image = Image.open(BytesIO(response.content))
        # Save the image to the specified path
        image.save(save_path)
        print(f"Image successfully downloaded and saved to {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def extract_urls(text):
    url_pattern = re.compile(
        r'https?://'  # Match http:// or https://
        r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        r'(?:\:\d+)?'  # Optional port number
        r'(?:/[-\w@:%_\+.~#?&//=]*)?'  # Path and other parts
        , re.IGNORECASE)

    # Find all matches in the text
    urls = url_pattern.findall(text)
    urls=[url for url in urls if "artigos_imagens" in url]
    return urls

import os
folder_path="article_images"

os.makedirs(folder_path, exist_ok=True)





import time
import random
image_urls=list()
for index,row in df.iterrows():
    images=extract_urls(row["articles"])

    image_location=os.path.join(folder_path,str(index))
    os.makedirs(image_location, exist_ok=True)
    image_number=0
    for i in images:
        time.sleep(random.randint(3, 7))

        try:
            download_image(i,os.path.join(image_location,str(image_number)+".jpg"))
            image_number=image_number+1
        except Exception as e:
            try:
                download_image(i, os.path.join(image_location, str(image_number) + ".png"))
                image_number = image_number+1
            except Exception as e:
                print("error in downloading image "+ str(e))

