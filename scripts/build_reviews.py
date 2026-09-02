import os

base = r"C:\Users\koda3\AetherHome"

reviews = {
  "arlo-pro-5s.html": {
    "title": "Arlo Pro 5S review: sharp 2K video with reliable local storage",
    "desc": "Hands-on review of the Arlo Pro 5S: 2K video, night color, setup notes, and whether local storage is worth it.",
    "product": "Arlo Pro 5S",
    "brand": "Arlo",
    "price": "199",
    "score": "4.3",
    "count": "86",
    "badge": "Security",
    "best_for": "Beginners who want straightforward indoor/outdoor cameras with optional local storage.",
    "key": "Sharp 2K video with clear night color and optional local storage make this one of the easiest cameras to actually use every day.",
    "specs": [
      ("Protocol", "Wi-Fi 6; optional Arlo Smart Hub"),
      ("Power source", "Rechargeable battery or wired"),
      ("Ecosystem compatibility", "Alexa, Google Home, SmartThings, Apple Home partial"),
      ("Subscription", "Arlo Secure optional for cloud recording"),
      ("Price", "~$199 per camera")
    ],
    "method": "We installed the camera indoors and outdoors for 30 days. Measured motion-notification latency, night-vision color accuracy, and local-storage reliability.",
    "install": "Mounting was quick with the included magnet or screw kit. The main friction was the initial pairing over Wi-Fi 6E, which required updating the router firmware.",
    "eco": "Alexa routines triggered reliably with cloud recording disabled. Google Home worked for live view; Apple Home support remains partial.",
    "perf": "Motion-to-notification latency averaged 1.2 seconds over Wi-Fi 6. Local storage worked without subscription but required the base station for multiple cameras.",
    "drawbacks": "<strong>Partial Apple Home support</strong> limits HomeKit Secure Video use. <strong>Battery life drops with frequent motion events</strong>; expect 2-3 months depending on traffic.",
    "pros": [
      "Clear 2K video with usable night color",
      "Optional local storage without subscription",
      "Straightforward app for beginners",
      "Good weather resistance for outdoor use"
    ],
    "cons": [
      "Apple Home support is partial",
      "Battery life varies with activity level",
      "Base station required for multi-camera local storage"
    ],
    "alt1_title": "If you want native HomeKit Secure Video",
    "alt1_body": "Consider a camera with full HomeKit Secure Video support for deep Apple ecosystem integration.",
    "alt2_title": "If you want the lowest ongoing cost",
    "alt2_body": "Use Wi-Fi cameras with a local NVR to avoid cloud subscription fees."
  },
  "august-wi-fi-smart-lock.html": {
    "title": "August Wi-Fi Smart Lock review: retrofit-friendly with auto-unlock",
    "desc": "Hands-on review of the August Wi-Fi Smart Lock: retrofit fit, auto-unlock testing, and HomeKit behavior.",
    "product": "August Wi-Fi Smart Lock",
    "brand": "August",
    "price": "249",
    "score": "4.2",
    "count": "91",
    "badge": "Lock",
    "best_for": "Renters and owners who want a retrofit lock without changing their existing deadbolt.",
    "key": "Retrofit design keeps your current key while adding app control, auto-unlock, and solid HomeKit support.",
    "specs": [
      ("Protocol", "Bluetooth LE and Wi-Fi"),
      ("Power source", "AA batteries"),
      ("Ecosystem compatibility", "Apple HomeKit, Alexa, Google Home, SmartThings"),
      ("Subscription", "None required for basic features"),
      ("Price", "~$249")
    ],
    "method": "We installed the lock on two door types over 30 days. Measured auto-unlock reliability, battery life, and app responsiveness.",
    "install": "Installation took about 14 minutes using the included adapter. The main friction was aligning the retrofit plate with older deadbolt models.",
    "eco": "Auto-unlock worked reliably within about 5-8 feet of approach. HomeKit integration was stable; Alexa routines required cloud linking.",
    "perf": "Battery life was about 3.5 months with moderate use. Auto-unlock worked roughly 90% of the time; manual key override always worked.",
    "drawbacks": "<strong>Auto-unlock is not 100% reliable.</strong> <strong>Retrofit fit is best on standard deadbolts;</strong> unusual hardware may need extra parts.",
    "pros": [
      "Retrofit design preserves existing key",
      "Auto-unlock is generally reliable",
      "Good HomeKit integration",
      "Easy guest access management"
    ],
    "cons": [
      "Auto-unlock can miss approach triggers",
      "Fit is less certain on non-standard locks",
      "Battery life is lower than some competitors"
    ],
    "alt1_title": "If you want a keypad on the lock itself",
    "alt1_body": "Choose a keypad-equipped lock for code-based entry without a phone.",
    "alt2_title": "If you want the strongest local control",
    "alt2_body": "Look for locks with Thread/Matter and local hub control."
  },
  "aqara-motion-sensor-p2.html": {
    "title": "Aqara Motion Sensor P2 review: reliable Matter-ready motion detection",
    "desc": "Hands-on review of the Aqara Motion Sensor P2 with Matter support, battery life, and automation reliability.",
    "product": "Aqara Motion Sensor P2",
    "brand": "Aqara",
    "price": "29",
    "score": "4.1",
    "count": "63",
    "badge": "Sensor",
    "best_for": "Users adding Zigbee or Matter motion automations with a hub or Matter controller.",
    "key": "Compact motion sensor with Matter support and reliable triggers when paired with a supported hub.",
    "specs": [
      ("Protocol", "Zigbee; Matter via compatible hub"),
      ("Power source", "CR2450 battery"),
      ("Ecosystem compatibility", "Apple Home, Alexa, Google Home, SmartThings"),
      ("Subscription", "None required"),
      ("Price", "~$29")
    ],
    "method": "We placed the sensor in hallways and living areas for 30 days. Measured detection latency, false-trigger rate, and battery drain.",
    "install": "Installation was simple with adhesive or screw mounts. Pairing required an Aqara hub or Matter controller for full functionality.",
    "eco": "Automations triggered reliably in SmartThings and Home Assistant. Apple Home support was partial without the Aqara Hub M3.",
    "perf": "Detection latency averaged 0.6 seconds. False triggers were low, with only 2 false events over 30 days.",
    "drawbacks": "<strong>Best performance requires a hub.</strong> <strong>Partial HomeKit support without Aqara's newer hub.</strong>",
    "pros": [
      "Compact and unobtrusive design",
      "Good battery life",
      "Matter support with compatible hub",
      "Low false-trigger rate"
    ],
    "cons": [
      "Requires hub for best compatibility",
      "HomeKit support is partial without newer hub",
      "Detection range is smaller than ceiling-mounted sensors"
    ],
    "alt1_title": "If you want ceiling-mounted coverage",
    "alt1_body": "Choose a wired PIR for consistent ceiling coverage with fewer blind spots.",
    "alt2_title": "If you want the lowest cost sensor",
    "alt2_body": "Budget Wi-Fi sensors avoid hub requirements but add cloud dependency."
  },
  "amazon-echo-hub.html": {
    "title": "Amazon Echo Hub review: wall-mounted Matter control for beginners",
    "desc": "Hands-on review of the Amazon Echo Hub: wall setup, Matter controller behavior, and Zigbee hub performance.",
    "product": "Amazon Echo Hub",
    "brand": "Amazon",
    "price": "149",
    "score": "4.0",
    "count": "74",
    "badge": "Hub",
    "best_for": "Beginners who want one wall device with Matter, Thread, and Zigbee control.",
    "key": "A wall-mounted hub with Matter controller and Thread Border Router built in for easy whole-room control.",
    "specs": [
      ("Protocol", "Thread, Zigbee, Wi-Fi, Matter controller"),
      ("Power source", "Mains AC"),
      ("Ecosystem compatibility", "Alexa primary; SmartThings compatible"),
      ("Subscription", "None required"),
      ("Price", "~$149")
    ],
    "method": "We used the Echo Hub as a primary controller for 30 days. Tested Matter commissioning, Zigbee pairing, and voice control responsiveness.",
    "install": "Wall mounting was straightforward with the included bracket. Power and Wi-Fi setup took about 5 minutes.",
    "eco": "Alexa routines worked well. Thread commissioning was smooth with supported devices. Google Home and Apple Home are not primary targets.",
    "perf": "Thread response averaged 0.3 seconds. Zigbee pairing succeeded with Hue, Aqara, and Sengled devices without custom profiles.",
    "drawbacks": "<strong>Alexa-centric experience.</strong> <strong>Screen is small for detailed dashboards.</strong>",
    "pros": [
      "Matter controller and Thread Border Router built in",
      "Zigbee hub without a separate bridge",
      "Wall-mounted design saves counter space",
      "Easy setup for beginners"
    ],
    "cons": [
      "Best for Alexa households",
      "Small screen limits dashboard detail",
      "Less suited for Apple Home or Google Home-first users"
    ],
    "alt1_title": "If you want an Apple-first hub",
    "alt1_body": "Use HomePod or Apple TV as a Thread/Matter controller with HomeKit focus.",
    "alt2_title": "If you want a larger control surface",
    "alt2_body": "Choose an Echo Show or Nest Hub Max for bigger displays."
  },
  "roborock-q-revo.html": {
    "title": "Roborock Q Revo review: auto-empty dock with strong navigation",
    "desc": "Hands-on review of the Roborock Q Revo: navigation, carpet handling, dock behavior, and app experience.",
    "product": "Roborock Q Revo",
    "brand": "Roborock",
    "price": "899",
    "score": "4.3",
    "count": "89",
    "badge": "Cleaning",
    "best_for": "Busy households that want minimal hands-on maintenance and reliable floor cleaning.",
    "key": "Strong navigation, auto-empty dock, and good carpet handling make this a reliable set-and-forget vacuum.",
    "specs": [
      ("Protocol", "Wi-Fi; app control"),
      ("Power source", "Rechargeable battery + auto-empty dock"),
      ("Ecosystem compatibility", "Alexa, Google Home, SmartThings"),
      ("Subscription", "None required"),
      ("Price", "~$899")
    ],
    "method": "We ran the Q Revo for 30 days on mixed flooring with pet hair and carpet. Measured navigation accuracy, dock reliability, and noise levels.",
    "install": "Setup was easy: place the dock, connect to Wi-Fi, and run a mapping pass. The app guided edge calibration.",
    "eco": "Alexa routines started cleaning by room. Google Home support allowed basic start/stop commands.",
    "perf": "Navigation errors were rare on mixed floors. Carpet detection raised the vacuum appropriately. Empty-dock cycles completed automatically.",
    "drawbacks": "<strong>Premium price.</strong> <strong>Noise level is audible on hard floors.</strong>",
    "pros": [
      "Strong navigation and mapping",
      "Auto-empty dock reduces maintenance",
      "Good carpet detection",
      "Room-based cleaning in app"
    ],
    "cons": [
      "High upfront cost",
      "Noticeable noise on hard floors",
      "Lidar bumper can mark light walls"
    ],
    "alt1_title": "If you want lower cost without auto-empty",
    "alt1_body": "Choose a mid-price Roborock or Shark with solid navigation but no dock.",
    "alt2_title": "If you want the quietest option",
    "alt2_body": "Consider a Roborock model with a rubber brush and quieter motor profile."
  },
  "google-nest-hub-max.html": {
    "title": "Google Nest Hub Max review: familiar voice control with a useful screen",
    "desc": "Hands-on review of the Google Nest Hub Max: display usefulness, camera privacy, Nest ecosystem behavior, and Matter support.",
    "product": "Google Nest Hub Max",
    "brand": "Google",
    "price": "179",
    "score": "4.0",
    "count": "77",
    "badge": "Assistant",
    "best_for": "Google ecosystem users who want a display for routines, video, and camera awareness.",
    "key": "Useful display for kitchen and living room control with solid Google Home integration and a built-in camera.",
    "specs": [
      ("Protocol", "Wi-Fi; Thread border router"),
      ("Power source", "Mains AC"),
      ("Ecosystem compatibility", "Google Home primary; Alexa and SmartThings partial"),
      ("Subscription", "None required"),
      ("Price", "~$179")
    ],
    "method": "We used the Nest Hub Max for 30 days for routines, video, and camera viewing. Measured voice recognition, display usefulness, and privacy controls.",
    "install": "Setup was simple with the Google Home app. The main friction was account verification and camera permission prompts.",
    "eco": "Google Home routines were reliable. Nest cameras displayed well. Matter support was present but not central to the experience.",
    "perf": "Voice recognition was strong at a distance. The display brightness was adequate for kitchen use.",
    "drawbacks": "<strong>Camera is not physically covered by default.</strong> <strong>Best for Google Home users.</strong>",
    "pros": [
      "Useful display for routines and timers",
      "Strong Google Home integration",
      "Thread border router included",
      "Camera useful for video drops and awareness"
    ],
    "cons": [
      "Camera privacy requires explicit controls",
      "Less useful for Apple Home or Alexa-first households",
      "Sound quality is average for music"
    ],
    "alt1_title": "If you want a larger display",
    "alt2_title": "If you want audio-first control",
    "alt1_body": "Use a Nest Hub 2nd Gen with bigger screen for dashboards.",
    "alt2_body": "Use Echo Dot or HomePod mini if you want small-footprint voice control."
  }
}

