import requests
import re
import json
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

products = [
    ("Philips Hue", "hue-bridge-pro", "Hue Bridge Pro", 77.28, 4.4, 201),
    ("Philips Hue", "hue-essential-starter-kit", "Hue Essential Starter Kit", 85.99, 4.5, 118),
    ("Philips Hue", "hue-white-color-ambiance-starter-kit", "Hue White and Color Ambiance Starter Kit", 149, 4.6, 552),
    ("Philips Hue", "hue-play-floor-lamp", "Hue Play Floor Lamp", 124.99, 4.8, 31),
    ("Philips Hue", "hue-outdoor-sensor", "Hue Outdoor Sensor", 49, 4.6, 2142),
    ("Ecobee", "ecobee-smart-thermostat-premium", "Ecobee Smart Thermostat Premium", 205, 4.4, 320),
    ("Ecobee", "ecobee-smart-thermostat-enhanced", "Ecobee Smart Thermostat Enhanced", 158, 4.3, 275),
    ("Ecobee", "ecobee-smartsensor-2-pack", "Ecobee SmartSensor 2-Pack", 66, 4.6, 8495),
    ("Ecobee", "ecobee-smartcamera", "Ecobee SmartCamera", 66, 4.0, 45),
    ("Ecobee", "ecobee-switch-plus", "Ecobee Switch+", 82, 4.1, 52),
    ("Arlo", "arlo-pro-5s", "Arlo Pro 5S", 158, 4.3, 210),
    ("Arlo", "arlo-ultra-3", "Arlo Ultra 3", 158, 4.2, 168),
    ("Arlo", "arlo-video-doorbell-2k", "Arlo Video Doorbell 2K", 108, 4.1, 146),
    ("Arlo", "arlo-essential-spotlight-camera", "Arlo Essential Spotlight Camera", 66, 4.1, 83),
    ("Arlo", "arlo-floodlight-camera", "Arlo Floodlight Camera", 208, 4.0, 48),
    ("August", "august-wi-fi-smart-lock", "August Wi-Fi Smart Lock", 208, 4.0, 4215),
    ("August", "august-smart-lock-pro", "August Smart Lock Pro", 166, 4.0, 102),
    ("August", "august-smart-keypad", "August Smart Keypad", 49, 3.9, 77),
    ("August", "august-doorbell-cam-pro", "August Doorbell Cam Pro", 166, 3.9, 41),
    ("August", "august-connect", "August Connect", 66, 3.8, 56),
    ("Aqara", "aqara-motion-sensor-p2", "Aqara Motion Sensor P2", 23, 4.2, 155),
    ("Aqara", "aqara-smart-lock-u400", "Aqara Smart Lock U400", 225, 4.2, 118),
    ("Aqara", "aqara-hub-m200", "Aqara Hub M200", 66, 4.2, 318),
    ("Aqara", "aqara-door-window-sensor", "Aqara Door and Window Sensor", 15, 4.3, 118),
    ("Aqara", "aqara-water-leak-sensor", "Aqara Water Leak Sensor", 15, 4.4, 134),
    ("Aqara", "aqara-camera-g3", "Aqara Camera G3", 66, 4.2, 76),
    ("Amazon Echo", "echo-hub", "Echo Hub", 125, 4.2, 140),
    ("Amazon Echo", "echo-show-8", "Echo Show 8", 150, 4.2, 174),
    ("Amazon Echo", "echo-dot-max", "Echo Dot Max", 79.99, 4.3, 162),
    ("Amazon Echo", "echo-pop", "Echo Pop", 44.99, 4.0, 94),
    ("Amazon Echo", "echo-dot-5th-gen", "Echo Dot 5th Gen", 54.99, 4.2, 101),
    ("Amazon Echo", "echo-studio", "Echo Studio", 219.99, 4.3, 89),
    ("Roborock", "roborock-qrevo-s-pro", "Roborock Qrevo S Pro", 429.99, 4.4, 120),
    ("Roborock", "roborock-qrevo-2-pro", "Roborock Qrevo 2 Pro", 529.99, 4.4, 104),
    ("Roborock", "roborock-s8-pro-ultra", "Roborock S8 Pro Ultra", 1079, 4.4, 64),
    ("Roborock", "roborock-e5", "Roborock E5", 249, 4.0, 92),
    ("Google Nest", "nest-hub-max", "Nest Hub Max", 214.99, 4.2, 178),
    ("Google Nest", "nest-learning-thermostat-4th-gen", "Nest Learning Thermostat 4th Gen", 208, 4.4, 245),
    ("Google Nest", "nest-cam-indoor-3rd-gen", "Nest Cam Indoor 3rd Gen", 83, 4.1, 132),
    ("Google Nest", "nest-doorbell", "Nest Doorbell", 150, 4.1, 88),
    ("Google Nest", "nest-mini", "Nest Mini", 41, 4.1, 112),
    ("Google Nest", "nest-audio", "Nest Audio", 83, 4.3, 98),
]

