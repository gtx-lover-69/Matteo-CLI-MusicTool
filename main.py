import os
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from colorama import Fore, Style
import random


def shuffle(folder, audio_files):
    shuffled = audio_files[:]
    random.shuffle(shuffled)

    track_index = 0
    while track_index < len(shuffled):
        song = shuffled[track_index]
        filename = os.path.join(folder, song)
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            print(f"Playing {song}")
        except pygame.error:
            track_index += 1
            continue

        print("N - Next")
        print("B - Previous")
        print("P - Pause")
        print("R - Resume")
        print("Q - Quit")

        state = "playing"
        advance = 1
        while True:
            control = input("> ").upper().strip()
            if control == "P":
                if state == "playing":
                    pygame.mixer.music.pause()
                    print("Paused")
                    state = "paused"
                else:
                    print("Already paused!")
            elif control == "R":
                if state == "paused":
                    pygame.mixer.music.unpause()
                    print("Playing")
                    state = "playing"
                else:
                    print("Already playing")
            elif control == "Q":
                pygame.mixer.music.stop()
                print("Stopped")
                time.sleep(1)
                return
            elif control == "N":
                pygame.mixer.music.stop()
                advance = 1
                break
            elif control == "B":
                pygame.mixer.music.stop()
                advance = -1
                break
            else:
                print("Invalid command")

        track_index = (track_index + advance) % len(shuffled)


def playmusic(folder, song_name):

    filename = os.path.join(folder, song_name)

    if not os.path.exists(filename):
        print(f"File '{filename}' not found!")
        time.sleep(1)
        return

    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Playback error: {e}")
        time.sleep(1)
        return

    print(f"Now playing: {song_name}")

    print("P - Pause")
    print("R - Resume")
    print("Q - Quit")

    state = "playing"
    while True:
        control = input("> ").upper().strip()
        if control == "P":
            if state == "playing":
                pygame.mixer.music.pause()
                print("Paused")
                state = "paused"
            else:
                print("Already paused!")
        elif control == "R":
            if state == "paused":
                pygame.mixer.music.unpause()
                print("Playing")
                state = "playing"
            else:
                print("Already playing")
        elif control == "Q":
            pygame.mixer.music.stop()
            print("Stopped")
            time.sleep(1)
            return
        else:
            print("Invalid command")
            time.sleep(1)

def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(Fore.RED + "Audio initialisation failed! ", e, Style.RESET_ALL)
        return

    while True:
        folder = input("Enter the music folder name: ")
        if os.path.isdir(folder):
            break
        print(Fore.RED + Style.BRIGHT + f"Folder '{folder}' not found!" + Style.RESET_ALL)

    audio_files = [file for file in os.listdir(folder) if file.endswith((".mp3",".wav"))]

    if not audio_files:
        print(f"No mp3 files found in folder {folder}")

    while True:
        print(Fore.BLUE + Style.BRIGHT + "Matteo's CLI MusicTool" + Style.RESET_ALL)
        print(Style.BRIGHT + "Main menu" + Style.RESET_ALL)
        menuchoice = input("""    1 - View song list
    2 - Shuffle songs
    3 - View Changelog
    0 - Exit
    """)
        if menuchoice.strip() == "1":
            print(Style.BRIGHT + f"{len(audio_files)} songs loaded" + Style.RESET_ALL)
            page = 1
            pagesize = 10
            totalpages = (len(audio_files) + pagesize - 1) // pagesize

            while True:
                start = (page - 1) * pagesize
                end = start + pagesize

                for index, song in enumerate(audio_files[start:end], start = start + 1):
                    print(Style.BRIGHT + f"{index}." + Style.RESET_ALL + song)

                print(Style.BRIGHT + f"Page [{page}/{totalpages}]" + Style.RESET_ALL)
                print("N - Next, P - Previous, M - Main menu, or enter a song number")

                choice = input("> ").upper().strip()

                if choice == "N":
                    if page < totalpages:
                        page += 1
                    else:
                        print("Already on the last page!")
                elif choice == "P":
                    if page > 1:
                        page -= 1
                    else:
                        print("Already on the first page!")
                elif choice == "M":
                    print("Alright!")
                    time.sleep(1)
                    break

                elif choice.isdigit():
                    int_choice = int(choice) - 1
                    if 0 <= int_choice < len(audio_files):
                        playmusic(folder, audio_files[int_choice])
                        break
                    else:
                        print("Please enter a valid number!")
                        time.sleep(1)

                else:
                    print("Please enter a valid number!")
                    time.sleep(1)
                    continue

        elif menuchoice.strip() == "2":
            shuffle(folder, audio_files)

        elif menuchoice.strip() == "3":
            print(Style.BRIGHT + "Changlelog" + Style.RESET_ALL)
            print("v0.1 - only shows a list of all songs, and supports just mp3")
            print("v0.2 - increased support for wav")
            print("v0.3 - added shuffle mode")
            print("""v1.0 - improved corrupted song skipping and detection,
       added skip and back controls, squashed bugs, optimised""")
            input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back")

        elif menuchoice.strip() == "0":
            print("Until next time!")
            break

        else:
            print("Invalid command!")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()