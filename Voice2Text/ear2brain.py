import sys
import os
import json

# Add parent directory for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CommandParser.parser_main import process_command

# Try importing voice modules
try:
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False

def run_text_input():
    print("📝 Voice input disabled. Using typed input for testing.")
    print("Type commands like 'list files', 'make directory test', or 'copy file1 file2'. Type 'exit' to quit.\n")
    while True:
        command_text = input("Enter command: ")
        if command_text.lower() == "exit":
            break
        process_command(command_text)

def run_voice_input():
    sample_rate = 16000
    model_path = "/home/komal11/models/vosk-model-small-en-us-0.15"
    
    if not os.path.exists(model_path):
        print(f"❌ Vosk model not found at: {model_path}")
        sys.exit(1)

    print("🔊 Loading Vosk model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)

    print("🎧 Listening... Say a Linux command like 'list files' or 'make directory test'")

    try:
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
        ) as stream:
            while True:
                data, overflowed = stream.read(8000)
                if recognizer.AcceptWaveform(bytes(data)):
                    result = recognizer.Result()
                    text = json.loads(result)["text"]
                    if text:
                        print(f"\n🗣️ Recognized: {text}")
                        process_command(text)
    except Exception as e:
        print(f"⚠️ Audio input failed: {e}")
        print("Falling back to typed input.\n")
        run_text_input()

if __name__ == "__main__":
    if VOICE_ENABLED:
        run_voice_input()
    else:
        run_text_input()
