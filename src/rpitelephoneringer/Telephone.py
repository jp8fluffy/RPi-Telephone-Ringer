import json
import gpiozero
from time import time
import pyttsx3


class Telephone:
    def __init__(self, donation_data) -> None:
        self.number_of_donations = donation_data[0]
        self.donations_json = donation_data[1]
        self.tts = pyttsx3.init()

        self.relay = gpiozero.OutputDevice(pin=26)
        self.button = gpiozero.Button(pin=2, bounce_time=1)

    def ring_if_donation(self):

        relay_start_time = time()

        while len(self.donations_json) > 0:
            relay_current_time = time()
            relay_epoch = relay_current_time - relay_start_time

            if relay_epoch >= 2:
                relay_start_time = relay_current_time
                self.relay.toggle()

            if self.button.is_pressed:
                try:
                    donation_to_read_json = json.loads(
                        self.return_and_remove_last_donation()
                    )
                    donation_name = str(donation_to_read_json["displayName"])
                    donation_amount = str(donation_to_read_json["amount"])
                    donation_message = str(donation_to_read_json["message"])
                    self.tts.say(
                        f"{donation_name} donated {donation_amount} dollars and said..... {donation_message}"
                    )
                except IndexError:
                    print("occured when trying to read donation")

    def return_and_remove_last_donation(self):
        if len(self.donations_json) > 0:
            last_donation = self.number_of_donations[-1]
            self.number_of_donations = self.number_of_donations[:-1]
            return last_donation
