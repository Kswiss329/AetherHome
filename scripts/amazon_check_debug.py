import re, subprocess, json, time, os

HEADERS = [
    '-H', 'Accept-Language: en-GB,en;q=0.9',
    '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

BASE = r'C:\Users\koda3\AetherHome'

products = [
    {"brand":"philips-hue","name":"Hue Bridge Pro","slug":"hue-bridge-pro","price":77.28,"score":4.4,"count":201},
    {"brand":"ecobee","name":"Ecobee Smart Thermostat Premium","slug":"ecobee-smart-thermostat-premium","price":205.0,"score":4.4,"count":320},
]

def fetch_search(name):
    url = 'https://www.amazon.co.uk/s?k=' + name.replace(' ', '+')
    cmd = ['curl', '-s', '-L'] + HEADERS + [url]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return res.stdout

def parse_first_organic_result(html):
    parts = html.split('data-component-type="s-search-result"')
    print(f"Parts count: {len(parts)}")
    if len(parts) < 2:
        # Save a snippet
        with open(os.path.join(BASE, 'scripts', 'debug_no_result.html'), 'w', encoding='utf-8') as f:
            f.write(html[:2000])
        return None
    block = parts[1]
    print("Block snippet:", block[:300])
    title_m = re.search(r'<h2[^>]*aria-label="([^"]+)"', block)
    title = title_m.group(1).strip() if title_m else ''
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
    return {'title': title, 'price': price, 'rating': rating, 'count': count, 'availability': avail}

for prod in products:
    print(f"=== {prod['name']} ===")
    html = fetch_search(prod['name'])
    print(f"HTML length: {len(html)}")
    result = parse_first_organic_result(html)
    print(json.dumps(result, indent=2))
    time.sleep(1)
