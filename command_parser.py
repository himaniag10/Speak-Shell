import re
import subprocess
import os
import platform
import psutil
import webbrowser
from rapidfuzz import fuzz
from datetime import datetime

class CommandParser:
    def __init__(self):
        self.system = platform.system()
        
        # Application paths for Windows
        self.app_paths = {
            'vscode': r'C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
        }
        
        # Command templates
        self.commands = {
            # File Operations
            'list_files': {
                'patterns': ['list files', 'show files', 'display files', 'ls', 'dir', 'what files'],
                'execute': self.list_files
            },
            'create_file': {
                'patterns': ['create file', 'make file', 'new file', 'touch'],
                'execute': self.create_file
            },
            'delete_file': {
                'patterns': ['delete file', 'remove file', 'delete', 'rm'],
                'execute': self.delete_file
            },
            'read_file': {
                'patterns': ['read file', 'show file', 'cat', 'open file', 'display file'],
                'execute': self.read_file
            },
            'copy_file': {
                'patterns': ['copy file', 'duplicate file', 'cp'],
                'execute': self.copy_file
            },
            'move_file': {
                'patterns': ['move file', 'mv', 'relocate file'],
                'execute': self.move_file
            },
            'rename_file': {
                'patterns': ['rename file', 'change name'],
                'execute': self.rename_file
            },
            
            # Directory Operations
            'change_directory': {
                'patterns': ['go to', 'change directory', 'cd', 'open folder', 'navigate to'],
                'execute': self.change_directory
            },
            'current_directory': {
                'patterns': ['where am i', 'current directory', 'pwd', 'current location', 'current folder'],
                'execute': self.current_directory
            },
            'create_directory': {
                'patterns': ['create folder', 'make directory', 'new folder', 'mkdir', 'create directory'],
                'execute': self.create_directory
            },
            'list_directory_tree': {
                'patterns': ['show tree', 'directory tree', 'folder structure', 'tree'],
                'execute': self.list_directory_tree
            },
            
            # Application Launch
            'open_application': {
                'patterns': ['open', 'launch', 'start', 'run application', 'open app'],
                'execute': self.open_application
            },
            'close_application': {
                'patterns': ['close', 'kill', 'stop', 'terminate'],
                'execute': self.close_application
            },
            
            # System Operations
            'system_info': {
                'patterns': ['system info', 'system information', 'pc info', 'computer info'],
                'execute': self.system_info
            },
            'disk_usage': {
                'patterns': ['disk space', 'storage', 'disk usage', 'free space'],
                'execute': self.disk_usage
            },
            'memory_usage': {
                'patterns': ['memory', 'ram usage', 'memory usage'],
                'execute': self.memory_usage
            },
            'cpu_usage': {
                'patterns': ['cpu', 'processor', 'cpu usage'],
                'execute': self.cpu_usage
            },
            'running_processes': {
                'patterns': ['processes', 'running programs', 'task list', 'show processes'],
                'execute': self.running_processes
            },
            
            # File Execution
            'execute_file': {
                'patterns': ['execute', 'run', 'run file', 'execute file', 'start file'],
                'execute': self.execute_file
            },
            
            # Web Operations
            'open_website': {
                'patterns': ['open website', 'browse', 'go to website', 'open url'],
                'execute': self.open_website
            },
            'search_web': {
                'patterns': ['search', 'google', 'search for', 'look up'],
                'execute': self.search_web
            },
            
            # Time & Date
            'get_time': {
                'patterns': ['time', 'what time', 'current time'],
                'execute': self.get_time
            },
            'get_date': {
                'patterns': ['date', 'what date', 'today'],
                'execute': self.get_date
            },
            
            # Power Operations
            'shutdown': {
                'patterns': ['shutdown', 'power off', 'turn off'],
                'execute': self.shutdown
            },
            'restart': {
                'patterns': ['restart', 'reboot'],
                'execute': self.restart
            },
            'sleep': {
                'patterns': ['sleep', 'hibernate'],
                'execute': self.sleep
            },
            
            # Volume Control
            'volume_up': {
                'patterns': ['volume up', 'increase volume', 'louder'],
                'execute': self.volume_up
            },
            'volume_down': {
                'patterns': ['volume down', 'decrease volume', 'quieter'],
                'execute': self.volume_down
            },
            'mute': {
                'patterns': ['mute', 'silence'],
                'execute': self.mute
            }
        }
    
    def parse(self, text):
        """Parse voice command and find best match"""
        text = text.lower().strip()
        
        best_match = None
        best_score = 0
        
        for cmd_name, cmd_data in self.commands.items():
            for pattern in cmd_data['patterns']:
                score = fuzz.partial_ratio(pattern, text)
                if score > best_score:
                    best_score = score
                    best_match = cmd_name
        
        if best_score > 60:
            return best_match, text
        else:
            return None, text
    
    def execute(self, command_name, full_text):
        """Execute the matched command"""
        if command_name in self.commands:
            return self.commands[command_name]['execute'](full_text)
        else:
            return False, "Command not recognized"
    
    # ============== FILE OPERATIONS ==============
    
    def list_files(self, text):
        try:
            files = os.listdir('.')
            if not files:
                return True, "Directory is empty"
            
            output = "Files and folders:\n"
            for item in files:
                if os.path.isdir(item):
                    output += f"📁 {item}\n"
                else:
                    size = os.path.getsize(item)
                    output += f"📄 {item} ({size} bytes)\n"
            return True, output
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def create_file(self, text):
        match = re.search(r'(?:named?|called)\s+(\S+)', text)
        if match:
            filename = match.group(1)
        else:
            words = text.split()
            filename = words[-1] if words else "newfile.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("")
            return True, f"File '{filename}' created successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_file(self, text):
        match = re.search(r'(?:file|named?)\s+(\S+)', text)
        if match:
            filename = match.group(1)
        else:
            words = text.split()
            filename = words[-1] if words else None
        
        if not filename:
            return False, "Please specify a filename"
        
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return True, f"File '{filename}' deleted"
            else:
                return False, f"File '{filename}' not found"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def read_file(self, text):
        match = re.search(r'(?:file|named?)\s+(\S+)', text)
        if match:
            filename = match.group(1)
        else:
            words = text.split()
            filename = words[-1] if words else None
        
        if not filename:
            return False, "Please specify a filename"
        
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    content = f.read()
                    if len(content) > 500:
                        content = content[:500] + "\n... (truncated)"
                return True, f"Content of '{filename}':\n{content}"
            else:
                return False, f"File '{filename}' not found"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def copy_file(self, text):
        match = re.search(r'(?:file\s+)?(\S+)\s+(?:to|as)\s+(\S+)', text)
        if match:
            source = match.group(1)
            dest = match.group(2)
        else:
            return False, "Please specify source and destination"
        
        try:
            import shutil
            shutil.copy2(source, dest)
            return True, f"Copied '{source}' to '{dest}'"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def move_file(self, text):
        match = re.search(r'(?:file\s+)?(\S+)\s+(?:to)\s+(\S+)', text)
        if match:
            source = match.group(1)
            dest = match.group(2)
        else:
            return False, "Please specify source and destination"
        
        try:
            import shutil
            shutil.move(source, dest)
            return True, f"Moved '{source}' to '{dest}'"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def rename_file(self, text):
        match = re.search(r'(?:file\s+)?(\S+)\s+(?:to|as)\s+(\S+)', text)
        if match:
            old_name = match.group(1)
            new_name = match.group(2)
        else:
            return False, "Please specify old and new names"
        
        try:
            os.rename(old_name, new_name)
            return True, f"Renamed '{old_name}' to '{new_name}'"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== DIRECTORY OPERATIONS ==============
    
    def change_directory(self, text):
        match = re.search(r'(?:to|directory)\s+(\S+)', text)
        if match:
            dirname = match.group(1)
        else:
            words = text.split()
            dirname = words[-1] if words else None
        
        if not dirname:
            return False, "Please specify a directory"
        
        try:
            os.chdir(dirname)
            return True, f"Changed to: {os.getcwd()}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def current_directory(self, text):
        try:
            cwd = os.getcwd()
            return True, f"Current directory: {cwd}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def create_directory(self, text):
        match = re.search(r'(?:named?|called)\s+(\S+)', text)
        if match:
            dirname = match.group(1)
        else:
            words = text.split()
            dirname = words[-1] if words else "newfolder"
        
        try:
            os.mkdir(dirname)
            return True, f"Directory '{dirname}' created"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def list_directory_tree(self, text):
        try:
            result = subprocess.run(['tree', '/F'], capture_output=True, text=True, shell=True)
            output = result.stdout[:1000]  # Limit output
            return True, f"Directory tree:\n{output}"
        except:
            return False, "Tree command not available"
    
    # ============== APPLICATION OPERATIONS ==============
    
    def open_application(self, text):
        # Extract app name
        app_name = None
        for app in self.app_paths.keys():
            if app in text.lower():
                app_name = app
                break
        
        if not app_name:
            return False, "Application not recognized. Try: vscode, notepad, calculator, chrome, etc."
        
        try:
            app_path = self.app_paths[app_name]
            
            # Expand user path if needed
            if '{}' in app_path:
                username = os.getenv('USERNAME')
                app_path = app_path.format(username)
            
            # Check if path exists or it's a system command
            if os.path.exists(app_path) or app_name in ['notepad', 'calc', 'calculator', 'mspaint', 'paint', 'explorer', 'cmd', 'powershell']:
                subprocess.Popen(app_path, shell=True)
                return True, f"Opening {app_name}"
            else:
                # Try as system command
                subprocess.Popen(app_name, shell=True)
                return True, f"Opening {app_name}"
        except Exception as e:
            return False, f"Could not open {app_name}: {str(e)}"
    
    def close_application(self, text):
        # Extract app name
        match = re.search(r'(?:close|kill|stop)\s+(\w+)', text)
        if match:
            app_name = match.group(1).lower()
        else:
            return False, "Please specify application to close"
        
        try:
            # Map common names to process names
            process_map = {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'vscode': 'Code.exe',
                'notepad': 'notepad.exe',
                'calculator': 'Calculator.exe',
                'paint': 'mspaint.exe'
            }
            
            process_name = process_map.get(app_name, f"{app_name}.exe")
            
            # Kill process
            subprocess.run(['taskkill', '/F', '/IM', process_name], capture_output=True)
            return True, f"Closed {app_name}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== SYSTEM OPERATIONS ==============
    
    def system_info(self, text):
        try:
            info = f"""System Information:
OS: {platform.system()} {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
Hostname: {platform.node()}"""
            return True, info
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def disk_usage(self, text):
        try:
            partitions = psutil.disk_partitions()
            output = "Disk Usage:\n"
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    output += f"{partition.device}: {usage.percent}% used ({usage.used // (1024**3)}GB / {usage.total // (1024**3)}GB)\n"
                except:
                    pass
            return True, output
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def memory_usage(self, text):
        try:
            mem = psutil.virtual_memory()
            output = f"""Memory Usage:
Total: {mem.total // (1024**3)} GB
Available: {mem.available // (1024**3)} GB
Used: {mem.used // (1024**3)} GB
Percentage: {mem.percent}%"""
            return True, output
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cpu_usage(self, text):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            output = f"""CPU Usage:
Cores: {cpu_count}
Usage: {cpu_percent}%"""
            return True, output
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def running_processes(self, text):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
            
            # Sort by CPU usage
            processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
            
            output = "Top 10 Processes:\n"
            for proc in processes:
                output += f"{proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}%\n"
            
            return True, output
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== FILE EXECUTION ==============
    
    def execute_file(self, text):
        # Extract filename
        match = re.search(r'(?:run|execute)\s+(\S+)', text)
        if match:
            filename = match.group(1)
        else:
            words = text.split()
            filename = words[-1] if words else None
        
        if not filename:
            return False, "Please specify a file to execute"
        
        try:
            if not os.path.exists(filename):
                return False, f"File '{filename}' not found"
            
            # Determine file type and execute accordingly
            ext = os.path.splitext(filename)[1].lower()
            
            if ext == '.py':
                result = subprocess.run(['python', filename], capture_output=True, text=True, timeout=10)
                return True, f"Output:\n{result.stdout}\n{result.stderr}"
            elif ext in ['.exe', '.bat', '.cmd']:
                subprocess.Popen(filename, shell=True)
                return True, f"Executing {filename}"
            elif ext == '.c':
                return False, "C files need to be compiled first"
            else:
                # Try to open with default program
                os.startfile(filename)
                return True, f"Opening {filename}"
        except subprocess.TimeoutExpired:
            return False, "Execution timeout"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== WEB OPERATIONS ==============
    
    def open_website(self, text):
        match = re.search(r'(?:open|go to|browse)\s+(?:website\s+)?(\S+)', text)
        if match:
            url = match.group(1)
            if not url.startswith('http'):
                url = 'https://' + url
        else:
            return False, "Please specify a website"
        
        try:
            webbrowser.open(url)
            return True, f"Opening {url}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def search_web(self, text):
        match = re.search(r'(?:search|google|look up)\s+(?:for\s+)?(.+)', text)
        if match:
            query = match.group(1)
        else:
            return False, "Please specify search query"
        
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return True, f"Searching for: {query}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== TIME & DATE ==============
    
    def get_time(self, text):
        try:
            current_time = datetime.now().strftime("%I:%M %p")
            return True, f"Current time: {current_time}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_date(self, text):
        try:
            current_date = datetime.now().strftime("%B %d, %Y")
            return True, f"Current date: {current_date}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== POWER OPERATIONS ==============
    
    def shutdown(self, text):
        return True, "Shutdown command disabled for safety. Use Windows menu to shutdown."
    
    def restart(self, text):
        return True, "Restart command disabled for safety. Use Windows menu to restart."
    
    def sleep(self, text):
        try:
            subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
            return True, "Putting system to sleep"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ============== VOLUME CONTROL ==============
    
    def volume_up(self, text):
        try:
            # Use nircmd or keyboard simulation
            return True, "Volume control requires additional setup (nircmd)"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def volume_down(self, text):
        return True, "Volume control requires additional setup (nircmd)"
    
    def mute(self, text):
        return True, "Mute control requires additional setup (nircmd)"


