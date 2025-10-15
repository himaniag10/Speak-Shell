import os
import subprocess
import pyttsx3
import shutil

# Initialize pyttsx3 safely
try:
    engine = pyttsx3.init()
    engine.setProperty("voice", "en-us")  # use en-us or default
except Exception as e:
    print(f"⚠️ pyttsx3 init failed: {e}")
    engine = None


def speak(text):
    """Speaks text using pyttsx3, or prints if TTS fails."""
    print(f"🗣️ {text}")
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ TTS failed: {e}")


def execute_linux_command(cmd, args):
    """Executes Linux/desktop commands safely."""
    try:
        # Basic Linux commands
        if cmd in ["ls", "pwd", "whoami", "date", "ps"]:
            output = subprocess.getoutput(" ".join([cmd] + args))
            print(output)
            speak("Command executed successfully.")

        # Make directory
        elif cmd == "mkdir":
            if args:
                os.mkdir(args[0])
                speak(f"Directory {args[0]} created successfully.")
            else:
                speak("Please specify a directory name.")

        # Remove file or directory
        elif cmd == "rm":
            if args:
                target = args[0]
                speak(f"Do you really want to delete {target}?")
                confirm = input("Type 'yes' to confirm: ")
                if confirm.lower() == "yes":
                    try:
                        if os.path.isfile(target):
                            os.remove(target)
                            speak(f"File {target} deleted successfully.")
                        elif os.path.isdir(target):
                            shutil.rmtree(target)
                            speak(f"Directory {target} deleted successfully.")
                        else:
                            speak(f"{target} does not exist.")
                    except Exception as e:
                        print(f"⚠️ Error: {e}")
                        speak("There was an error executing the command.")
                else:
                    speak("Deletion cancelled.")
            else:
                speak("Please specify a file or directory name.")

        # Change directory
        elif cmd == "cd":
            if args:
                os.chdir(args[0])
                speak(f"Changed directory to {args[0]}.")
            else:
                speak("Please specify a directory name.")

        # Open desktop apps
        elif cmd in ["firefox", "code", "gedit", "chrome"]:
            subprocess.Popen([cmd])
            speak(f"Opening {cmd}")

        # System commands
        elif cmd in ["shutdown", "reboot"]:
            subprocess.run([cmd])
            speak(f"System {cmd} initiated.")

        # Clear screen
        elif cmd == "clear":
            os.system("clear")
            speak("Screen cleared.")

        # Copy and move files
        elif cmd == "copy":
            if len(args) >= 2:
                subprocess.run(["cp", args[0], args[1]])
                speak(f"Copied {args[0]} to {args[1]}")
            else:
                speak("Please specify source and destination files.")

        elif cmd == "move":
            if len(args) >= 2:
                subprocess.run(["mv", args[0], args[1]])
                speak(f"Moved {args[0]} to {args[1]}")
            else:
                speak("Please specify source and destination.")

        # Fallback for other commands
        else:
            output = subprocess.getoutput(" ".join([cmd] + args))
            print(output)
            speak("Executed your command.")

    except Exception as e:
        print(f"⚠️ Error: {e}")
        speak("There was an error executing the command.")
