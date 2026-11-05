import io
import requests
import soundfile as sf
import sounddevice as sd

# The URL of your running FastAPI server
API_URL = "http://localhost:8000/generate"

def generate_and_play(text: str):
    print(f"Sending request to server: '{text}'")
    
    # 1. Send the request to the server
    response = requests.post(
        API_URL, 
        data={"text": text}
    )
    
    if response.status_code == 200:
        print("Audio received! Playing...")
        
        # 2. Load the raw bytes into a virtual in-memory file
        audio_bytes = io.BytesIO(response.content)
        
        # 3. Read the virtual file into a NumPy array
        audio_data, samplerate = sf.read(audio_bytes)
        
        # 4. Play the audio directly
        sd.play(audio_data, samplerate)
        sd.wait() # Keep the script alive until playback finishes
        
        print("Playback finished.")
    else:
        print(f"Server returned an error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Test the client
    generate_and_play("Hello from the client! I'm streaming this directly from the server's memory.")
