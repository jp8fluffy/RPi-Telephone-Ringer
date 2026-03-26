import gpiozero
import json
from rpitelephoneringer.DonoTracker import DonationTracker
import rpitelephoneringer.ringer as ringer
from time import time

url = "https://www.extra-life.org/api/1.6/participants/minismeef/donations"
tracker = DonationTracker(url)
start_time = time()

relay = gpiozero.OutputDevice(26)
read_donation_button = gpiozero.Button(2)

if __name__ == "__main__":
    while True:
        current_time = time()
        if current_time - start_time >= 15:
            start_time = current_time
            new_donos = tracker.get_new_donations()
            print(
                f"Number of new donations {new_donos[1][0]['message']} {json.dumps(new_donos[1], indent=4)}"
            )
            print("done")
