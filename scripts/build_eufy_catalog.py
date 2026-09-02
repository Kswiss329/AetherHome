import os, html
base=r'C:\Users\koda3\AetherHome'
out=os.path.join(base,'brands','eufy'); assets=os.path.join(base,'assets','products','eufy')
os.makedirs(out,exist_ok=True); os.makedirs(assets,exist_ok=True)
raw='''Indoor Cam E220|indoor-cam-e220|44.99|Camera
Video Doorbell E340|video-doorbell-e340|109.99|Doorbell
Video Doorbell S220|video-doorbell-s220|119.00|Doorbell
SoloCam S340|solocam-s340|129.00|Camera
Battery Pack|battery-pack|29.99|Accessory
MiniBase Chime|minibase-chime|35.99|Accessory
Entry Sensor|entry-sensor|19.99|Sensor
Video Doorbell E340 + HomeBase S380|video-doorbell-e340-homebase-s380|253.32|Bundle
Video Doorbell S330|video-doorbell-s330|139.00|Doorbell
HomeBase S380 (HomeBase 3)|homebase-s380|154.00|Hub
RoboVac Cleaning Solution 2-Pack|robovac-cleaning-solution|24.99|Accessory
X10 Pro Omni Robot Vacuum|x10-pro-omni|429.00|Robot vacuum
SmartTrack Link|smarttrack-link|15.99|Tracker
Motion Sensor|motion-sensor|21.98|Sensor
eufy Dust Bag 3-Pack|dust-bag-3-pack|15.99|Accessory
Floodlight Camera E340|floodlight-camera-e340|189.00|Camera
5-Piece Home Alarm Kit|5-piece-home-alarm-kit|149.00|Alarm
Video Doorbell C31|video-doorbell-c31|69.99|Doorbell
4G LTE Cam S330|4g-lte-cam-s330|169.00|Camera
Solar Wall Light Cam S120|solar-wall-light-cam-s120|79.99|Camera
Indoor Cam S350|indoor-cam-s350|118.00|Camera
E21 5-inch Smart Video Baby Monitor|e21-baby-monitor|199.00|Baby monitor
E20 5-inch Smart Video Baby Monitor|e20-baby-monitor|149.00|Baby monitor
Video Doorbell C30|video-doorbell-c30|49.99|Doorbell
Indoor Cam C220|indoor-cam-c220|26.99|Camera
RoboVac Replacement Battery X8|robovac-battery-x8|39.99|Accessory
Video Doorbell Chime Add-on|video-doorbell-chime|19.99|Accessory
SoloCam S220 2-Cam Pack|solocam-s220-2-pack|179.00|Camera
Security Siren 105 dB|security-siren|35.99|Alarm
Indoor Cam E30|indoor-cam-e30|51.99|Camera
Indoor Cam C210|indoor-cam-c210|27.99|Camera
Smart Scale P2 Pro|smart-scale-p2-pro|45.99|Health
Omni C20 Robot Vacuum|omni-c20|499.00|Robot vacuum
Clean L60|clean-l60|174.99|Robot vacuum
Clean L60 Self-Empty Station|clean-l60-self-empty|349.99|Robot vacuum
Omni S2 Robot Vacuum|omni-s2|1599.00|Robot vacuum
Omni E25 Robot Vacuum|omni-e25|598.99|Robot vacuum
Omni E28 Robot Vacuum|omni-e28|899.00|Robot vacuum
Omni C28 Robot Vacuum|omni-c28|529.00|Robot vacuum
Omni S1 Pro Robot Vacuum|omni-s1-pro|699.00|Robot vacuum
C10 Robot Vacuum|c10-robot-vacuum|294.99|Robot vacuum
S4 NVR Security System|s4-nvr-system|799.00|NVR security
S4 Max NVR Security System|s4-max-nvr-system|948.99|NVR security
FamiLock S3 Max|familock-s3-max|399.00|Smart lock
Smart Display E10|smart-display-e10|249.00|Display
SoloCam E30|solocam-e30|99.00|Camera
Video Smart Lock S330|video-smart-lock-s330|299.00|Smart lock
'''
products=[]
for line in raw.splitlines():
 n,s,p,c=line.split('|'); products.append({'name':n,'slug':s,'price':p,'category':c})
# Local original SVG visual for each catalog entry
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#101827"/><stop offset="1" stop-color="#15334a"/></linearGradient></defs><rect width="800" height="500" rx="28" fill="url(#g)"/><circle cx="400" cy="220" r="105" fill="#67e8f9" opacity=".12"/><rect x="295" y="145" width="210" height="150" rx="24" fill="#0b1220" stroke="#67e8f9" stroke-width="4"/><circle cx="400" cy="220" r="34" fill="#67e8f9" opacity=".75"/><text x="400" y="390" fill="#d9faff" font-family="Arial" font-size="34" text-anchor="middle">eufy</text></svg>'''
for p in products: open(os.path.join(assets,p['slug']+'.svg'),'w',encoding='utf-8').write(svg)

