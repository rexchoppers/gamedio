import os
import time
import subprocess

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def play_beep():
    sound_paths = [
        "/usr/share/sounds/freedesktop/stereo/bell.oga",
        "/usr/share/sounds/freedesktop/stereo/message-new-instant.oga",
        "/usr/share/sounds/gnome/default/alerts/glass.ogg",
    ]
    
    for path in sound_paths:
        if os.path.exists(path):
            try:
                subprocess.run(["paplay", path], check=False, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass
    
    print("\a", end="", flush=True)

def main():
    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=spotify_redirect_uri,
        scope="user-library-read,user-read-currently-playing,user-read-playback-state",
    ))

    while True:
        for i in range(3, 0, -1):
            print(f"Countdown: {i}")
            play_beep()
            time.sleep(1)

        results = sp.current_user_playing_track()
        if results is not None and results['is_playing']:
            track = results['item']
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            track_name = track['name']
            print(f"Currently playing: {track_name} by {artist_names}")
        else:
            print("No track is currently playing.")

        play_beep()

        time.sleep(5)


if __name__ == "__main__":
    main()