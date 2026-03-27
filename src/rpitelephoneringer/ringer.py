import gpiozero
import json
import concurrent.futures
from time import time


class Ring:
    def __init__(self, number_of_donations: int, donations_json: dict) -> None:
        self.number_of_donations = number_of_donations
        self.last_donation_index = self.number_of_donations - 1
        self.donations_json = donations_json

        self.button_read_donation = gpiozero.Button(2)
        self.relay = gpiozero.OutputDevice(26)

    # ---- Public Methods ------
    def ring_if_donation(self, ring_duration_seconds: int):
        relay_start_time = time()
        button_start_time = time()
        while self.number_of_donations >= 0:
            relay_current_time = time()
            button_current_time = time()
            relay_epoch = relay_current_time - relay_start_time
            button_epoch = button_current_time - button_start_time

            if relay_epoch >= ring_duration_seconds:
                relay_start_time = relay_current_time
                self.relay.toggle()

            if self.button_read_donation.is_pressed and button_epoch >= 1:
                print("relay off")
                self.relay.off()

                current_donation_json = self.donations_json[self.last_donation_index]
                print(json.dumps(current_donation_json, indent=4))

                print("removing donation and json")
                self.donations_json = self.donations_json[: self.last_donation_index]
                self.number_of_donations = self.number_of_donations - 1

                return current_donation_json

    # --- Private Methods ------
    def _open_check_button_read_donation_thread(self) -> bool:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            button_read_thread = executor.submit(self._check_button_pressed, 1)
            return button_read_thread.result()

    def _check_button_pressed(self, button: gpiozero.Button) -> bool:
        button.wait_for_active()
        return True
