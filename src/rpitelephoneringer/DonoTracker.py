from pathlib import Path
import os.path
import cloudscraper
import json


class DonationTracker:
    # Class for getting and storing donations
    def __init__(self, url, filename="donos.json") -> None:
        self.url = url
        self.scraper = cloudscraper.create_scraper()

        # Uses filename (if given) to set path to the json file with donation information
        # Otherwise uses default path (local and named donos.json)
        self.filename = filename
        self.path_to_json = Path(filename)
        self._check_extension_of_json_file()

    # ----------- Public methods --------------------

    def get_new_donations(self):
        stored_donation_data = self._load_json_file()
        new_donation_data = self._request_donos()

        amount_of_new_donations = len(new_donation_data) - len(stored_donation_data)

        if amount_of_new_donations > 0:
            new_donations_json = new_donation_data[0:amount_of_new_donations]
            self._output_to_file(new_donation_data)
            return [amount_of_new_donations, new_donations_json]
        elif amount_of_new_donations < 0:
            raise ValueError(
                f"CRITICAL ERROR: New donations are smaller than stored donations ({amount_of_new_donations=})"
            )
        else:
            empty_json = "{}"
            return [amount_of_new_donations, empty_json]

    def get_last_cached_donation(self):
        return self.get_cached_donation(0)

    def get_cached_donation(self, donation_index: int):
        if os.path.isfile(self.path_to_json):
            try:
                donation_data = self._load_json_file()
                return donation_data[donation_index]
            except IndexError, TypeError:
                pass

        print(
            "Could not get donations: Index out of range (or not an integer) or file does not exist"
        )
        empty_json = "{}"
        return empty_json

    # ------------ Private Methods ------------------

    def _check_extension_of_json_file(self):
        expected_file_extension = ".json"
        if (
            self.path_to_json.suffix.lower() != expected_file_extension
        ):  # .suffix.lower() method from pathlib returns just the file extension
            raise TypeError(
                f'json file given ({self.filename}) is not of type ".json". '
            )

    def _create_donos_json(self):
        try:
            with open(self.path_to_json, "w") as file:
                empty_json = "{}"
                file.write(empty_json)
        except OSError as error:
            print(f"Error creating json file {self.path_to_json}: {error}")

    def _request_donos(self):
        # request donoations from extralife, convert from html to json and return
        dono_api_request = self.scraper.get(self.url)
        dono_json = json.loads(dono_api_request.text)
        return dono_json

    def _output_to_file(self, json_data):
        # Check for an already existing json file, if none exists, create a new one
        try:
            # Checks for json file existance
            abs_path_to_json = self.path_to_json.resolve(strict=True)
        except FileNotFoundError:
            print("File does not exist... creating json file")
            self._create_donos_json()
            with open(self.path_to_json, "w") as file:
                file.write(json.dumps(json_data, indent=4))
        else:
            # File exists
            with open(abs_path_to_json, "w") as file:
                file.write(json.dumps(json_data, indent=4))

    def _load_json_file(self, filepath=None, max_attempts=3):
        attempts = 0

        while attempts < max_attempts:
            if filepath is not None:
                try:
                    with open(filepath, "r") as json_file:
                        stored_donation_data = json.load(json_file)
                    return stored_donation_data
                except FileNotFoundError:
                    print("Json file not found; Creating new json file...")
                    self._create_donos_json()
                    attempts += 1
            else:
                try:
                    with open(self.path_to_json, "r") as json_file:
                        stored_donation_data = json.load(json_file)
                    return stored_donation_data
                except FileNotFoundError:
                    print("Json file not found; Creating new json file...")
                    self._create_donos_json()
                    attempts += 1

        if attempts == max_attempts:
            raise RuntimeError(
                "Could not load specified file and could not create new file"
            )
