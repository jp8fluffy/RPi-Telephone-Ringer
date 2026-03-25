import gpiozero
import json
import concurrent.futures
from time import sleep


class Ring:
    def __init__(self, number_of_donations: int, donations_json: dict) -> None:
        self.number_of_donations = number_of_donations
        self.last_donation_index = self.number_of_donations - 1
        self.donations_json = donations_json

        if self.number_of_donations > 0:
            self.has_donation = True

        self.button_read_donation = gpiozero.Button(2)
        self.relay = gpiozero.OutputDevice(3)

    @property
    def last_donation_index(self):
        """Getter for last_donation_index"""
        return self._last_donation_index

    @last_donation_index.setter
    def last_donation_index(self, number_of_donations):
        self._last_donation_index = number_of_donations - 1

    # ---- Public Methods ------
    def ring_if_donation(self, ring_duration_seconds: int):
        while self.number_of_donations > 0:
            button_pressed: bool = self._open_check_button_read_donation_thread()
            if button_pressed:
                print("relay off")
                self.relay.off()

                current_donation_json = self.donations_json[self.last_donation_index]
                print(json.dumps(current_donation_json, indent=4))

                print("removing donation and json")
                self.donations_json = self.donations_json[: self.last_donation_index]
                self.number_of_donations = self.number_of_donations - 1

                return current_donation_json
            self.relay.toggle()
            print("toggled relay")
            print("Sleeping")
            sleep(ring_duration_seconds)

    # --- Private Methods ------
    def _open_check_button_read_donation_thread(self) -> bool:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            button_read_thread = executor.submit(self._check_button_pressed, 1)
            return button_read_thread.result()

    def _check_button_pressed(self, button: gpiozero.Button) -> bool:
        button.wait_for_active()
        return True
