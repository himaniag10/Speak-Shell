import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# This is a placeholder function for Himani's module
def process_command(command_text):
    print(f"MSP --->Himani: '{command_text}' to Himani's module.")
    # Here, you would call Himani's function to parse and execute the command.
    # We will replace this with the actual function later.

# Define audio parameters
sample_rate = 16000
device_id = 1  # Use your microphone's device ID

# Load the Vosk model
model_path = r"C:\Users\rey27\Downloads\vosk-model-en-in-0.5"
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
        if recognizer.AcceptWaveform(bytes(data)):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            if text:
                process_command(text)
