import vosk
import sounddevice as sd
import json
import queue

class VoiceRecognizer:
    def __init__(self, model_path="model"):
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.audio_queue = queue.Queue()
        
    def audio_callback(self, indata, frames, time, status):
        """Called for each audio block"""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def listen(self):
        """Start listening and return recognized text"""
        print("🎤 Listening... (Speak now)")
        
        with sd.RawInputStream(samplerate=16000, blocksize=8000, 
                               dtype='int16', channels=1, 
                               callback=self.audio_callback):
            
            while True:
                data = self.audio_queue.get()
                
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    
                    if text:
                        return text
                else:
                    # Partial result (optional, for real-time feedback)
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get('partial', '')
                    if partial_text:
                        print(f"Hearing: {partial_text}", end='\r')

# Test it
if __name__ == "__main__":
    recognizer = VoiceRecognizer()
    
    while True:
        text = recognizer.listen()
        print(f"\n✅ You said: {text}")
        
        if "exit" in text or "quit" in text:
            print("Goodbye!")
            break