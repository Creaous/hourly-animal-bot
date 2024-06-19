import os
import requests
from pyunsplash import PyUnsplash
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

def get_existing_ids():
    with open("run/image_ids.txt", "r") as f:
        return f.read().splitlines()

def compress_image(file_path, quality=85):
    """Compress an image by resizing and reducing its quality."""
    img = Image.open(file_path)
    img.save(file_path, quality=quality, optimize=True)

pu = PyUnsplash(api_key=os.getenv('UNSPLASH_API_KEY'))

photos = pu.photos(type_='random', count=os.getenv('UNSPLASH_DOWNLOAD_COUNT'), featured=True, query=os.getenv('UNSPLASH_SEARCH_QUERY'))

existing_ids = get_existing_ids()

for photo in photos.entries:
    if photo.id in existing_ids:
        break

    response = requests.get(photo.link_download, allow_redirects=True)

    os.makedirs("run/images", exist_ok=True)

    file = f"run/images/{photo.id}.jpg"

    with open(file, 'wb') as f:
        f.write(response.content)

    compress_image(file)

    with open("run/image_ids.txt", "a") as f:
        f.write(photo.id + "\n")