def card(p):
 return f'''<article class="card product-card"><div class="badge">{html.escape(p['category'])}</div><img src="../../assets/products/eufy/{p['slug']}.svg" alt="Original AetherHome visual for {html.escape(p['name'])}" style="width:100%;height:150px;object-fit:cover;border-radius:10px;margin:10px 0"/><h3><a href="{p['slug']}.html">{html.escape(p['name'])}</a></h3><p>eufy {html.escape(p['category'].lower())} listing with UK buying guidance and compatibility notes.</p><div class="price-row"><div class="price">£{p['price']}</div><a class="btn btn-secondary" href="{p['slug']}.html">Review</a></div></article>'''
head='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>eufy products — AetherHome</title><meta name="description" content="Complete eufy UK product catalog including security, robot vacuums, smart locks, baby monitors and accessories."><link rel="stylesheet" href="../../styles.css"></head><body><header><div class="container nav"><a class="brand" href="../../index.html"><div class="brand-mark" aria-hidden="true"></div>AetherHome</a><nav class="nav-links"><a href="../../index.html#catalog">Products</a><a href="../../compare.html">Compare</a><a href="../../guides.html">Guides</a><a href="../../compatibility.html">Compatibility</a><a href="../../calculator.html">Savings</a><a href="../../quiz.html">Quiz</a></nav></div></header>'''
foot='''<footer><div class="container"><div>© AetherHome — independent testing and advice. Commissions may come from affiliate links.</div><div class="tag-row"><a class="tag" href="../../legal/privacy.html">Privacy</a><a class="tag" href="../../legal/terms.html">Terms</a><a class="tag" href="../../legal/disclosures.html">Disclosures</a><a class="tag" href="../../contact.html">Contact</a></div></div></footer></body></html>'''
index=head+f'''<main><div class="container section"><div class="disclosure"><strong>Disclosure:</strong> We may earn a commission through retailer links. Product visuals on this page are original AetherHome SVG illustrations, not manufacturer photos.</div><h1 class="section-title">Complete eufy product range</h1><p class="section-sub">{len(products)} eufy UK catalogue entries across security, cleaning, smart locks, baby care, tracking, health and accessories. The official eufy UK catalog also contains variant bundles that change over time.</p><p class="section-sub"><a href="https://www.eufy.com/uk/collections/all" rel="nofollow">Verify current official availability →</a></p><div class="grid grid-4">{''.join(card(p) for p in products)}</div></div></main>{foot}'''
open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(index)
for p in products:
 title=html.escape(p['name']); desc=f"AetherHome catalog entry for {title}, including UK price guidance, compatibility, setup notes and drawbacks."
 page=head+f'''<main><div class="container section"><div class="disclosure"><strong>Disclosure:</strong> We may earn a commission through retailer links. This is an independent catalog entry; verify live price and availability before buying.</div><div class="review-hero"><div><span class="pill">eufy UK catalog</span><h1>{title}</h1><p class="lead">{desc}</p><span class="tag">{html.escape(p['category'])}</span></div><aside class="verdict"><img src="../../assets/products/eufy/{p['slug']}.svg" alt="Original AetherHome visual for {title}" style="width:100%;height:180px;object-fit:cover;border-radius:12px"><div class="price">£{p['price']}</div><p>Indicative UK price. Check the retailer for live availability.</p><a class="buy-btn" href="https://www.amazon.co.uk/s?k=eufy+{p['slug'].replace('-', '+')}" rel="sponsored nofollow">Check Amazon UK →</a></aside></div><section class="section"><h2 class="section-title">What this product is</h2><p>This {html.escape(p['category'].lower())} is included in AetherHome’s expanded eufy range. Confirm the exact model number, included accessories, power requirements and subscription terms before purchase.</p><h2 class="section-title">Compatibility and setup</h2><p>Check Wi-Fi band requirements, eufy app support, local-storage options and whether a HomeBase or other hub is required. For wired products, use a qualified installer where electrical work is involved.</p><h2 class="section-title">Drawbacks to consider</h2><div class="note-callout"><p>Prices and bundles change frequently. Some eufy features vary by region and model, and accessory compatibility must be checked against the exact device generation.</p></div><h2 class="section-title">Buying advice</h2><p>Compare the live eufy UK listing with Amazon UK and other authorised retailers before buying. AetherHome does not use manufacturer product photographs on this page.</p></section></div></main>{foot}'''
 open(os.path.join(out,p['slug']+'.html'),'w',encoding='utf-8').write(page)
print(f'Generated {len(products)} eufy catalog entries and {len(products)} local original SVG visuals.')