def search_amazon(query):
    url = f"https://www.amazon.co.uk/s?k={requests.utils.quote(query)}"
    try:
        resp = requests.get(url, headers=headers, timeout=25)
        if resp.status_code != 200:
            return None, f"HTTP {resp.status_code}"
        soup = BeautifulSoup(resp.text, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        if not results:
            return None, "No results"
        
        best = None
        best_score = 0
        query_lower = query.lower()
        for item in results[:30]:
            title_tag = item.find('h2')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True).lower()
            tokens = set(re.findall(r'[a-z0-9]+', query_lower))
            brand_words = {'philips', 'hue', 'google', 'nest', 'amazon', 'echo', 'roborock', 'arlo', 'august', 'aqara', 'ecobee', 'smart', 'newest', 'gen', 'wifi', 'wi-fi'}
            tokens = tokens - brand_words
            if not tokens:
                score = 1.0
            else:
                matched = sum(1 for t in tokens if t in title)
                score = matched / len(tokens)
            if score > best_score:
                best_score = score
                best = item
                if score >= 0.8:
                    break
        
        if best is None or best_score < 0.3:
            return None, f"Low match ({best_score:.2f})"
        
        asin = best.get('data-asin')
        if not asin:
            link = best.find('a', href=re.compile(r'/dp/'))
            if link:
                m = re.search(r'/dp/([A-Z0-9]{10})', link['href'])
                if m:
                    asin = m.group(1)
        
        title = best.find('h2').get_text(strip=True)[:150]
        return {"asin": asin, "title": title, "match": best_score}, None
    except Exception as e:
        return None, str(e)

def fetch_product(asin):
    url = f"https://www.amazon.co.uk/dp/{asin}"
    try:
        resp = requests.get(url, headers=headers, timeout=25)
        if resp.status_code != 200:
            return None, None, None, f"HTTP {resp.status_code}"
        soup = BeautifulSoup(resp.text, 'lxml')
        
        price = None
        price_el = soup.select_one('.a-price .a-offscreen') or soup.select_one('#priceblock_ourprice') or soup.select_one('.a-color-price')
        if price_el:
            text = price_el.get_text(strip=True)
            m = re.search(r'£\s*([0-9,]+\.[0-9]{2})', text)
            if m:
                price = float(m.group(1).replace(',', ''))
        
        rating = None
        rating_el = soup.select_one('#acrPopover') or soup.select_one('span[data-hook="rating-out-of-text"]') or soup.select_one('.a-icon-alt')
        if rating_el:
            text = rating_el.get_text(strip=True)
            m = re.search(r'([0-9]\.[0-9])', text)
            if m:
                rating = float(m.group(1))
        
        count = None
        count_el = soup.select_one('#acrCustomerReviewText') or soup.select_one('span[data-hook="total-review-count"]')
        if count_el:
            text = count_el.get_text(strip=True)
            m = re.search(r'([0-9,]+)', text.replace(',', ''))
            if m:
                count = int(m.group(1))
        
        return price, rating, count, None
    except Exception as e:
        return None, None, None, str(e)

changes = []
same = []
errors = []

for brand, slug, name, old_price, old_score, old_count in products:
    search_result, err = search_amazon(name)
    time.sleep(1.0)
    
    if err or not search_result or not search_result.get('asin'):
        alt_query = f"{brand} {name}"
        search_result, err = search_amazon(alt_query)
        time.sleep(1.0)
    
    if err or not search_result or not search_result.get('asin'):
        errors.append({"brand": brand, "name": name, "error": f"Search failed: {err}"})
        continue
    
    asin = search_result['asin']
    price, rating, count, err = fetch_product(asin)
    time.sleep(0.6)
    
    if err:
        errors.append({"brand": brand, "name": name, "asin": asin, "error": f"Product page failed: {err}"})
        continue
    
    price_changed = False
    score_changed = False
    count_changed = False
    delta_price = None
    
    if price is not None and old_price > 0:
        pct = (price - old_price) / old_price * 100
        if abs(pct) >= 8:
            price_changed = True
            delta_price = pct
    
    if rating is not None:
        if abs(rating - old_score) >= 0.2:
            score_changed = True
    
    if count is not None and old_count > 0:
        if abs(count - old_count) / old_count >= 0.15:
            count_changed = True
    
    entry = {
        "brand": brand,
        "name": name,
        "slug": slug,
        "asin": asin,
        "search_title": search_result['title'],
        "old_price": old_price,
        "new_price": price,
        "delta_pct": delta_price,
        "old_score": old_score,
        "new_score": rating,
        "score_changed": score_changed,
        "old_count": old_count,
        "new_count": count,
        "count_changed": count_changed,
    }
    
    if price_changed or score_changed or count_changed:
        changes.append(entry)
    else:
        same.append(entry)

print("=== CHANGES ===")
print(json.dumps(changes, indent=2))
print("\n=== SAME ===")
for item in same:
    print(json.dumps(item))
print(f"\nTotal checked: {len(products)}, Changed: {len(changes)}, Same: {len(same)}, Errors: {len(errors)}")
if errors:
    print("Errors:", json.dumps(errors, indent=2))
