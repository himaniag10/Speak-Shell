# CommandParser/fuzzy_matcher.py

from rapidfuzz import process

COMMANDS = [
    "ls", "mkdir", "rm", "cd", "pwd", "whoami", "date", "ps",
    "firefox", "chrome", "code", "gedit", "shutdown", "reboot",
    "copy", "move", "clear"
]

def fuzzy_match(word):
    """
    Finds the closest matching command to the recognized word.
    Returns the best match if score > 70, else None.
    """
    match, score, _ = process.extractOne(word, COMMANDS)
    return match if score > 70 else None
