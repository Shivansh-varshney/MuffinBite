# 📧 MuffinBite

This project sends personalized emails in bulk using a single Python script.

---

## 📦 Current Features

- Send bulk emails with attachments using Gmail API
- Personalize content using CSV/Excel data
- Log successful and failed email attempts
- Optional HTML support for emails
---

---
## 📦 Upcoming
- Email open tracking

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/Shivansh-varshney/MuffinBite
cd MuffinBite
```

### 2. Run the build.py file and activate environment
```
python build.py
```

### 3. Configure your Gmail API
> Enable Gmail API in Google Cloud Console
> Download credentials.json
> Place it inside your project directory


### 4. Set-up main.py and settings.py files like the given templates
> Please don't edit the given template files, instead make your own
> main.py and settings.py files and run the code from there

### 5. Run main.py
```
python main.py
```

> First run will open a browser window for logging in
> and generate token.json for authentication.

## Attention !!
> If you're encountering errors while authenticating with the Gmail API, 
> please note that these issues are not related to the code itself. 
> Such errors are likely caused by a misconfiguration during the API setup.
> So we kindly ask you not to open a new issue on the repository right away.
> Instead, please double-check your API setup and ensure all steps are followed correctly.
> However, if you have crossed check all of your api configurations and the error persists
> only then open a new issue on the repository.