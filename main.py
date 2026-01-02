import os
import time
import subprocess

import pyperclip
from Xlib import X, display, XK
from Xlib.ext import xtest
from dotenv import load_dotenv
import spotipy
from llama_cpp import Llama
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def generate_announcement_prompt(track_name, artist_names):
    station_name = os.getenv("RADIO_NAME", "Gamedio FM")
    station_description = os.getenv("RADIO_DESCRIPTION", "Your ultimate gaming companion")
    
    prompt = (
        f"<|system|>\n"
        f"You are a radio station announcer. Generate a very short, upbeat announcement. "
        f"Include the station name, description, and the currently playing song. "
        f"Format it as a radio shout-out. Keep it to one sentence.<|end|>\n"
        f"<|user|>\n"
        f"Station: {station_name}\n"
        f"Description: {station_description}\n"
        f"Currently playing: {track_name} by {artist_names}<|end|>\n"
        f"<|assistant|>\n"
    )
    return prompt

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

def simulate_broadcast():
    d = display.Display()
    
    def send_key(keysym, modifiers=[]):
        keycode = d.keysym_to_keycode(keysym)
        
        for mod in modifiers:
            xtest.fake_input(d, X.KeyPress, d.keysym_to_keycode(mod))
        
        xtest.fake_input(d, X.KeyPress, keycode)
        xtest.fake_input(d, X.KeyRelease, keycode)
        
        # Release modifiers (in reverse order)
        for mod in reversed(modifiers):
            xtest.fake_input(d, X.KeyRelease, d.keysym_to_keycode(mod))
        
        d.sync()

    time.sleep(0.5)
    
    send_key(XK.XK_Return)
    time.sleep(0.2)
    
    send_key(XK.XK_v, modifiers=[XK.XK_Control_L])
    time.sleep(0.2)
    
    send_key(XK.XK_Return)
    d.close()


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

    llm = Llama(
        model_path=f"./models/{os.getenv('LLM')}",
        n_gpu_layers=-1,
        n_ctx=200,
        flash_attn=True,
        n_threads=os.cpu_count(),
        verbose=True
    )

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
            
            prompt = generate_announcement_prompt(track_name, artist_names)

            response = llm(
                prompt,
                max_tokens=200,
                temperature=0.1,
                top_p=0.9,
                repeat_penalty=1.1,
            )
            text_response = response["choices"][0]["text"].strip().replace('"', '')
            print(text_response)

            pyperclip.copy(text_response)
            simulate_broadcast()

        else:
            print("No track is currently playing.")

        time.sleep(180)


if __name__ == "__main__":
    main()