# ============== TEST/DEMO FUNCTION ==============
if __name__ == "__main__":
    print("=" * 60)
    print("COMMAND PARSER TEST - Voice OS")
    print("=" * 60)
    
    parser = CommandParser()
    
    # Test commands
    test_commands = [
        "list files",
        "create file named test.txt",
        "where am i",
        "open notepad",
        "system info",
        "memory usage",
        "what time is it",
        "search for python tutorials",
        "run demo.py"
    ]
    
    print("\nTesting command parsing and execution:\n")
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n[Test {i}] Command: \"{cmd}\"")
        print("-" * 60)
        
        # Parse
        command_name, full_text = parser.parse(cmd)
        
        if command_name:
            print(f"✓ Matched: {command_name}")
            
            # Execute
            success, output = parser.execute(command_name, full_text)
            
            if success:
                print(f"✓ Result: {output}")
            else:
                print(f"✗ Error: {output}")
        else:
            print(f"✗ No command matched for: {cmd}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    
    # Interactive mode
    print("\n[Interactive Mode] - Type commands to test (type 'exit' to quit)")
    print("Example: list files, open notepad, system info, etc.\n")
    
    while True:
        try:
            user_input = input("🎤 Command: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            command_name, full_text = parser.parse(user_input)
            
            if command_name:
                print(f"   Executing: {command_name}")
                success, output = parser.execute(command_name, full_text)
                
                if success:
                    print(f"   {output}\n")
                else:
                    print(f"   {output}\n")
            else:
                print(f"   Command not recognized\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"    Error: {str(e)}\n")