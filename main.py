import datetime
import time

import dojo_scraper
from save_to_json import save


def update_time():
    """
    Update the last_update.txt file with the current timestamp
    :return:
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y, %I:%M %p")
    with open("./last_update.txt", "w") as f:
        f.write(now)
    print(f"Set last_update.txt to {now}")


def scrape_and_save():
    """
    Perform a scrape and save the result to the configured destination
    :return:
    """
    result = dojo_scraper.scrape()
    save(result)
    update_time()


def run_indefinitely():
    while True:
        scrape_and_save()
        time.sleep(60*15)


if __name__ == '__main__':
    # Default behavior is to run indefinitely.
    run_indefinitely()

    # For testing purposes.
    # scrape_and_save()
