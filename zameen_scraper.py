
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time

# Optional: Google Sheets
USE_GOOGLE_SHEETS = False  # Set to True if using Google Sheets
GOOGLE_SHEET_ID = 'your_google_sheet_id_here'
SHEET_NAME = 'DailyListings'

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://www.zameen.com"

LOCATION_URLS = {
    # "Askari 4":
    # "https://www.zameen.com/Homes/Karachi_Gulistan_e_Jauhar_Askari_4-6648-1.html?beds_in=3",
    # "Askari 5":
    # "https://www.zameen.com/Rentals/Karachi_Askari_5-418/3_bedrooms/",
    # "KDA Officers":
    # "https://www.zameen.com/Rentals/Karachi_KDA_Officers_Society-423/3_bedrooms/",
    # "PECHS":
    # "https://www.zameen.com/Rentals/Karachi_PECHS-410/3_bedrooms/",
    # "KDA Overseas":
    # "https://www.zameen.com/Rentals/Karachi_KDA_Overseas-4968/3_bedrooms/",
    "Priority":
    "https://www.zameen.com/Rentals/Karachi_Cantt_Malir_Cantonment_Askari_5-6655-1.html?locations=%2FKarachi_Gulistan_e_Jauhar_Askari_4-6648%2C%2FKarachi_Jamshed_Town_PECHS-403%2C%2FKarachi_Gulshan_e_Iqbal_Town_KDA_Officers_Society-508%2C%2FKarachi_Gulistan_e_Jauhar_KDA_Overseas_Bungalows-19647&beds_in=3&sort=price_asc"
}

def get_listing_data_from_page(url, area_name):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    ads = soup.select("li._357a9934")
    data = []

    for ad in ads:
        try:
            title = ad.select_one("h2._64bb5d3b").get_text(strip=True)
            price = ad.select_one("span._1d4e7065").get_text(strip=True)
            features = ad.select_one("span._033281ab").get_text(strip=True)
            location = ad.select_one("span._162e6469").get_text(strip=True)
            link = BASE_URL + ad.select_one("a")["href"]
        except:
            continue

        try:
            detail_response = requests.get(link, headers=HEADERS)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
            portion_type = "Upper Portion" if "Upper Portion" in title else (
                           "Lower Portion" if "Lower Portion" in title else "Unknown")
            size = features.split("•")[-1].strip()
            beds = features.split("•")[0].strip()
            block = next((b for b in location.split(",") if "Block" in b), "N/A")
            contact = detail_soup.select_one('a._9a722c12')
            contact = contact.get_text(strip=True) if contact else "Not Shown"
        except:
            portion_type = size = beds = block = contact = "N/A"

        data.append([
            datetime.date.today(),
            area_name,
            portion_type,
            size,
            beds,
            price,
            block,
            link,
            contact,
            ""
        ])
        time.sleep(1)
    return data

def get_all_pages(base_url, max_pages=200, area_name="Unknown"):
    all_results = []
    for page in range(1, max_pages + 1):
        paged_url = f"{base_url}?page={page}"
        print(f"🔄 {area_name} - Page {page}")
        listings = get_listing_data_from_page(paged_url, area_name)
        if not listings:
            break
        all_results.extend(listings)
        time.sleep(2)
    return all_results

def run_multi_location_scraper():
    final_results = []
    for location, url in LOCATION_URLS.items():
        print(f"\n📍 Scraping: {location}")
        results = get_all_pages(url, max_pages=5, area_name=location)
        final_results.extend(results)
    return final_results

def save_to_csv(data, filename='zameen_multi_karachi.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def save_to_google_sheet(data):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(SHEET_NAME)
    sheet.append_rows(data, value_input_option='RAW')

if __name__ == "__main__":
    data = run_multi_location_scraper()

    if USE_GOOGLE_SHEETS:
        save_to_google_sheet(data)
    else:
        save_to_csv(data)

    print(f"\n✅ Finished. {len(data)} listings saved.")
