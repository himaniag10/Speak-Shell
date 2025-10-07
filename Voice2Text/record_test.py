import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

fs = 44100  # Sample rate
duration = 5  # Duration of recording in seconds
device_id = 1 # Replace with your microphone's ID

print("Recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, device=device_id)
sd.wait()  # Wait until recording is finished
print("Recording finished.")

# Save the recorded data as a WAV file
write('output.wav', fs, myrecording)

print("Audio saved to output.wav")
