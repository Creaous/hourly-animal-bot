# Hourly Animal Bot

Downloads images from Unsplash (every midnight) and posts them to Twitter (every hour).

## Setup

- Create a `.env` file with the following variables:
  - `TWITTER_USERNAME`
  - `TWITTER_EMAIL`
  - `TWITTER_PASSWORD`
  - `TWITTER_TOTP_SECRET`
  - `UNSPLASH_API_KEY`
  - `UNSPLASH_SEARCH_QUERY`
  - `UNSPLASH_RANDOM_QUERIES_LIST`
  - `SCHEDULER_TIMEZONE`

OR:

- Copy `.env.example` to `.env` and fill in the values.

### Docker

```bash
docker build -t twitter-unsplash-bot .
```

```bash
docker run -it --rm --env-file .env twitter-unsplash-bot
```

### Manual

1. Run `pip install -r requirements.txt`
2. Run `python scheduler.py` to run the scheduler.

## Removing Attribution

You are not allowed to remove the attribution from the images as per Unsplash's developer agreement.
