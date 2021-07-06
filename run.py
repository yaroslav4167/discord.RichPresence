import random
import time

import pyautogui
from pypresence import Presence

from configmanager import ConfigManager

try:
    # Logo Initialize
    try:
        with open("logo.yml", "r", encoding="utf8") as logo:
            data = logo.read()
            print(data)
    except FileNotFoundError:
        print("\033[33m{}".format("Logo file not found!\nSkipped."))
finally:
    print("Injecting. . .\n##########################################################")

settings = ConfigManager()

while True:

    client_id = settings.get("application_id")
    start_time = int(time.time())
    try:
        if not settings.get("application_id"):
            print("\033[31m{}".format("Please, check and correct your application_id in file settings.ini!"))
            exit()
        else:
            try:
                RPC = Presence(client_id)  # Initialize the Presence class
                RPC.connect()
            except TimeoutError:
                print("Token error!")

        while True:
            try:
                buttons_list = [
                    {
                        "label": random.choice(settings.get("first_button_layer_1_text")),
                        "url": random.choice(settings.get("first_button_layer_1_url"))},
                    {
                        "label": random.choice(settings.get("second_button_layer_1_text")),
                        "url": random.choice(settings.get("second_button_layer_1_url"))}
                ]
                RPC.update(
                    # start=start_time,
                    large_text=random.choice(settings.get("quotes_large_image_text")),
                    small_text=random.choice(settings.get("quotes_small_image_text")),
                    large_image=random.choice(settings.get("quotes_large_image")),
                    small_image=random.choice(settings.get("window_error_small_image")),
                    buttons=buttons_list,
                    details="Change everything you are",
                    state="And everything you were..."
                )
                time.sleep(int(settings.get("next_layer_time")))
                try:
                    current = pyautogui.getActiveWindowTitle()
                    activity_details = ""
                    last = None
                    # for browsers in range(len(web_browsers)):
                    #    if str(web_browsers) in current:
                    #        activity_details = "Web-Surfing:"
                    if "Discord" in current:
                        activity_details = "In Discord | Watching:"
                    else:
                        activity_details = "Current Activity:"
                    if len(current) >= 128:
                        continue
                    if current != last:
                        RPC.update(
                            start=start_time,
                            large_text=random.choice(settings.get("quotes_large_image_text")),
                            small_text=random.choice(settings.get("quotes_small_image_text")),
                            large_image=random.choice(settings.get("quotes_large_image")),
                            small_image=random.choice(settings.get("quotes_small_image")),
                            # party_size=[666, 666],
                            buttons=buttons_list,
                            details=activity_details,
                            state=f"{str(current)}",
                            instance=False
                        )
                        time.sleep(int(settings.get("next_layer_time")))
                except Exception as e:
                    print("[EXCEPTION] " + repr(e))
                    print("Window layer error.")
                    #
                    # Activity Layer WindowERROR
                    #
                    RPC.update(
                        start=start_time,
                        large_text=random.choice(settings.get("window_error_large_text")),
                        small_text=random.choice(settings.get("quotes_small_image_text")),
                        large_image=random.choice(settings.get("window_error_large_image")),
                        small_image="profile_image",
                        # party_size=[666, 666],
                        buttons=buttons_list,
                        details="Coffee Time ☕",
                        state="Do not disturb!"
                    )
                time.sleep(int(settings["GeneralSettings"]["next_layer_time"]))
                #
                # Activity Layer #3
                #
                l3_buttons_list = [
                    {
                        "label": random.choice(settings.get("first_button_layer_2_text")),
                        "url": random.choice(settings.get("first_button_layer_2_url"))
                    },
                ]
                RPC.update(
                    # start=start_time,
                    large_text="𝓜𝓮𝓽𝓪  𝓟𝓮𝓪𝓬𝓮  𝓣𝓮𝓪𝓶®",
                    small_text="𝓨𝓾𝓴𝓴𝓲 - Developer's Bot",
                    large_image='yukki_server_avatar_1024x1024',
                    small_image='yukki_512x512_image',
                    # party_size=[666, 666],
                    buttons=l3_buttons_list,
                    details="☚ 𝕸𝖞 𝕯𝖎𝖘𝖈𝖔𝖗𝖉 𝕾𝖊𝖗𝖛𝖊𝖗",
                    state="⠀⠀ ⠀⠀𝕵𝖔𝖎𝖓 𝖚𝖘!"
                )
                time.sleep(int(settings["GeneralSettings"]["next_layer_time"]))
            #
            # Exception to check if discord is dropped
            #
            except Exception as e:
                print("\nActivity Status Error!")
                break
    #
    # General Library Exception and check if discord is not running
    #
    except Exception as e:
        print(
            "Discord process error!\n"
            "Retry connecting via " +
            str(settings.get("reloading_after_exception_time"))
            + " seconds...\n"
              ". . . ")
        time.sleep(int(settings.get("reloading_after_exception_time")))
        try:
            RPC = Presence(client_id)
            RPC.connect()
            time.sleep(int(settings.get("reloading_after_exception_time")))
        except:
            continue
