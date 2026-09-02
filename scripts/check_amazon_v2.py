import os, re, ast, time, subprocess, json
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from hermes_tools import web_search, terminal

BASE = r"C:\Users\koda3\AetherHome"
PYTHON_FILE = os.path.join(BASE, "scripts", "build_expanded_reviews.py")

# Load brands dict safely
with open(PYTHON_FILE, "r", encoding="utf-8") as f:
    source = f.read()
brands_code = source.split("for brand_slug, brand_data in brands.items()")[0]
glo = {"os": os}
exec(brands_code, glo)
brands = glo["brands"]

CURL_HEADERS = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-GB,en;q=0.5",
]

def curl(url):
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "30"] + [f"-H={h}" for h in CURL_HEADERS] + [url],
            capture_output=True, text=True, timeout=45
        )
        return result.stdout
    except Exception as e:
        print(f"curl error: {e}")
        return ""

def is_bot_check(html):
    return "bm-verify" in html or "Enter the characters you see below" in html or "To discuss automated access" in html

def extract_asin_from_url(url):
    m = re.search(r"/dp/([A-Z0-9]{10})", url)
    if m:
        return m.group(1)
    return ""

def search_amazon_asin(query):
    """Use web_search to find an Amazon UK URL and extract ASIN."""
    try:
        res = web_search(query=query + " amazon.co.uk", limit=5)
        data = res.get("data", {}).get("web", [])
        for item in data:
            url = item.get("url", "")
            if "amazon.co.uk" in url and "/dp/" in url:
                asin = extract_asin_from_url(url)
                if asin:
                    return asin, url
    except Exception as e:
        print(f"web_search error: {e}")
    return "", ""

def parse_product_page(html):
    title_match = re.search(r"<title>(.*?)</title>", html)
    title = title_match.group(1).strip() if title_match else ""
    price_match = re.search(r'<span class="a-offscreen">(£[0-9,]+\.[0-9]{2})</span>', html)
    price = price_match.group(1) if price_match else ""
    rating_match = re.search(r'<span class="a-icon-alt">(.*?)</span>', html)
    rating = rating_match.group(1) if rating_match else ""
    review_match = re.search(r'<span id="acrCustomerReviewText"[^>]*>(.*?)</span>', html)
    if not review_match:
        review_match = re.search(r'<span class="a-size-base s-underline-text[^"]*"[^>]*>(.*?)</span>', html)
    reviews = review_match.group(1) if review_match else ""
    avail_match = re.search(r'<span class="a-color-success">(.*?)</span>', html)
    if not avail_match:
        avail_match = re.search(r'<span class="a-color-base a-text-bold">(.*?)</span>', html)
    availability = avail_match.group(1) if avail_match else ""
    return {
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "availability": availability,
    }

def is_match(product_name, page_title):
    pn = product_name.lower()
    pt = page_title.lower()
    words = [w for w in re.split(r"\W+", pn) if len(w) > 3]
    return all(w in pt for w in words)

report = []
changes = []

for brand_slug, brand_data in brands.items():
    brand_name = brand_data["name"]
    for prod in brand_data["products"]:
        name = prod["name"]
        slug = prod["slug"]
        current_price = prod["price"]
        current_score = prod["score"]
        current_count = prod["count"]
        query = f"{name} {brand_name}"
        print(f"Checking: {name} ...")
        asin, url = search_amazon_asin(query)
        if not asin:
            print(f"  No ASIN found for {name}")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "no_asin",
            })
            time.sleep(2)
            continue
        prod_url = f"https://www.amazon.co.uk/gp/product/{asin}"
        html = curl(prod_url)
        if not html or is_bot_check(html):
            print(f"  Bot check or empty for {name} (ASIN {asin})")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "skipped",
                "asin": asin,
                "url": url,
            })
            time.sleep(5)
            continue
        data = parse_product_page(html)
        if not data["price"]:
            print(f"  No price found for {name} (ASIN {asin})")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "no_price",
                "asin": asin,
                "url": url,
                "title": data["title"],
            })
            time.sleep(3)
            continue
        # Validate match
        if not is_match(name, data["title"]) and not is_match(name.split()[0], data["title"]):
            print(f"  Title mismatch: expected {name}, got {data['title']}")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "mismatch",
                "asin": asin,
                "url": url,
                "title": data["title"],
            })
            time.sleep(3)
            continue
        price_changed = current_price != data["price"]
        rating_changed = current_score != data["rating"].split(" ")[0]
        count_changed = False
        if data["reviews"]:
            count_str = data["reviews"].strip("()").replace(",", "").replace(" ", "")
            if count_str.isdigit():
                count_val = int(count_str)
                count_changed = abs(count_val - int(current_count)) > 50
        material = price_changed or rating_changed or count_changed
        record = {
            "brand": brand_name,
            "product": name,
            "slug": slug,
            "status": "ok" if not material else "changed",
            "asin": asin,
            "amazon_title": data["title"],
            "amazon_price": data["price"],
            "amazon_rating": data["rating"],
            "amazon_reviews": data["reviews"],
            "amazon_availability": data["availability"],
            "current_price": current_price,
            "current_score": current_score,
            "current_count": current_count,
        }
        report.append(record)
        if material:
            changes.append(record)
            print(f"  CHANGE: price {current_price} -> {data['price']}, rating {current_score} -> {data['rating']}, reviews {current_count} -> {data['reviews']}")
        else:
            print(f"  OK: price {data['price']}, rating {data['rating']}, reviews {data['reviews']}")
        time.sleep(3)

report_path = os.path.join(BASE, "scripts", "amazon_check_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({"report": report, "changes": changes}, f, indent=2)
print("\nReport saved to", report_path)
print("Total products:", len(report))
print("Changed:", len(changes))
for c in changes:
    print(f"  {c['brand']} / {c['product']}: price {c['current_price']} -> {c['amazon_price']}, rating {c['current_score']} -> {c['amazon_rating']}, reviews {c['current_count']} -> {c['amazon_reviews']}")
