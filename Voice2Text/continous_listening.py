import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# Define audio parameters
sample_rate = 16000
device_id = 1  # Use your microphone's device ID

# Load the Vosk model
model_path = r"C:\Users\rey27\Downloads\vosk-model-en-in-0.5" # Your model path
model = Model(model_path)
recognizer = KaldiRecognizer(model, sample_rate)

print("Listening for commands...")

with sd.RawInputStream(
    samplerate=sample_rate,
    blocksize=8000,
    device=device_id,
    dtype="int16",
    channels=1,
) as stream:
    while True:
        data, overflowed = stream.read(8000)
        # Convert the buffer object to a bytes object
        if recognizer.AcceptWaveform(bytes(data)):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text:
                print(f"Recognized: {text}")
