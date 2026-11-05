import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS

# Load the Turbo model (use device="cpu" if you lack a dedicated GPU)
model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# The text to synthesize, including optional emotion tags
text = "Hi there! [chuckle] I'm generating this voice entirely locally."

# Generate the audio using your reference clip
wav = model.generate(text, audio_prompt_path="ref.wav")

# Save the output file
ta.save("output_cloned.wav", wav, model.sr)
print("Audio saved successfully!")
