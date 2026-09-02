import os
import re
import ast
import time
import subprocess
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

BASE = r"C:\Users\koda3\AetherHome"
PYTHON_FILE = os.path.join(BASE, "scripts", "build_expanded_reviews.py")

# Extract brands dict from build_expanded_reviews.py without executing file-writing code
with open(PYTHON_FILE, "r", encoding="utf-8") as f:
    source = f.read()
# Split before the generation loop
brands_code = source.split("for brand_slug, brand_data in brands.items()")[0]
# Execute to get brands variable
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

def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('div[data-asin][data-component-type=s-search-result]')
    results = []
    for item in items[:5]:
        asin = item.get("data-asin", "")
        title_tag = item.select_one("h2 span")
        title = title_tag.get_text(strip=True) if title_tag else ""
        price_tag = item.select_one("span.a-price span.a-offscreen")
        price = price_tag.get_text(strip=True) if price_tag else ""
        rating_tag = item.select_one("span.a-icon-alt")
        rating = rating_tag.get_text(strip=True) if rating_tag else ""
        review_tag = item.select_one("span.a-size-base.s-underline-text")
        reviews = review_tag.get_text(strip=True) if review_tag else ""
        link = f"https://www.amazon.co.uk/dp/{asin}"
        results.append({
            "asin": asin,
            "title": title,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "link": link,
        })
    return results

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
    # availability
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
    # Normalize
    pn = product_name.lower()
    pt = page_title.lower()
    # Check if all significant words from product name appear in page title
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
        search_url = f"https://www.amazon.co.uk/s?k={quote_plus(query)}"
        print(f"Checking: {name} ...")
        html = curl(search_url)
        if not html or is_bot_check(html):
            print(f"  Bot check or empty for {name}")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "skipped",
                "reason": "bot check or empty search"
            })
            time.sleep(5)
            continue
        results = parse_search_results(html)
        matched = None
        for res in results:
            if not res["asin"]:
                continue
            # Quick check: does search result title look like the product?
            if is_match(name, res["title"]):
                matched = res
                break
        if not matched and results:
            # fallback to first result with ASIN
            matched = next((r for r in results if r["asin"]), None)
        if not matched:
            print(f"  No result for {name}")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "no_search_result"
            })
            time.sleep(3)
            continue
        # Fetch product page for detailed data
        prod_url = matched["link"]
        prod_html = curl(prod_url)
        if not prod_html or is_bot_check(prod_html):
            print(f"  Bot check on product page for {name}")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "skipped",
                "reason": "bot check on product page",
                "asin": matched["asin"],
                "search_title": matched["title"],
                "search_price": matched["price"],
                "search_rating": matched["rating"],
            })
            time.sleep(5)
            continue
        data = parse_product_page(prod_html)
        # Validate product page matches
        if not is_match(name, data["title"]) and not is_match(name.split()[0], data["title"]):
            print(f"  Title mismatch: search says '{matched['title']}', product page says '{data['title']}'")
            report.append({
                "brand": brand_name,
                "product": name,
                "status": "mismatch",
                "asin": matched["asin"],
                "search_title": matched["title"],
                "product_title": data["title"],
            })
            time.sleep(3)
            continue
        # Compare
        price_changed = data["price"] and current_price != data["price"]
        rating_changed = data["rating"] and current_score != data["rating"].split(" ")[0]
        count_changed = False
        if data["reviews"]:
            # strip parentheses and commas
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
            "asin": matched["asin"],
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
            print(f"  CHANGE: {name} | Price: {current_price} -> {data['price']} | Rating: {current_score} -> {data['rating']} | Count: {current_count} -> {data['reviews']}")
        else:
            print(f"  OK: {name} | Price: {data['price']} | Rating: {data['rating']} | Reviews: {data['reviews']}")
        time.sleep(3)

# Save report
report_path = os.path.join(BASE, "scripts", "amazon_check_report.json")
import json
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({"report": report, "changes": changes}, f, indent=2)
print("\nReport saved to", report_path)
print("Total products:", len(report))
print("Changed:", len(changes))
if changes:
    print("Changed products:")
    for c in changes:
        print(f"  {c['brand']} / {c['product']}: price {c['current_price']} -> {c['amazon_price']}, rating {c['current_score']} -> {c['amazon_rating']}, reviews {c['current_count']} -> {c['amazon_reviews']}")
else:
    print("No material changes detected.")
