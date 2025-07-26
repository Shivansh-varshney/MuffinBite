import os
import sys
import csv
import subprocess
from pathlib import Path

env_dir = Path("environment")
dirs_to_create = ["Attachments", "DataFiles", "EmailStatus", "logs"]
requirements_file = "requirements.txt"
file_names = ['successful_emails.csv', 'failed_emails.csv']

def log_error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)

def create_virtualenv():
    if not env_dir.exists():
        print("\nCreating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(env_dir)])
    else:
        print("\nVirtual environment already exists.")

def install_requirements():
    print("\nInstalling dependencies...")

    with open(requirements_file) as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    pip_path = env_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
    subprocess.check_call([str(pip_path), "install", "-r", requirements_file],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    
def create_directories():
    print("\nChecking for directories...\n")
    for dir_name in dirs_to_create:
        path = Path(dir_name)
        if not path.exists():
            path.mkdir(exist_ok=True)
            print(f"    Created: {path}")
        else:
            print(f"    {path} already exists")

def create_files():

    print("\nChecking for files...\n")
    for fileName in file_names:
        filePath = Path('EmailStatus/'+fileName)
        if not filePath.exists():
            try:
                with open(filePath, 'a', newline='') as file:
                    writer = csv.writer(file)
                    row = ['Email', ' Date', ' Time']
                    writer.writerow(row)
                print(f'    Created: {fileName}')

            except Exception as error:
                log_error(f"Could not write to {filePath} due to: {error}")
        else:
            print(f'    {fileName} already exists')

def main():
    try:
        create_virtualenv()
        install_requirements()
        create_directories()
        create_files()

        print()
        print("Setup completed successfully !!")
        print(f"\nTo activate the virtual environment, run:")
        print(r"    for Windows: 'environment\\Scripts\\activate'")
        print(r"    for Linux: 'source environment/bin/activate'")
        print()

    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {e}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()