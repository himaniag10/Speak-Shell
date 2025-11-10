# SpeakShell-Voice-Based Operating System

Control your computer using voice commands. Offline, secure, and natural language powered.

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/voice-os.git
cd voice-os

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install vosk sounddevice pyttsx3 numpy rapidfuzz psutil

# Download Vosk model (40MB)
# https://alphacephei.com/vosk/models
# Extract to voice_os/model/

# Run application
python main.py
```

---

##  Features

- **40+ Voice Commands** - File management, app control, system monitoring
- **Offline Recognition** - Privacy-focused using Vosk
- **Natural Language** - "create file named test" or "make a file test"
- **Real-time Feedback** - Visual GUI + audio confirmation
- **Cross-Platform** - Windows 10/11 support

---

## Command Examples

```
File Operations:
  "list files"
  "create file named test.txt"
  "delete file demo.py"
  "copy file source.txt to backup.txt"

Applications:
  "open notepad"
  "open vscode"
  "open calculator"
  "close chrome"

System:
  "memory usage"
  "cpu usage"
  "disk space"
  "what time is it"

Navigation:
  "where am i"
  "go to documents"
  "create folder projects"

Web:
  "open website google.com"
  "search for python tutorials"

Execution:
  "run demo.py"
  "execute script.bat"

Exit:
  "exit" or "quit"
```

---

## 🏗️ Architecture

```
┌──────────────────────────┐
│   Voice Input (Vosk)     │  ← Microphone
└──────────┬───────────────┘
           │ "create file test.txt"
┌──────────▼───────────────┐
│   NLP Parser (rapidfuzz) │  ← Command matching
└──────────┬───────────────┘
           │ (command_name, params)
┌──────────▼───────────────┐
│   OS Executor (subprocess)│ ← System calls
└──────────┬───────────────┘
           │ (success, output)
┌──────────▼───────────────┐
│   GUI + TTS Feedback     │  ← User sees/hears result
└──────────────────────────┘
```

---

##  Project Structure

```
voice_os/
├── model/                    # Vosk speech model
├── main.py                   # Main application
├── voice_recognition.py      # Speech-to-text
├── command_parser.py         # NLP + command logic
├── text_to_speech.py         # Audio feedback
├── gui.py                    # Terminal interface
└── test_audio.py             # Audio setup test
```

---

##  Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Speech-to-Text | Vosk (offline) |
| Audio I/O | sounddevice |
| NLP | rapidfuzz |
| Text-to-Speech | pyttsx3 |
| System Ops | subprocess, os, psutil |
| GUI | tkinter |

---

##  Troubleshooting

**Microphone not detected:**
```python
# Run test_audio.py to list devices
python test_audio.py
# Note your device ID and set in code
```

**WSL audio not working:**
- Run on native Windows Python (not WSL)
- WSL doesn't support audio devices

**Bluetooth headphones:**
- Connect in Windows settings first
- Run test_audio.py to verify

**Commands not recognized:**
- Speak clearly and slowly
- Check microphone volume in Windows
- Try exact command phrases from examples

**Import errors:**
```bash
pip install vosk sounddevice pyttsx3 numpy rapidfuzz psutil
```

---

##  Key Highlights

**OS-Based Project:**
- Direct system calls (fork/exec, open/read/write)
- Process management & scheduling
- File system manipulation
- Memory & CPU monitoring via kernel APIs
- Device I/O (microphone/speakers)
- Shell-like command interpretation

**Security:**
- Disabled destructive power commands
- File operation confirmations
- No cloud dependency (offline)

---

##  Future Scope

- AI models (BERT/GPT) for context awareness
- Voice biometric authentication
- Multi-language support (Hindi, Spanish)
- Mobile apps (Android/iOS)
- Docker container management
- Predictive command suggestions
- Cloud sync across devices

---

##  Requirements

**Hardware:**
- Microphone or Bluetooth headphones
- 4GB RAM minimum
- 500MB disk space

**Software:**
- Python 3.10+
- Windows 10/11

---

## License

MIT License - Feel free to use and modify

---

##  Contributors

[Himani Agarwal (@himaniag10)] - Developer

---

## Acknowledgments

- Vosk team for offline speech recognition
- Python community for excellent libraries

---

**Quick Commands Cheat Sheet:**

```
Files: list | create | delete | read | copy | move | rename
Folders: where am i | go to | create folder
Apps: open [notepad|vscode|calculator|chrome]
System: memory | cpu | disk space | time | date
Web: open website | search for
Execute: run | execute
Exit: exit | quit
```
