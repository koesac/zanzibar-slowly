from pathlib import Path
import html,json,re,shutil

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'_site'
photos=json.loads((ROOT/'assets/photos.json').read_text())
def credit(p):
    e=html.escape
    return f'<a href="{e(p["source"])}" target="_blank" rel="noopener noreferrer">{e(p["title"])}</a> · {e(p["author"])} · <a href="{e(p["licenseUrl"])}" target="_blank" rel="noopener noreferrer">{e(p["license"])}</a> · Resized / layout-cropped'
def img(p,eager=False):
    e=html.escape
    return f'<img src="{e(p["src"])}" alt="{e(p["title"])}" width="{p["width"]}" height="{p["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'
source=(ROOT/'index.html').read_text()
for old,key in [('photo-1500375592092-40eb2168fd21','coast'),('photo-1510414842594-a61c69b5ae57','seaweed')]:
    source,n=re.subn(r'<img[^>]*'+re.escape(old)+r'[^>]*>',lambda m:img(photos[key],key=='coast'),source)
    if n!=1:raise SystemExit('Expected exactly one stock photograph: '+old)
source=source.replace("<div class='stay-art' aria-hidden='true'></div>",'<div class="stay-art">'+img(photos['coast'])+'</div><p class="photo-credit">Jambiani destination view, not the hotel. '+credit(photos['coast'])+'</p>')
source=source.replace("<div class='stay-art town-art' aria-hidden='true'></div>",'<div class="stay-art">'+img(photos['town'])+'</div><p class="photo-credit">Stone Town destination detail, not the hotel. '+credit(photos['town'])+'</p>')
gallery='<section class="wrap gallery-section" id="island-portraits"><div class="heading"><div><p class="eyebrow">THE PLACES IN OUR PLAN</p><h2>A real sense of <em>here.</em></h2></div><p>Tap a photograph to look closer.</p></div><p class="gallery-intro">Photographs of Jambiani, Stone Town and Jozani from credited Wikimedia Commons contributors. These are destination photographs, not hotel or tour-operator images.</p><div class="gallery-grid">'
for key,p in photos.items():
    gallery+=f'<figure class="gallery-item"><button type="button" class="gallery-open" data-photo="{key}" aria-label="Enlarge photograph: {html.escape(p["title"])}">'+img(p)+'<span aria-hidden="true">↗</span></button><figcaption><h3>'+html.escape(p['title'])+'</h3><p class="photo-credit">'+credit(p)+'</p></figcaption></figure>'
gallery+='</div></section>'
needle="<section class='wrap' id='places'>"
if source.count(needle)!=1:raise SystemExit('Places section marker changed; review the build script.')
source=source.replace(needle,gallery+needle)
source=source.replace('These are illustrative coastal stock photographs hosted by Unsplash, not verified photographs of Zanzibar, the hotels or the activities. We can replace them with our own trip photographs later. The hotel panels are decorative CSS illustrations.','The photographs show real destinations in our plan: Jambiani, Stone Town and Jozani. They are not photographs of our hotels or booked tours. Each has a linked source, photographer credit and Creative Commons licence. The full credits are in the island gallery. Images use responsive resizing and layout cropping; adaptations retain the indicated licence.')
source=source.replace('The photographs load from an external image host. No analytics, advertising scripts or remote fonts are used.','Photographs load from Wikimedia’s image servers; visitors contact that external host. No analytics, advertising scripts or remote fonts are used. Our source records are in assets/photos.json.')
manifest=json.dumps(photos,ensure_ascii=False).replace('<',chr(92)+'u003c')
source=source.replace('</head>','<meta name="color-scheme" content="light dark"><link rel="stylesheet" href="assets/enrich.css"><script type="application/json" id="trip-photos">'+manifest+'</script><script defer src="assets/enrich.js"></script></head>')
if 'images.unsplash.com' in source:raise SystemExit('Stock photograph reference remains.')
OUT.mkdir(exist_ok=True)
(OUT/'index.html').write_text(source)
(OUT/'.nojekyll').touch()
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
