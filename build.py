import os
import subprocess
import sys
from pathlib import Path

# Configuration
env_dir = Path("environment")
dirs_to_create = ["Attachments", "DataFiles", "EmailStatus", "logs"]
requirements_file = "requirements.txt"

def log_error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)

def create_virtualenv():
    if not env_dir.exists():
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(env_dir)])
    else:
        print("Virtual environment already exists.")

def install_requirements():
    print("Installing dependencies...")
    # Use venv-specific pip
    pip_path = env_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
    subprocess.check_call([str(pip_path), "install", "-r", requirements_file])

def create_directories():
    for dir_name in dirs_to_create:
        path = Path(dir_name)
        path.mkdir(exist_ok=True)
        print(f"Created or found directory: {path}")

def main():
    try:
        create_virtualenv()
        install_requirements()
        create_directories()

        print("\n✅ Setup completed successfully.")
        print(f"\n➡️  To activate the virtual environment, run:")
        print(f"   {'environment\\Scripts\\activate' if os.name == 'nt' else 'source environment/bin/activate'}\n")

    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {e}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