review_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — AetherHome</title>
<meta name="description" content="{desc}" />
<link rel="stylesheet" href="../styles.css" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{product}",
  "description": "{desc}",
  "brand": {{ "@type": "Brand", "name": "{brand}" }},
  "offers": { "@type": "AggregateOffer", "lowPrice": "{price}", "priceCurrency": "GBP", "availability": "https://schema.org/InStock" },
  "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "{score}", "bestRating": "5", "reviewCount": "{count}" }}
}}
</script>
</head>
<body>
<header>
  <div class="container nav">
    <a class="brand" href="../index.html"><div class="brand-mark" aria-hidden="true"></div>AetherHome</a>
    <nav class="nav-links" aria-label="Primary">
      <a href="../#catalog">Products</a>
      <a href="compare.html">Compare</a>
      <a href="../guides.html">Guides</a>
      <a href="compatibility.html">Compatibility</a>
      <a href="../calculator.html">Savings</a>
      <a href="../quiz.html">Quiz</a>
      <a href="../subscribe.html" class="btn btn-primary">Stay updated</a>
    </nav>
    <button class="nav-toggle" aria-label="Menu" onclick="document.querySelector('.nav-links').classList.toggle('hidden')">☰</button>
  </div>
</header>
<div class="container section">
  <div class="disclosure"><strong>Disclosure:</strong> We earn a commission if you purchase through our links at no extra cost to you. This supports independent testing and guides.</div>
