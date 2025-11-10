import tkinter as tk
from tkinter import scrolledtext
import threading

class VoiceOSGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice OS Terminal")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="🎤 Ready to listen...",
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Consolas', 14, 'bold')
        )
        self.status_label.pack(pady=10)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            bg='#0c0c0c',
            fg='#00ff00',
            font=('Consolas', 11),
            insertbackground='white',
            wrap=tk.WORD
        )
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Make it read-only
        self.output_text.config(state=tk.DISABLED)
        
        # Welcome message
        self.append_output("=" * 50)
        self.append_output("VOICE-BASED OPERATING SYSTEM")
        self.append_output("=" * 50)
        self.append_output("\nSpeak commands to control the system")
        self.append_output("Say 'exit' or 'quit' to close\n")
        self.append_output("=" * 50 + "\n")
    
    def append_output(self, text):
        """Append text to output area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def set_status(self, text, color='#00ff00'):
        """Update status label"""
        self.status_label.config(text=text, fg=color)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

# Test it
if __name__ == "__main__":
    gui = VoiceOSGUI()
    
    # Simulate some output
    import time
    def simulate():
        time.sleep(2)
        gui.append_output("You: list files")
        gui.set_status("🔄 Processing...", '#ffff00')
        time.sleep(1)
        gui.append_output("Executing: ls")
        gui.append_output("test.txt\ndemo.py\nREADME.md")
        gui.set_status("🎤 Listening...", '#00ff00')
    
    thread = threading.Thread(target=simulate, daemon=True)
    thread.start()
    
    gui.run()