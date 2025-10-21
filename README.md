# MuffinBite

MuffinBite is a **CLI-based email automation tool** built in Python. It allows you to send personalized emails in bulk, attach files seamlessly, and manage campaigns with ease. MuffinBite supports the **Gmail API** and any other SMTP service provider, making it flexible for different use cases.  

It’s ideal for small businesses, marketers, or anyone looking to send large-scale emails without hitting restrictive limits.

---

## Features
- Send bulk emails using the Gmail API  
- SMTP support for ESPs such as Brevo, Mailgun, Postmark, and others  
- Create, list, show, and delete campaigns with subject, template, attachments, CC/BCC, etc.  
- Send bulk HTML template emails with embedded images (base64 supported)  
- Personalize email content using CSV/Excel data sources  
- Insert variables into subject lines and email bodies for dynamic outreach  
- Attach unlimited files of any type  
- Add custom HTML signatures to all outgoing emails (with enable/disable toggle)  
- Set a custom time delay between sending emails to avoid spam filters  
- Test mode: send emails using test data files before running real campaigns  
- Real-time directory watching: automatically refreshes session data when files in Attachments or DataFiles change  
- Log successful and failed email attempts to CSV files  
- Detailed error logging to file when debug mode is enabled  
- Configure all settings (user, provider, debug, delay, signature, etc.) via CLI  
- Run shell commands directly from the MuffinBite CLI using `!<command>`
---

## Upcoming Features

- Fetch drafts directly from Gmail  
- Google Sheets integration for recipient data  
- Unit Tests support
---
## Available commands
    Available MuffinBite commands:

        build - Create the necessary directories and files for the working of the project

        camp - Maintains campaign
            Example:
                camp --create                   (creates new campaign)
                camp --show   'campaign_name'   (shows a specific campaign)
                camp --delete 'campaign_name'   (delete a specific campaign)
                camp --list                     (list all the campaigns)

        send - Sends emails 
            Example:
                send --test (sends emails from test data)
                send --real (sends emails from real data)

        config - Configure settings.
            Example:
                config --user-name name                             (resets user name)
                config --user-email firstname.lastname@example.com  (resets the user email)
                config --service-provider-name provider_name        (resets service provider name)
                config --service-provider-server server_address     (resets service provider server address)
                config --service-provider-login login               (resets service provider login ID)
                config --service-provider-port 000                  (resets service provider port number)
                config --signature <html>                           (add signature to all the outgoing mails)
                config --signature-on                               (turn signatures ON)
                config --signature-off                              (turn signatures OFF)
                config --time-delay 0.00                            (time gap between two emails)
                config --show                                       (shows the current configurations)
                config --debug True/False                           (switches debug mode for error logs)

        exit - Exit the MuffinBite

        reset - Deletes the config file

        help - Shows all the available commands and their uses
    Use !<command> for direct shell commands like `ls`, `clear`, `pwd`, etc.
---

---
## Folder Structure
```
repo_root/
├── muffinbite/
│   ├── commands/            # CLI commands
│   │   ├── __init__.py
│   │   ├── build.py
│   │   ├── campaign.py
│   │   ├── configure.py
│   │   ├── quit.py
│   │   ├── reset_config.py
│   │   └── send.py
│   │
│   ├── esp/                 # Email service providers integration
│   │   ├── __init__.py
│   │   ├── google_esp.py
│   │   └── smtp_esp.py
│   │
│   ├── management/          # Core management and CLI setup
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── session_watcher.py
│   │   └── settings.py
│   │
│   ├── sender/              # Email sending logic
│   │   ├── __init__.py
│   │   └── sender.py
│   │
│   └── utils/               # Helper functions and abstract classes
│       ├── __init__.py
│       ├── abstracts.py
│       ├── helpers.py
│       └── hybridcompleter.py
│
├── LICENSE
├── MANIFEST.in
├── README.md
├── requirements.txt
└── setup.py

```
---
## Setup Instructions

### 1. Clone the repository locally

```
git clone https://github.com/Shivansh-varshney/MuffinBite
```

### 2. Install the cloned project in your virtual environment
```
pip install /path/to/muffinbite/
```

### 3. Enter the MuffinBite CLI
```
(environment) shivansh@shivansh:~/Desktop/all_codes/tryMuffinBite$ bite
```
### 4. For the first time run 'build' or 'help'
```
bite> build
bite> help
```

> Put the credentials for Google Gmail Api in credentials.json file in the working directory.
> If you are using gmail api then first run will open a browser window for logging in and generate token.json for authentication.