import sounddevice as sd

# List all audio devices
print("Available Audio Devices:")
print(sd.query_devices())

# Test recording
print("\nRecording for 3 seconds... Speak now!")
duration = 3
recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
sd.wait()
print("Recording complete!")

# Test playback
print("Playing back...")
sd.play(recording, 16000)
sd.wait()
print("Done!")