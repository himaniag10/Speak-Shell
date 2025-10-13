from CommandParser.command_executor import execute_linux_command

def process_command(command_text):
    """
    Convert natural language commands into Linux commands
    and execute them.
    """
    command_text = command_text.lower().strip()
    words = command_text.split()

    # Natural language mappings
    NLP_COMMANDS = {
        "list files": ["ls"],
        "current directory": ["pwd"],
        "make directory": ["mkdir"],
        "remove directory": ["rm"],
        "remove file": ["rm"],
        "change directory":["cd"],
        "make file":["touch"],
    }

    # Match NLP commands
    for phrase, cmd_list in NLP_COMMANDS.items():
        if command_text.startswith(phrase):
            args = words[len(phrase.split()):]  # anything after phrase
            execute_linux_command(cmd_list[0], cmd_list[1:] + args)
            return

    # Fallback: treat as literal Linux command
    if words:
        cmd = words[0]
        args = words[1:]
        execute_linux_command(cmd, args)
    else:
        print("⚠️ Command not recognized.")
