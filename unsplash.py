import os
import requests
import random
import json
from pyunsplash import PyUnsplash
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

print("Starting download and compression process...")

def get_existing_ids():
    with open("run/image_ids.txt", "r") as f:
        return f.read().splitlines()

def compress_image(file_path, quality=85):
    """Compress an image by resizing and reducing its quality."""
    img = Image.open(file_path)

    # Set the maximum width and height for the compressed image
    max_width = 1920
    max_height = 1080

    # Calculate the new width and height while preserving the aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    if aspect_ratio > 1:
        new_width = min(width, max_width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(height, max_height)
        new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_img = img.resize((new_width, new_height))

    # Save the compressed image
    resized_img.save(file_path, quality=quality, optimize=True)

pu = PyUnsplash(api_key=os.getenv('UNSPLASH_API_KEY'))

def get_random_photos(query=os.getenv('UNSPLASH_SEARCH_QUERY')):
    photos = pu.photos(type_='random', count=1, featured=True, query=query)

    existing_ids = get_existing_ids()

    for photo in photos.entries:
        if photo.id in existing_ids:
            print(f"Skipping {photo.id} as it has already been downloaded in the past.")
            break

        response = requests.get(photo.link_download, allow_redirects=True)

        file = f"run/images/{photo.id}.jpg"

        with open(file, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {photo.id}")

        print(f"Compressing {photo.id}")
        compress_image(file)

        with open("run/image_ids.txt", "a") as f:
            f.write(photo.id + "\n")
    
count = 30

query = os.getenv('UNSPLASH_SEARCH_QUERY')
queries = json.loads(os.getenv('UNSPLASH_RANDOM_QUERIES_LIST', '[]'))

if queries == []:
    print("No queries found in UNSPLASH_RANDOM_QUERIES_LIST. Using UNSPLASH_SEARCH_QUERY instead.")
    query = os.getenv('UNSPLASH_SEARCH_QUERY')

    for i in range(count):
        print(f"Query: {query}")
        get_random_photos(query=query)
else:
    for i in range(count):
        query = random.choice(queries)
        queries.remove(query)
        print(f"Query: {query}")
        get_random_photos(query=query)

print("Completed downloading and compressing images.")
