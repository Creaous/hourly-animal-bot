import os
import random
from twikit import Client
from dotenv import load_dotenv

load_dotenv()

# Get list of files in image/ folder
files = os.listdir('run/images/')

# exclude all .gitkeep files
files = [f for f in files if f != '.gitkeep']

# Initialize client
client = Client('en-US')

client.login(
    auth_info_1=os.getenv('TWITTER_USERNAME'),
    auth_info_2=os.getenv('TWITTER_EMAIL'),
    password=os.getenv('TWITTER_PASSWORD'),
    totp_secret=os.getenv('TWITTER_TOTP_SECRET')
)

media_retry_limit = 3
photo_tweet_retry_limit = 3

for _ in range(media_retry_limit):
    try:
        file = random.choice(files)
        media = client.upload_media(f'run/images/{file}')
        os.remove(f'run/images/{file}')
        imageData = [file.split(".jpg")[0], media]
        break
    except Exception as e:
        print(e)
else:
    print("Failed to upload image. Ignoring rest of script.")
    exit()

for _ in range(photo_tweet_retry_limit):
    try:
        photo_tweet = client.create_tweet(media_ids=[imageData[1]])
        break
    except Exception as e:
        print(e)
else:
    print("Failed to post photo. Ignoring rest of script.")
    exit()

for _ in range(photo_tweet_retry_limit):
    try:
        attribution_tweet = client.create_tweet(
            text=f'Full quality version: https://unsplash.com/photos/{imageData[0]}',
            reply_to=photo_tweet.id
        )
        break
    except Exception as e:
        print(e)
else:
    print("Failed to post attribution. Ignoring rest of script.")
    exit()
