import schedule
import time
import subprocess
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

print("Starting scheduler...")

def write_files():
    os.makedirs("run", exist_ok=True)
    os.makedirs("run/timings", exist_ok=True)
    os.makedirs("run/images", exist_ok=True)

    with open("run/timings/unsplash.txt", "w") as file:
        file.write("")
    with open("run/timings/twitter.txt", "w") as file:
        file.write("")
    with open("run/image_ids.txt", "w") as file:
        file.write("")

def write_timing(type):
    with open(f"run/timings/{type}.txt", "a") as file:
        file.write("{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))

def read_timing(type):
    with open(f"run/timings/{type}.txt", "r") as file:
        last_run = file.readlines()[-1].strip()
        last_run_time = datetime.datetime.strptime(last_run, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        time_difference = current_time - last_run_time
        return time_difference.total_seconds()

def run_task(type):
    print(f"Running {type} task...")
    write_timing(type)
    subprocess.Popen(["python", f"{type}.py"])

write_files()

schedule.every().day.at("00:00", os.getenv("SCHEDULER_TIMEZONE", '')).do(run_task, "unsplash")

for twitterTime in ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]:
    print("Twitter task scheduled for {}".format(twitterTime))
    schedule.every().day.at(twitterTime, os.getenv("SCHEDULER_TIMEZONE", '')).do(run_task, "twitter")

while True:
    schedule.run_pending()
    time.sleep(1)
