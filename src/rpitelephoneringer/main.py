import gpiozero
import json
from donationmanager import DonoTracker
import rpitelephoneringer.ringer as ringer


url = "https://www.extra-life.org/api/1.6/participants/minismeef/donations"
tracker = DonoTracker.DonationTracker(url)

if __name__ == "__main__":
    new_donos = tracker.get_new_donations()
    print(
        f"Number of new donations {new_donos[0]} {json.dumps(new_donos[1], indent=4)}"
    )
    ringer1 = ringer.Ring(new_donos[0], new_donos[1])
