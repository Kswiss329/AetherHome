import re, subprocess, json, time

HEADERS = [
    '-H', 'Accept-Language: en-GB,en;q=0.9',
    '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def fetch_search(name):
    url = 'https://www.amazon.co.uk/s?k=' + name.replace(' ', '+')
    cmd = ['curl', '-s', '-L'] + HEADERS + [url]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return res.stdout

def parse_first_result(html):
    parts = html.split('data-component-type="s-search-result"')
    if len(parts) < 2:
        return None
    block = parts[1]
    # Title
    title_m = re.search(r'<h2[^>]*aria-label="([^"]+)"', block)
    if not title_m:
        title_m = re.search(r'<h2>\s*<span[^>]*class="a-size-base-plus a-color-base a-text-normal">([^<]+)</span>', block)
    title = title_m.group(1).strip() if title_m else ''
    # Brand from first span in title block
    brand_m = re.search(r'<h2 class="a-size-mini s-line-clamp-1"><span class="a-size-base-plus a-color-base">([^<]+)</span></h2>', block)
    brand = brand_m.group(1).strip() if brand_m else ''
    if brand and brand.lower() not in title.lower():
        title = brand + ' ' + title
    # Price
    price_m = re.search(r'<span class="a-offscreen">£(\d+(?:\.\d+)?)</span>', block)
    price = float(price_m.group(1)) if price_m else None
    # Rating
    rating_m = re.search(r'(\d\.\d) out of 5 stars', block)
    rating = float(rating_m.group(1)) if rating_m else None
    # Count - try multiple patterns
    count = None
    count_m = re.search(r'aria-label="(\d[\d,]*)\s*ratings"', block)
    if count_m:
        count = int(count_m.group(1).replace(',', ''))
    else:
        count_m = re.search(r'\((\d[\d,]*)\)', block)
        if count_m:
            count = int(count_m.group(1).replace(',', ''))
    # Availability
    avail = 'In stock'
    if 'Currently unavailable' in block or 'out of stock' in block.lower():
        avail = 'Out of stock'
    return {'title': title, 'price': price, 'rating': rating, 'count': count, 'availability': avail}

if __name__ == '__main__':
    names = ['Philips Hue Bridge Pro', 'Echo Hub', 'Roborock Qrevo S Pro']
    for name in names:
        print(f"=== {name} ===")
        html = fetch_search(name)
        result = parse_first_result(html)
        print(json.dumps(result, indent=2))
        time.sleep(1)
