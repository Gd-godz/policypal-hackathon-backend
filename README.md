# PolicyPal Backend

This is the Python backend for **PolicyPal**, a conversational health coverage assistant powered by Gemini. It handles user queries, connects to Google Sheets for plan data, and returns intelligent responses to the frontend.

---

## 🧠 Tech Stack

| Layer                | Technology                            |
|----------------------|----------------------------------------|
| **Language**         | Python                                 |
| **Framework**        | Flask |
| **AI Service**       | Google Gemini API                      |
| **Data Source**      | Google Sheets (via service account)    |
| **Deployment**       | Cloud Functions                        |
| **Auth**             | Service account JSON (not committed)   |

---

## 🚀 Run Locally

**Prerequisites:**
- Python 3.10+
- `pip` or `poetry`

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your service account credentials
Place your service-account.json file in the root directory.
Important: This file is ignored via .gitignore and should never be committed.
### 4. Run the server
python main.py

### Security Notes
- service-account.json contains sensitive credentials, do not commit it to GitHub
- .gitignore is configured to exclude this file
- Use environment variables or secret managers in production

🌐 API Endpoint
This backend is deployed to Google Cloud Functions.
The frontend sends requests to:
https://us-central1-crested-idiom-305022.cloudfunctions.net/check_coverage

### Related Repo:
PolicyPal Frontend: https://github.com/Gd-godz/policypal-hackathon-frontend.git
