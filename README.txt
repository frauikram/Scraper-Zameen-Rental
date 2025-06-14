
ZAMEEN SCRAPER - MULTI LOCATION (KARACHI)

This script scrapes listings daily from the following areas:
- Askari 4
- Askari 5
- KDA Officers
- PECHS
- KDA Overseas

FEATURES:
- Fetches up to 5 pages per area
- Outputs to CSV (zameen_multi_karachi.csv)
- Optional Google Sheets integration

TO USE LOCALLY:
1. Install dependencies:
   pip install requests beautifulsoup4 gspread oauth2client

2. Run the script:
   python zameen_scraper.py

TO USE GOOGLE SHEETS:
1. Set USE_GOOGLE_SHEETS = True in the script.
2. Place your Google service account credentials as credentials.json
3. Add your Google Sheet ID and sheet name in the script.

FOR DAILY AUTOMATION:
- Use Replit, cron-job.org, or local OS crontab.
