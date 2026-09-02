import ast, os, html
base=r'C:\Users\koda3\AetherHome'
source=os.path.join(base,'scripts','build_expanded_reviews.py')
text=open(source,encoding='utf-8').read()
mod=ast.parse(text)
brands_node=next(n for n in mod.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='brands' for t in n.targets))
brands=ast.literal_eval(brands_node.value)

def esc(x): return html.escape(str(x))
def visual(slug, brand):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#101827"/><stop offset="1" stop-color="#1d1740"/></linearGradient></defs><rect width="800" height="500" rx="28" fill="url(#g)"/><circle cx="400" cy="220" r="105" fill="#a78bfa" opacity=".14"/><rect x="295" y="145" width="210" height="150" rx="24" fill="#0b1220" stroke="#a78bfa" stroke-width="4"/><circle cx="400" cy="220" r="34" fill="#a78bfa" opacity=".75"/><text x="400" y="375" fill="#ede9fe" font-family="Arial" font-size="28" text-anchor="middle">{esc(brand)}</text><text x="400" y="415" fill="#c4b5fd" font-family="Arial" font-size="20" text-anchor="middle">AetherHome original visual</text></svg>'''

def header():
 return '''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="../../styles.css">'''
def nav():
 return '''</head><body><header><div class="container nav"><a class="brand" href="../../index.html"><div class="brand-mark" aria-hidden="true"></div>AetherHome</a><nav class="nav-links"><a href="../../index.html#catalog">Products</a><a href="../../compare.html">Compare</a><a href="../../guides.html">Guides</a><a href="../../compatibility.html">Compatibility</a><a href="../../calculator.html">Savings</a><a href="../../quiz.html">Quiz</a></nav></div></header>'''
def footer():
 return '''<footer><div class="container"><div>© AetherHome — independent testing and advice. Commissions may come from affiliate links.</div><div class="tag-row"><a class="tag" href="../../legal/privacy.html">Privacy</a><a class="tag" href="../../legal/terms.html">Terms</a><a class="tag" href="../../legal/disclosures.html">Disclosures</a><a class="tag" href="../../contact.html">Contact</a></div></div></footer></body></html>'''
for slug,data in brands.items():
 if slug=='eufy': continue
 directory=os.path.join(base,'brands',slug); assetdir=os.path.join(base,'assets','products',slug)
 os.makedirs(directory,exist_ok=True); os.makedirs(assetdir,exist_ok=True)
 products=data.get('products',[])
 for p in products:
  open(os.path.join(assetdir,p['slug']+'.svg'),'w',encoding='utf-8').write(visual(p['slug'],data['name']))
 cards=[]
 for p in products:
  cards.append(f'''<article class="card product-card"><div class="badge">{esc(p['badge'])}</div><img src="../../assets/products/{slug}/{p['slug']}.svg" alt="Original AetherHome visual for {esc(p['name'])}" style="width:100%;height:150px;object-fit:cover;border-radius:10px;margin:10px 0"><h3><a href="{p['slug']}.html">{esc(p['name'])}</a></h3><p>{esc(p['key'])}</p><div class="price-row"><div class="price">£{esc(p['price'])}</div><a class="btn btn-secondary" href="{p['slug']}.html">Review</a></div></article>''')
 index=header()+f'''<title>{esc(data['name'])} products — AetherHome</title><meta name="description" content="AetherHome catalog of {esc(data['name'])} products, with GBP pricing, compatibility notes and buying guidance.">'''+nav()+f'''<main><div class="container section"><div class="disclosure"><strong>Disclosure:</strong> We may earn a commission through retailer links. Product visuals are original AetherHome SVG illustrations, not manufacturer photographs.</div><h1 class="section-title">{esc(data['name'])} product catalog</h1><p class="section-sub">All {len(products)} {esc(data['name'])} products currently represented on AetherHome, with GBP price guidance and individual pages. Manufacturer catalogs and prices change, so verify live details before buying.</p><div class="grid grid-4">{''.join(cards)}</div></div></main>'''+footer()
 open(os.path.join(directory,'index.html'),'w',encoding='utf-8').write(index)
 for p in products:
  title=esc(p['name']); amazon='https://www.amazon.co.uk/s?k='+p['name'].replace(' ','+')
  page=header()+f'''<title>{title} review — AetherHome</title><meta name="description" content="AetherHome catalog entry for {title}, with GBP price guidance, setup notes, compatibility and drawbacks.">'''+nav()+f'''<main><div class="container section"><div class="disclosure"><strong>Disclosure:</strong> We may earn a commission through retailer links. Verify live price and availability before purchasing.</div><div class="review-hero"><div><span class="pill">{esc(data['name'])} catalog</span><h1>{title}</h1><p class="lead">{esc(p['key'])}</p><span class="tag">{esc(p['badge'])}</span></div><aside class="verdict"><img src="../../assets/products/{slug}/{p['slug']}.svg" alt="Original AetherHome visual for {title}" style="width:100%;height:180px;object-fit:cover;border-radius:12px"><div class="price">£{esc(p['price'])}</div><p>Indicative UK price. Check retailer for live availability.</p><a class="buy-btn" href="{amazon}" rel="sponsored nofollow">Check Amazon UK →</a></aside></div><section class="section"><h2 class="section-title">What we checked</h2><p>{esc(p['method'])}</p><h2 class="section-title">Installation and compatibility</h2><p>{esc(p['install'])} {esc(p['eco'])}</p><h2 class="section-title">Performance</h2><p>{esc(p['perf'])}</p><h2 class="section-title">Drawbacks</h2><div class="note-callout"><p>{esc(p['drawbacks'])}</p></div><h2 class="section-title">Pros and cons</h2><div class="pros-cons"><div class="col pros"><h4>Pros</h4><ul>{''.join('<li>'+esc(x)+'</li>' for x in p['pros'])}</ul></div><div class="col cons"><h4>Cons</h4><ul>{''.join('<li>'+esc(x)+'</li>' for x in p['cons'])}</ul></div></div><h2 class="section-title">Our conclusion</h2><p>{esc(p['conclusion'])}</p></section></div></main>'''+footer()
  open(os.path.join(directory,p['slug']+'.html'),'w',encoding='utf-8').write(page)
 print(data['name'],len(products))
print('done')

def add_homepage_links():
 p=os.path.join(base,'index.html'); s=open(p,encoding='utf-8').read()
 marker='<section id="catalog" class="section">'
 block='''<section class="section"><div class="container"><div class="card"><h2 class="section-title">Browse every brand catalog</h2><p class="section-sub">Explore the complete AetherHome catalog by company, including all current site listings.</p><div class="tag-row">'''
 links=[]
 for slug,data in brands.items():
  links.append(f'<a class="tag" href="brands/{slug}/index.html">{esc(data["name"])} catalog</a>')
 block+=''.join(links)+'</div></div></div></section>\n'
 if 'Browse every brand catalog' not in s: s=s.replace(marker,block+marker)
 open(p,'w',encoding='utf-8').write(s)
add_homepage_links()
print('homepage updated')
# Refresh the existing generated catalogs with their current product visual paths if needed.
print('catalog directories written')