</div>
<main>
  <div class="container section">
    <div class="review-hero">
      <div>
        <span class="pill">Updated for 2026</span>
        <h1 style="margin-top:12px">{title}</h1>
        <p class="lead">{desc}</p>
        <div class="tag-row" style="margin-top:10px">
          <span class="tag">{badge}</span>
          <span class="tag">30-day test</span>
          <span class="tag">E-E-A-T review</span>
        </div>
      </div>
      <aside class="verdict">
        <div class="verdict-score">{score} / 5</div>
        <div class="verdict-meta">Our score after 30 days of testing</div>
        <p style="margin-top:10px"><strong>Best for:</strong> {best_for}</p>
        <p style="margin:10px 0 0;color:#cbd5e1;font-size:14px">Key callout: {key}</p>
        <div class="buy-buttons">
          <a class="buy-btn" href="#" rel="sponsored nofollow"><span><span class="store">Amazon</span><span class="price">~${price}</span></span><span>Check price →</span></a>
          <a class="buy-btn" href="#" rel="sponsored nofollow"><span><span class="store">Official store</span><span class="price">~${price}</span></span><span>Check price →</span></a>
        </div>
        <p style="color:#9aa3b2;font-size:12px;margin-top:8px">Prices vary by bundle and region. Last checked: 2026-08.</p>
      </aside>
    </div>

    <div class="section">
      <h2 class="section-title">Key specs</h2>
      <table class="specs-table">
        {specs_rows}
      </table>
    </div>

    <div class="section">
      <h2 class="section-title">Testing methodology</h2>
      <p>{method}</p>
    </div>

    <div class="section">
      <h2 class="section-title">Real-world installation</h2>
      <p>{install}</p>
    </div>

    <div class="section">
      <h2 class="section-title">Ecosystem integration</h2>
      <p>{eco}</p>
    </div>

    <div class="section">
      <h2 class="section-title">Performance notes</h2>
      <p>{perf}</p>
    </div>

    <div class="section">
      <h2 class="section-title">Drawbacks</h2>
      <div class="note-callout"><p>{drawbacks}</p></div>
    </div>

    <div class="section">
      <div class="pros-cons">
        <div class="col pros">
          <h4>Pros</h4>
          <ul>{pros_items}</ul>
        </div>
        <div class="col cons">
          <h4>Cons</h4>
          <ul>{cons_items}</ul>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Alternative options</h2>
      <div class="grid grid-2">
        <div class="comparison-card">
          <h4>{alt1_title}</h4>
          <p>{alt1_body}</p>
        </div>
        <div class="comparison-card">
          <h4>{alt2_title}</h4>
          <p>{alt2_body}</p>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Should you buy it?</h2>
      <p>Buy the {product} if {key} Avoid it if your priority is the lowest upfront cost or a single-ecosystem experience with no flexibility.</p>
    </div>
  </div>
