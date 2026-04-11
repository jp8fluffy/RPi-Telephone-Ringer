from DonoTracker import DonationTracker
from Telephone import Telephone
from time import time

url = "https://www.extra-life.org/api/1.6/participants/minismeef/donations"
tracker = DonationTracker(url)
start_time = time()


if __name__ == "__main__":
    while True:
        current_time = time()
        time_epoch = current_time - start_time

        if time_epoch >= 15:
            start_time = time()
            donation_data = tracker.get_new_donations()

        if donation_data[0] > 0:
            telephone = Telephone(donation_data)
            telephone.ring_if_donation()
