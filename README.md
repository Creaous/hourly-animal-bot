# Hourly Animal Bot

Downloads images from Unsplash (every 5 hours) and posts them to Twitter (every hour).

## Setup

1. Create a `.env` file with the following variables:
   - `TWITTER_USERNAME`
   - `TWITTER_EMAIL`
   - `TWITTER_PASSWORD`
   - `TWITTER_TOTP_SECRET`
   - `UNSPLASH_API_KEY`
   - `UNSPLASH_DOWNLOAD_COUNT`
   - `UNSPLASH_SEARCH_QUERY`

### Docker

```bash
docker build -t twitter-unsplash-bot .
```

```bash
docker run -it --rm --env-file .env twitter-unsplash-bot
```

### Manual

2. Run `pip install -r requirements.txt`
3. Run `python unsplash.py` to run the scheduler.

_have the download count set to atleast 5-6 otherwise the bot won't have any posts to make since it only runs the download task every 5 hours_

## Removing Attribution

You are not allowed to remove the attribution from the images as per Unsplash's developer agreement.
