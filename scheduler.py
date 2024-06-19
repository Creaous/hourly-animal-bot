import schedule
import time
import subprocess
import datetime

print("Starting scheduler...")

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

# Schedule the Unsplash task to run every 5 hours
schedule.every(5).hours.do(run_task, "unsplash")

# Schedule the Twitter task to run every 1 hour
schedule.every(1).hours.do(run_task, "twitter")

try:
    if read_timing("twitter") > 3600:
        run_task("twitter")
except:
    run_task("twitter")

try:
    if read_timing("unsplash") > 18000:
        run_task("unsplash")
except:
    run_task("unsplash")

# Run the scheduled tasks and catch up on missed tasks
while True:
    print("Still running...")
    schedule.run_pending()
    time.sleep(1)
