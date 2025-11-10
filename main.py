import threading
from voice_recognition import VoiceRecognizer
from text_to_speech import Speaker
from command_parser import CommandParser
from gui import VoiceOSGUI

class VoiceOS:
    def __init__(self):
        self.gui = VoiceOSGUI()
        self.recognizer = VoiceRecognizer()
        self.speaker = Speaker()
        self.parser = CommandParser()
        self.running = True
    
    def voice_loop(self):
        """Main voice recognition loop"""
        self.gui.append_output("\n[System Ready] Start speaking commands...\n")
        self.speaker.speak("Voice OS is ready")
        
        while self.running:
            try:
                # Update status
                self.gui.set_status("Listening...", '#00ff00')
                
                # Listen for command
                text = self.recognizer.listen()
                
                if not text:
                    continue
                
                # Display what was heard
                self.gui.append_output(f"\n You said: {text}")
                
                # Check for exit command
                if "exit" in text.lower() or "quit" in text.lower():
                    self.gui.append_output("\n[System] Shutting down...")
                    self.speaker.speak("Goodbye")
                    self.running = False
                    self.gui.root.quit()
                    break
                
                # Update status
                self.gui.set_status(" Processing...", '#ffff00')
                
                # Parse command
                command_name, full_text = self.parser.parse(text)
                
                if command_name:
                    # Execute command
                    self.gui.append_output(f"Executing: {command_name}")
                    success, output = self.parser.execute(command_name, full_text)
                    
                    # Display output
                    if success:
                        self.gui.append_output(f" {output}")
                        self.speaker.speak("Command executed successfully")
                    else:
                        self.gui.append_output(f" {output}")
                        self.speaker.speak("Command failed")
                else:
                    self.gui.append_output(" Command not recognized")
                    self.speaker.speak("Sorry, I didn't understand that command")
                
            except Exception as e:
                self.gui.append_output(f" Error: {str(e)}")
                self.gui.set_status(" Error occurred", '#ff0000')
        
    def start(self):
        """Start the Voice OS"""
        # Run voice loop in separate thread
        voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
        voice_thread.start()
        
        # Start GUI (blocking)
        self.gui.run()

if __name__ == "__main__":
    voice_os = VoiceOS()
    voice_os.start()