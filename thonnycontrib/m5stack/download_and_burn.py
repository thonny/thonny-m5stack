import sys
import ast
import os.path
from urllib.request import urlretrieve
import subprocess

BASE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "M5FirmwaresForThonny")
BASE_URL = "https://thonny.org/m5stack/firmwares"
port, baud, name, spec = sys.argv
spec = ast.literal_eval(spec)


def check_download(relative_path):
    full_path = os.path.join(BASE_DIR, relative_path)
    full_url = BASE_URL + "/" + relative_path.replace("\\", "/")
    
    if os.path.exists(full_path):
        print(relative_path, "already downloaded in", BASE_DIR)
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        print("Downloading", relative_path, "from", BASE_URL)
        print("0%", end="")
        
        milestones = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]    
        def on_download_progress(blocknum, bs, size): 
            percent_done = int((blocknum * bs) / size * 100)    
            while milestones and percent_done >= milestones[0]:
                milestone = milestones.pop(0)
                print("%d ... " % milestone, end="")
                
        urlretrieve(full_url, full_path, on_download_progress)

# Prepare
prepared_commands = []
for command_template in spec["commands"]:
    parts = command_template.split()
    for i, part in enumerate(parts):
        if part == "%port":
            parts[i] = port
        elif part == "%baud":
            parts[i] = baud
        elif part.startswith("%PATH"):
            parts[i] = (part.replace("%PATH", spec["path"])
                            .replace("/", os.path.sep)
                            .replace("\\", os.path.sep))
            check_download(parts[i])
            
    prepared_commands.append(parts)

# Execute
for cmd in prepared_commands:
    print("esptool", " ".join(cmd)) 
    proc = subprocess.Popen([sys.executable, "-m", "esptool"] + cmd, cwd=BASE_DIR, 
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE,
                            errors="replace")
    
    while True:
        out = proc.stdout.read(1)
        if out == "" and proc.poll() is not None:
            break
        if out != "":
            print(out, end="")
    