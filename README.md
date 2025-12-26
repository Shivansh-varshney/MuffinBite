# MuffinBite

## What MuffinBite Is (Authoritative)

MuffinBite is a **Python-based interactive CLI tool** for sending **personalized bulk emails** using predefined campaigns and **explicit, user-triggered execution**.

MuffinBite sends emails **only when a user runs a command in the CLI**.  
It does **not** run background jobs, scheduled tasks, queues, or analytics services.

If a feature or command is not explicitly documented in this file, it does not exist in the current version of MuffinBite.

## Key Characteristics

- Interactive CLI (not a background daemon)
- Immediate execution only
- Campaign-based email organization
- Gmail API and SMTP provider support
- Local, file-based configuration and data

## Official Documentation

The official documentation for MuffinBite is available at: https://www.muffinbite.dev/

The documentation provides:
- Installation and setup guides
- Campaign configuration examples
- Provider-specific notes (Gmail API, SMTP)
- Common troubleshooting steps
- Version-specific behavior notes

The README remains the **authoritative feature list** for the current release.

## Platform Support & Compatibility

MuffinBite is implemented entirely in Python and can be installed on **Linux, Windows, and macOS**.

However, **v0.1.x is optimized and tested primarily on Linux**.  
Some behaviors differ across operating systems due to shell, filesystem, and process model differences.

| Platform | Support Level |
|--------|--------------|
| Linux | Fully supported (primary development platform) |
| macOS | Partially supported |
| Windows | Partially supported |

## Current Capabilities (Implemented)

The following list describes the **current, implemented capabilities** of MuffinBite.  
No functionality exists beyond what is listed here.

- Send bulk emails using the Gmail API
- Send bulk emails using SMTP providers (Brevo, Mailgun, Postmark, etc.)
- Campaign management (create, list, show, delete)
- Send HTML emails with embedded images (base64 supported)
- Personalize email content using CSV or Excel data files
- Variable substitution in subject lines and email bodies
- Attach unlimited files of any type
- Add a global HTML email signature (enable/disable)
- Configure a fixed time delay between consecutive emails
- Test mode for validating campaigns before real sends
- Real-time directory watching for Attachments and DataFiles **(Linux-only in v0.1.x)**
- Log successful and failed email attempts to CSV files
- Detailed error logging when debug mode is enabled
- Full configuration via CLI commands

## Shell Commands

Shell commands can be executed from within the MuffinBite CLI using the `!<command>` prefix.

These commands are executed using the **system shell**, and behavior depends on the operating system:

- Linux / macOS: bash or zsh
- Windows: cmd.exe or PowerShell

Shell command syntax is **OS-specific**.

Examples:
- Linux/macOS: `!ls`, `!clear`
- Windows: `!dir`, `!cls`

## Experimental & Linux-First Features (v0.1.x)

The following behaviors are **experimental and Linux-first** in the current v0.1.x series:

- Automatic session refresh using file system watchers
- Automatic CLI restart after `build` and `config` commands

These features rely on Linux-specific process and filesystem behavior and may behave differently or be unavailable on Windows and macOS.

They are expected to be **removed or redesigned in v0.2.0**, as MuffinBite moves toward a stateless and fully cross-platform CLI architecture.

## MuffinBite CLI Commands (Complete and Exclusive)

The commands listed below are the **only commands supported by MuffinBite**.  
Any other commands mentioned elsewhere are **incorrect**.

### `bite`
Enter the muffinbite CLI
```
~/Documents/all_codes/tryMuffinBite$ bite
```

### `build`
Initializes the working directory structure required by MuffinBite.
```
bite> build
```

### `camp`
Campaign management commands.
```
bite> camp --create
bite> camp --show <campaign_name>
bite> camp --delete <campaign_name>
bite> camp --list
```

### `send`
Send emails for the active campaign.
```
bite> send --test # send emails using test data
bite> send --real # send emails using real data
```
Emails are sent immediately when this command is executed.

### `config`
Configure MuffinBite settings.
```
bite> config --user-name <name>
bite> config --user-email <email>
bite> config --service-provider-name <provider>
bite> config --service-provider-server <server_address>
bite> config --service-provider-login <login>
bite> config --service-provider-port <port>
bite> config --signature <html>
bite> config --signature-on
bite> config --signature-off
bite> config --time-delay <seconds>
bite> config --show
bite> config --debug True|False
```
### `reset`

Deletes the configuration file.
```
bite> reset
```
### `help`

Shows all available commands and their usage.
```
bite> help
```
### `exit`

Exit the MuffinBite CLI.
```
bite> exit
```
## Explicitly Not Supported

The following features are intentionally not supported:

- Scheduled or delayed execution at a specific date or time
- Background queues or worker processes
- Email analytics dashboards or statistics
- Command aliases not listed in this README
- REST APIs or web dashboards

## Folder Structure
```
repo_root/
├── muffinbite/
│ ├── commands/
│ │ ├── build.py
│ │ ├── campaign.py
│ │ ├── configure.py
│ │ ├── quit.py
│ │ ├── reset_config.py
│ │ └── send.py
│ ├── esp/
│ │ ├── google_esp.py
│ │ └── smtp_esp.py
│ ├── management/
│ │ ├── cli.py
│ │ ├── session_watcher.py
│ │ └── settings.py
│ ├── sender/
│ │ └── sender.py
│ └── utils/
│ ├── abstracts.py
│ ├── helpers.py
│ └── hybridcompleter.py
├── LICENSE
├── MANIFEST.in
├── README.md
├── requirements.txt
└── setup.py
```

## Setup Instructions
### 1. Clone the repository
```
git clone https://github.com/Shivansh-varshney/MuffinBite
```
### 2. Install the project in a virtual environment
```
pip install /path/to/muffinbite/
```
### 3. Enter the MuffinBite CLI
```
bite
```
### 4. First-time setup
```
bite> build
bite> help
```
> Place Google Gmail API credentials in a `credentials.json` file in the working directory.  
On first use, a browser window will open to complete authentication and generate `token.json`.

## License

> MIT License