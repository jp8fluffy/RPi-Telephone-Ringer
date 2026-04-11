import json
import gpiozero
from time import time
import pyttsx4


class Telephone:
    def __init__(self, donation_data) -> None:
        self.number_of_donations = donation_data[0]
        self.donations_json = donation_data[1]
        self.tts = pyttsx4.init()

        self.relay = gpiozero.OutputDevice(pin=26)
        self.button = gpiozero.InputDevice(pin=17)

    def ring_if_donation(self):

        relay_start_time = time()
        button_start_time = time()

        while self.number_of_donations > 0:
            print(self.button.value)
            relay_current_time = time()
            relay_epoch = relay_current_time - relay_start_time

            button_current_time = time()
            button_epoch = button_current_time - button_start_time

            if relay_epoch >= 2:
                relay_start_time = relay_current_time
                self.relay.toggle()

            if self.button.value == 1 and button_epoch >= 2:
                button_start_time = time()
                try:
                    donation_to_read_json = json.loads(
                        self.return_and_remove_last_donation()
                    )
                    donation_name = str(donation_to_read_json["displayName"])
                    donation_amount = str(donation_to_read_json["amount"])
                    if "message" in donation_to_read_json:
                        donation_message = str(donation_to_read_json["message"])
                    else:
                        donation_message = ""
                    self.tts.say(
                        f"{donation_name} donated {donation_amount} dollars and said..... {donation_message}"
                    )
                    self.tts.runAndWait()
                except (IndexError, TypeError):
                    print("occured when trying to read donation")

    def return_and_remove_last_donation(self):
        if self.number_of_donations > 0:
            last_donation = self.donations_json[-1]
            self.donations_json = self.donations_json[:-1]
            self.number_of_donations -= 1
            return last_donation
