import os
import urllib.request

base = r"C:\Users\koda3\AetherHome"
assets = os.path.join(base, "assets", "products")
os.makedirs(assets, exist_ok=True)

# Map of slug -> search query for placeholder images using open-source image APIs
# Using picsum or placeholder services would still give random photos.
# Better approach: generate simple SVG placeholders per product category.
products = {
  "philips-hue": ["hue-bridge-pro", "hue-essential-starter-kit", "hue-play-floor-lamp", "hue-white-color-ambiance-starter-kit", "hue-outdoor-sensor"],
  "ecobee": ["ecobee-smart-thermostat-premium", "ecobee-smart-thermostat-enhanced", "ecobee-smartsensor-2-pack", "ecobee-smartcamera", "ecobee-switch-plus"],
  "arlo": ["arlo-pro-5s", "arlo-ultra-3", "arlo-video-doorbell-2k", "arlo-essential-spotlight-camera", "arlo-floodlight-camera"],
  "august": ["august-wi-fi-smart-lock", "august-smart-lock-pro", "august-smart-keypad", "august-doorbell-cam-pro", "august-connect"],
  "aqara": ["aqara-motion-sensor-p2", "aqara-smart-lock-u400", "aqara-hub-m200", "aqara-door-window-sensor", "aqara-water-leak-sensor", "aqara-camera-g3"],
  "amazon-echo": ["echo-hub", "echo-show-8", "echo-dot-max", "echo-pop", "echo-dot-5th-gen", "echo-studio"],
  "roborock": ["roborock-qrevo-s-pro", "roborock-qrevo-2-pro", "roborock-s8-pro-ultra", "roborock-e5"],
  "google-nest": ["nest-hub-max", "nest-learning-thermostat-4th-gen", "nest-cam-indoor-3rd-gen", "nest-doorbell", "nest-mini", "nest-audio"]
}

category_colors = {
    "lighting": "#D8B25C",
    "thermostat": "#4ade80",
    "camera": "#f87171",
    "lock": "#60a5fa",
    "sensor": "#a78bfa",
    "hub": "#f472b6",
    "display": "#fb923c",
    "speaker": "#34d399",
    "cleaning": "#94a3b8",
    "doorbell": "#fbbf24",
    "accessory": "#e879f9",
}

def slug_to_category(slug):
    s = slug.lower()
    if "bridge" in s or "hub" in s: return "hub"
    if "sensor" in s or "camera" in s and "door" not in s: return "camera" if "camera" in s else "sensor"
    if "lock" in s or "u400" in s: return "lock"
    if "door" in s or "doorbell" in s: return "doorbell"
    if "thermostat" in s or "switch" in s: return "thermostat"
    if "show" in s or "hub" in s: return "display"
    if "dot" in s or "studio" in s or "pop" in s or "audio" in s or "mini" in s: return "speaker"
    if "strip" in s or "lamp" in s or "light" in s or "hue" in s: return "lighting"
    if "vacuum" in s or "roborock" in s or "qrevo" in s or "s8" in s or "e5" in s: return "cleaning"
    return "accessory"

count = 0
for brand, slugs in products.items():
    brand_dir = os.path.join(assets, brand)
    os.makedirs(brand_dir, exist_ok=True)
    for slug in slugs:
        cat = slug_to_category(slug)
        color = category_colors.get(cat, "#888888")
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420">
  <rect width="640" height="420" fill="#1C1C1E"/>
  <rect x="40" y="40" width="560" height="340" rx="24" fill="none" stroke="{color}" stroke-width="2" opacity="0.4"/>
  <text x="320" y="200" font-family="system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif" font-size="28" fill="#EFEDE7" text-anchor="middle" font-weight="600">{slug.replace("-", " ").title()}</text>
  <text x="320" y="245" font-family="system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif" font-size="16" fill="#9aa3b2" text-anchor="middle">{cat.title()}</text>
  <circle cx="320" cy="310" r="28" fill="{color}" opacity="0.18"/>
  <circle cx="320" cy="310" r="10" fill="{color}" opacity="0.85"/>
</svg>'''
        path = os.path.join(brand_dir, f"{slug}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        count += 1

print(f"Generated {count} copyright-safe SVG product placeholders under {assets}")
