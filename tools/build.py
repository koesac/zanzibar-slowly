from pathlib import Path
from datetime import date
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
def accommodation(source,stay):
    start=date.fromisoformat(stay['check_in']);end=date.fromisoformat(stay['check_out'])
    if end<=start:raise ValueError('Hotel checkout must be after check-in')
    label=f'{start.day}–{end.day} {start.strftime("%B").upper()}' if (start.year,start.month)==(end.year,end.month) else f'{start:%d %b %Y}–{end:%d %b %Y}'
    e=html.escape
    panel=f"<article class='stay'><div class='stay-art' aria-hidden='true'></div><div class='stay-body'><div class='meta'><span>{e(label)}</span><span>{(end-start).days} NIGHTS</span></div><h3>{e(stay['name'])}</h3><p>{e(stay['location'])}. Our beach chapter: slow mornings, a changing ocean and days with very little on the agenda.</p><div class='links'><a href='{e(stay['website'],quote=True)}' target='_blank' rel='noopener noreferrer'>Hotel website ↗</a><a href='{e(stay['listing'],quote=True)}' target='_blank' rel='noopener noreferrer'>Booking listing ↗</a><a href='{e(stay['map'],quote=True)}' target='_blank' rel='noopener noreferrer'>Map ↗</a></div></div></article>"
    source,n=re.subn(r"(<div class='stays'>)<article class='stay'>.*?</article>",lambda m:m[1]+panel,source,count=1,flags=re.S)
    if n!=1:raise ValueError('Jambiani stay panel marker changed')
    note='<details><summary>Our hotel dates</summary><p>Jambiani: '+e(stay['name'])+', '+e(label.lower())+' '+str(start.year)+'. The first-leg stay dates were confirmed by us on 11 November 2026. Flight numbers, airports, local times and transfers still need adding.</p></details>'
    source,n=re.subn(r'<details><summary>A small date detail to confirm</summary><p>.*?</p></details>',lambda m:note,source,count=1,flags=re.S)
    if n!=1:raise ValueError('Original hotel-date note marker changed')
    name=stay['name'].replace('\\','\\\\').replace("'","\\'").replace('<','\\u003c')
    source=source.replace('transfer to Blue Oyster and take the rest of the day slowly. Check-in date needs confirming.','transfer to '+name+' and take the rest of the day slowly.')
    source=source.replace('Check out of Blue Oyster and transfer to Dhow Palace.','Check out of '+name+' and transfer to Dhow Palace.')
    source=source.replace('Confirm hotel dates, especially Blue Oyster check-in','Review hotel confirmations and check-in details')
    source=source.replace('Content prepared 10 November 2026','Content updated 11 November 2026')
    if any(old in source for old in ('Blue Oyster','blueoyster','blue-oyster','Check-in date needs confirming')):raise ValueError('Outdated hotel detail remains in output')
    return source
source=accommodation((ROOT/'index.html').read_text(),json.loads((ROOT/'assets/accommodation.json').read_text())['jambiani'])
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
