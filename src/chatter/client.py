import argparse
import io

import requests
import sounddevice as sd
import soundfile as sf

# The URL of your running FastAPI server
API_URL = "http://localhost:8000/generate"


def generate_and_play(text: str):
    print(f"Sending request to server: '{text}'")

    # 1. Send the request to the server
    response = requests.post(API_URL, data={"text": text})

    if response.status_code == 200:
        print("Audio received! Playing...")

        # 2. Load the raw bytes into a virtual in-memory file
        audio_bytes = io.BytesIO(response.content)

        # 3. Read the virtual file into a NumPy array
        audio_data, samplerate = sf.read(audio_bytes)

        # 4. Play the audio directly
        sd.play(audio_data, samplerate)
        sd.wait()  # Keep the script alive until playback finishes

        print("Playback finished.")
    else:
        print(f"Server returned an error: {response.status_code}")
        print(response.text)


def main():
    parser = argparse.ArgumentParser(description="Chatter TTS Client")
    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        default=
        "Hello from the client! I'm streaming this directly from the server's memory.",
        help="The text you want the server to synthesize into speech.")
    args = parser.parse_args()

    generate_and_play(args.text)


if __name__ == "__main__":
    main()