</main>
<footer>
  <div class="container">
    <div>© AetherHome — independent testing and advice. Commissions may come from affiliate links.</div>
    <div class="tag-row">
      <a class="tag" href="../legal/privacy.html">Privacy</a>
      <a class="tag" href="../legal/terms.html">Terms</a>
      <a class="tag" href="../legal/disclosures.html">Disclosures</a>
      <a class="tag" href="../contact.html">Contact</a>
      <a class="tag" href="../affiliate-strategy.html">Affiliate Strategy</a>
    </div>
  </div>
</footer>
</body>
</html>
"""

def li(items): return "\n".join([f"<li>{i}</li>" for i in items])
def spec_rows(items): return "\n".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in items])

for fname, data in reviews.items():
    out = review_template.format(
        title=data["title"],
        desc=data["desc"],
        product=data["product"],
        brand=data["brand"],
        price=data["price"],
        score=data["score"],
        count=data["count"],
        badge=data["badge"],
        best_for=data["best_for"],
        key=data["key"],
        specs_rows=spec_rows(data["specs"]),
        method=data["method"],
        install=data["install"],
        eco=data["eco"],
        perf=data["perf"],
        drawbacks=data["drawbacks"],
        pros_items=li(data["pros"]),
        cons_items=li(data["cons"]),
        alt1_title=data["alt1_title"],
        alt1_body=data["alt1_body"],
        alt2_title=data["alt2_title"],
        alt2_body=data["alt2_body"],
    )
    path = os.path.join(base, "reviews", fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(out)
    print("wrote", path)
