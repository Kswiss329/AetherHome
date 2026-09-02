import re, subprocess, json, time, os

HEADERS = [
    '-H', 'Accept-Language: en-GB,en;q=0.9',
    '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

BASE = r'C:\Users\koda3\AetherHome'

products = [
    {"brand":"philips-hue","name":"Hue Bridge Pro","slug":"hue-bridge-pro","price":77.28,"score":4.4,"count":201},
    {"brand":"philips-hue","name":"Hue Essential Starter Kit","slug":"hue-essential-starter-kit","price":85.99,"score":4.5,"count":118},
    {"brand":"philips-hue","name":"Hue White and Color Ambiance Starter Kit","slug":"hue-white-color-ambiance-starter-kit","price":149.0,"score":4.6,"count":552},
    {"brand":"philips-hue","name":"Hue Play Floor Lamp","slug":"hue-play-floor-lamp","price":124.99,"score":4.8,"count":31},
    {"brand":"philips-hue","name":"Hue Outdoor Sensor","slug":"hue-outdoor-sensor","price":49.0,"score":4.6,"count":2142},
    {"brand":"ecobee","name":"Ecobee Smart Thermostat Premium","slug":"ecobee-smart-thermostat-premium","price":205.0,"score":4.4,"count":320},
    {"brand":"ecobee","name":"Ecobee Smart Thermostat Enhanced","slug":"ecobee-smart-thermostat-enhanced","price":158.0,"score":4.3,"count":275},
    {"brand":"ecobee","name":"Ecobee SmartSensor 2-Pack","slug":"ecobee-smartsensor-2-pack","price":66.0,"score":4.6,"count":8495},
    {"brand":"ecobee","name":"Ecobee SmartCamera","slug":"ecobee-smartcamera","price":66.0,"score":4.0,"count":45},
    {"brand":"ecobee","name":"Ecobee Switch+","slug":"ecobee-switch-plus","price":82.0,"score":4.1,"count":52},
    {"brand":"arlo","name":"Arlo Pro 5S","slug":"arlo-pro-5s","price":158.0,"score":4.3,"count":210},
    {"brand":"arlo","name":"Arlo Ultra 3","slug":"arlo-ultra-3","price":158.0,"score":4.2,"count":168},
    {"brand":"arlo","name":"Arlo Video Doorbell 2K","slug":"arlo-video-doorbell-2k","price":108.0,"score":4.1,"count":146},
    {"brand":"arlo","name":"Arlo Essential Spotlight Camera","slug":"arlo-essential-spotlight-camera","price":66.0,"score":4.1,"count":83},
    {"brand":"arlo","name":"Arlo Floodlight Camera","slug":"arlo-floodlight-camera","price":208.0,"score":4.0,"count":48},
    {"brand":"august","name":"August Wi-Fi Smart Lock","slug":"august-wi-fi-smart-lock","price":208.0,"score":4.0,"count":4215},
    {"brand":"august","name":"August Smart Lock Pro","slug":"august-smart-lock-pro","price":166.0,"score":4.0,"count":102},
    {"brand":"august","name":"August Smart Keypad","slug":"august-smart-keypad","price":49.0,"score":3.9,"count":77},
    {"brand":"august","name":"August Doorbell Cam Pro","slug":"august-doorbell-cam-pro","price":166.0,"score":3.9,"count":41},
    {"brand":"august","name":"August Connect","slug":"august-connect","price":66.0,"score":3.8,"count":56},
    {"brand":"aqara","name":"Aqara Motion Sensor P2","slug":"aqara-motion-sensor-p2","price":23.0,"score":4.2,"count":155},
    {"brand":"aqara","name":"Aqara Smart Lock U400","slug":"aqara-smart-lock-u400","price":225.0,"score":4.2,"count":118},
    {"brand":"aqara","name":"Aqara Hub M200","slug":"aqara-hub-m200","price":66.0,"score":4.2,"count":318},
    {"brand":"aqara","name":"Aqara Door and Window Sensor","slug":"aqara-door-window-sensor","price":15.0,"score":4.3,"count":118},
    {"brand":"aqara","name":"Aqara Water Leak Sensor","slug":"aqara-water-leak-sensor","price":15.0,"score":4.4,"count":134},
    {"brand":"aqara","name":"Aqara Camera G3","slug":"aqara-camera-g3","price":66.0,"score":4.2,"count":76},
    {"brand":"amazon-echo","name":"Echo Hub","slug":"echo-hub","price":125.0,"score":4.2,"count":140},
    {"brand":"amazon-echo","name":"Echo Show 8","slug":"echo-show-8","price":150.0,"score":4.2,"count":174},
    {"brand":"amazon-echo","name":"Echo Dot Max","slug":"echo-dot-max","price":79.99,"score":4.3,"count":162},
    {"brand":"amazon-echo","name":"Echo Pop","slug":"echo-pop","price":44.99,"score":4.0,"count":94},
    {"brand":"amazon-echo","name":"Echo Dot 5th Gen","slug":"echo-dot-5th-gen","price":54.99,"score":4.2,"count":101},
    {"brand":"amazon-echo","name":"Echo Studio","slug":"echo-studio","price":219.99,"score":4.3,"count":89},
    {"brand":"roborock","name":"Roborock Qrevo S Pro","slug":"roborock-qrevo-s-pro","price":429.99,"score":4.4,"count":120},
    {"brand":"roborock","name":"Roborock Qrevo 2 Pro","slug":"roborock-qrevo-2-pro","price":529.99,"score":4.4,"count":104},
    {"brand":"roborock","name":"Roborock S8 Pro Ultra","slug":"roborock-s8-pro-ultra","price":1079.0,"score":4.4,"count":64},
    {"brand":"roborock","name":"Roborock E5","slug":"roborock-e5","price":249.0,"score":4.0,"count":92},
    {"brand":"google-nest","name":"Nest Hub Max","slug":"nest-hub-max","price":214.99,"score":4.2,"count":178},
    {"brand":"google-nest","name":"Nest Learning Thermostat 4th Gen","slug":"nest-learning-thermostat-4th-gen","price":208.0,"score":4.4,"count":245},
    {"brand":"google-nest","name":"Nest Cam Indoor 3rd Gen","slug":"nest-cam-indoor-3rd-gen","price":83.0,"score":4.1,"count":132},
    {"brand":"google-nest","name":"Nest Doorbell","slug":"nest-doorbell","price":150.0,"score":4.1,"count":88},
    {"brand":"google-nest","name":"Nest Mini","slug":"nest-mini","price":41.0,"score":4.1,"count":112},
    {"brand":"google-nest","name":"Nest Audio","slug":"nest-audio","price":83.0,"score":4.3,"count":98},
]

ACCESSORY_KEYWORDS = [
    'compatible with', 'replacement', 'mount', 'charger', 'case', 'wall plate',
    'accessory', 'battery', 'spare parts', 'dock', 'brush', 'filter', 'bag',
    'pad', 'cloth', 'cable', 'adapter', 'power supply', 'stand', 'holder',
    'bracket', 'wall mount', 'power extender', 'c-wire', 'extension', 'plug',
    'socket', 'renewed', 'refurbished', 'gelink', 'for google home mini',
    'for nest mini', 'compatible for', 'fits', 'adapter for', 'charger for'
]

def fetch_search(name):
    url = 'https://www.amazon.co.uk/s?k=' + name.replace(' ', '+')
    cmd = ['curl', '-s', '-L'] + HEADERS + [url]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return res.stdout

def parse_results(html):
    parts = html.split('data-component-type="s-search-result"')
    results = []
    for part in parts[1:]:
        block = part
        asin_m = re.search(r'data-asin="([A-Z0-9]{10})"', block)
        asin = asin_m.group(1) if asin_m else ''
        title_m = re.search(r'<h2[^>]*aria-label="([^"]+)"', block)
        if not title_m:
            title_m = re.search(r'<h2>\s*<span[^>]*class="a-size-base-plus a-color-base a-text-normal">([^<]+)</span>', block)
        title = title_m.group(1).strip() if title_m else ''
        brand_m = re.search(r'<h2 class="a-size-mini s-line-clamp-1"><span class="a-size-base-plus a-color-base">([^<]+)</span></h2>', block)
        brand = brand_m.group(1).strip() if brand_m else ''
        if brand and brand.lower() not in title.lower():
            title = brand + ' ' + title
        price_m = re.search(r'<span class="a-offscreen">£(\d+(?:\.\d+)?)</span>', block)
        price = float(price_m.group(1)) if price_m else None
        rating_m = re.search(r'(\d\.\d) out of 5 stars', block)
        rating = float(rating_m.group(1)) if rating_m else None
        count = None
        count_m = re.search(r'aria-label="(\d[\d,]*)\s*ratings"', block)
        if count_m:
            count = int(count_m.group(1).replace(',', ''))
        else:
            count_m = re.search(r'\((\d[\d,]*)\)', block)
            if count_m:
                count = int(count_m.group(1).replace(',', ''))
        avail = 'In stock'
        if 'Currently unavailable' in block or 'out of stock' in block.lower():
            avail = 'Out of stock'
        if title or price or rating:
            results.append({
                'asin': asin, 'title': title, 'price': price, 'rating': rating,
                'count': count, 'availability': avail
            })
    return results

def is_accessory(title):
    t = title.lower()
    return any(kw in t for kw in ACCESSORY_KEYWORDS)

def best_match(product_name, candidates):
    # Require product name (or significant part) to be in title
    words = set(re.findall(r'\w+', product_name.lower()))
    stops = {'and','the','a','an','of','for','with','to','in','on','new','gen','generation','wifi','wi','fi','smart','home','auto','lock','pro','plus','max','mini','audio','hub','camera','doorbell','thermostat','sensor','light','lamp','robot','vacuum','cleaner','mop','suction'}
    words -= stops
    if not words:
        return None
    best = None
    best_score = 0
    for c in candidates:
        title_l = c['title'].lower()
        # skip accessories
        if is_accessory(c['title']):
            continue
        # skip if price is suspiciously low
        if c['price'] is not None and c['price'] < 10:
            continue
        score = len(words & set(re.findall(r'\w+', title_l)))
        # require at least half the words to match
        if score >= len(words) * 0.5 and score > best_score:
            best_score = score
            best = c
    return best

changes = []
no_change = []

for prod in products:
    try:
        html = fetch_search(prod['name'])
        candidates = parse_results(html)
    except Exception as e:
        print(f"Error fetching {prod['name']}: {e}")
        no_change.append(prod['name'])
        continue

    best = best_match(prod['name'], candidates)
    if not best:
        print(f"No good match for {prod['name']}")
        no_change.append(prod['name'])
        continue

    price_changed = False
    score_changed = False
    count_changed = False
    title_changed = False
    avail_changed = False

    if best['price'] is not None:
        diff = abs(best['price'] - prod['price'])
        pct = diff / prod['price'] if prod['price'] else 1
        if pct > 0.02 or diff > 2.0:
            price_changed = True
    if best['rating'] is not None:
        if abs(best['rating'] - prod['score']) > 0.1:
            score_changed = True
    if best['count'] is not None:
        if prod['count'] > 0 and abs(best['count'] - prod['count']) / max(prod['count'], 1) > 0.10:
            count_changed = True
        elif prod['count'] == 0 and best['count'] != 0:
            count_changed = True
    base_name = prod['name'].split('(')[0].strip()
    if base_name.lower() not in best['title'].lower():
        title_changed = True

    if any([price_changed, score_changed, count_changed, title_changed, avail_changed]):
        changes.append({
            'brand': prod['brand'],
            'name': prod['name'],
            'slug': prod['slug'],
            'old_price': prod['price'],
            'new_price': best['price'],
            'old_score': prod['score'],
            'new_score': best['rating'],
            'old_count': prod['count'],
            'new_count': best['count'],
            'title': best['title'],
            'availability': best['availability'],
            'asin': best['asin'],
            'changes': {
                'price': price_changed,
                'score': score_changed,
                'count': count_changed,
                'title': title_changed,
                'availability': avail_changed,
            }
        })
    else:
        no_change.append(prod['name'])
    time.sleep(0.5)

print(f"\n=== SUMMARY ===")
print(f"Total products: {len(products)}")
print(f"Changes detected: {len(changes)}")
print(f"No change: {len(no_change)}")

for c in changes:
    print(f"\n{c['brand']} / {c['name']}:")
    print(f"  ASIN: {c['asin']}")
    print(f"  Title: {c['title']}")
    print(f"  Price: {c['old_price']} -> {c['new_price']}")
    print(f"  Score: {c['old_score']} -> {c['new_score']}")
    print(f"  Count: {c['old_count']} -> {c['new_count']}")
    print(f"  Availability: {c['availability']}")
    print(f"  Flags: {c['changes']}")

with open(os.path.join(BASE, 'scripts', 'amazon_check_report.json'), 'w', encoding='utf-8') as f:
    json.dump({'changes': changes, 'no_change': no_change, 'total': len(products)}, f, indent=2)

print("\nReport written to scripts/amazon_check_report.json")
