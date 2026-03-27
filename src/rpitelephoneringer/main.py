import gpiozero
import json
from rpitelephoneringer.DonoTracker import DonationTracker
import rpitelephoneringer.ringer as ringer
from time import time
from platformdirs import user_cache_dir
from gtts import gTTS
from os import system, path
import shutil

cachedir = user_cache_dir("rpitelephoneringer", "Johnpaul Shields", ensure_exists=True)

url = "https://www.extra-life.org/api/1.6/participants/minismeef/donations"
tracker = DonationTracker(url, cachedir + "/donos.json")
start_time = time()

# relay = gpiozero.OutputDevice(26)
# read_donation_button = gpiozero.Button(2)


def create_and_play_tts(text: str, dir, dono_number: int):
    file_path = str(dir + "/" + str(dono_number) + ".mp3")
    tts = gTTS(text, lang="en", slow=True)
    tts.save(file_path)
    system("mpg123 " + str(file_path))


if __name__ == "__main__":
    if path.exists(cachedir) and path.isdir(cachedir):
        shutil.rmtree(cachedir)
        print("deleted cache")
    while True:
        current_time = time()
        if current_time - start_time >= 15:
            start_time = current_time
            new_donos = tracker.get_new_donations()
            print(
                f"Number of new donations {new_donos[1][0]['message']} {json.dumps(new_donos[1], indent=4)}"
            )
            create_and_play_tts(
                new_donos[1][0]["message"], str(cachedir + "/"), new_donos[0]
            )
            print("done")
