import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # Set properties
        self.engine.setProperty('rate', 165)    # Speed
        self.engine.setProperty('volume', 1.0)   # Volume (0-1)
        
        # Optional: Change voice (0 = male, 1 = female usually)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Speak the given text"""
        print(f"🔊 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# Test it
if __name__ == "__main__":
    speaker = Speaker()
    speaker.speak("Hello, I am your voice based operating system")
    speaker.speak("I can execute commands for you")