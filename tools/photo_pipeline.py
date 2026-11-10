"""Run after tools/build.py. Extra photographs are checked against Commons metadata.
Network failures are non-fatal; the deployed photo-report.json records coverage.
"""
from pathlib import Path
import html,json,re
from urllib.parse import urlencode,quote,urlparse
from urllib.request import Request,urlopen

EXTRA=[
    ('rock','The Rock Restaurant','The Rock Restaurant, Zanzibar (53801362304).jpg',('zanzibar',)),
    ('forodhani','Forodhani Gardens','Forodhani jubilee gardens Zanzibar.jpg',('zanzibar','forodhani')),
    ('prison','Prison Island','Prison Island.jpg',('zanzibar','changuu')),
    ('colobus','Red colobus at Jozani','Zanzibar Red Colobus at Jozani Chwaka Bay National Park, Kusini DC, South Zanzibar, Tanzania.jpg',('jozani',)),
]
USER_AGENT='ZanzibarSlowly/1.0 (https://github.com/koesac/zanzibar-slowly; credited travel photography)'
def request(url,max_bytes):
    with urlopen(Request(url,headers={'User-Agent':USER_AGENT}),timeout=12) as response:
        payload=response.read(max_bytes+1)
        if len(payload)>max_bytes:raise ValueError('Response exceeds size limit')
        return payload

def text(value):return html.unescape(re.sub('<[^>]+>','',str(value))).strip()
def metadata():
    params={'action':'query','format':'json','prop':'imageinfo','titles':'|'.join('File:'+p[2] for p in EXTRA),'iiprop':'url|size|extmetadata','iiurlwidth':'1280','iiextmetadatafilter':'Artist|LicenseShortName|LicenseUrl|ImageDescription'}
    response=json.loads(request('https://commons.wikimedia.org/w/api.php?'+urlencode(params),2000000))
    return {p['title']:p for p in response.get('query',{}).get('pages',{}).values()}
def additional(pages):
    result={}
    for key,title,filename,terms in EXTRA:
        try:
            info=pages['File:'+filename]['imageinfo'][0];meta=info['extmetadata']
            value=lambda name:text(meta.get(name,{}).get('value',''))
            description=value('ImageDescription').lower()
            if not any(term in description for term in terms):raise ValueError('Destination description not verified')
            licence=value('LicenseShortName');licence_url=value('LicenseUrl')
            if licence_url.startswith('//'):licence_url='https:'+licence_url
            if licence_url.startswith('http://'):licence_url='https://'+licence_url[7:]
            allowed=re.fullmatch(r'https://creativecommons.org/licenses/by(?:-sa)?/[0-9.]+/?',licence_url)
            if not allowed and licence.lower() not in ('public domain','cc0'):raise ValueError('Reusable licence not verified')
            if not allowed:licence_url='https://creativecommons.org/publicdomain/mark/1.0/' if licence.lower()=='public domain' else 'https://creativecommons.org/publicdomain/zero/1.0/'
            author=value('Artist')
            if not author:raise ValueError('Photographer credit missing')
            src=info.get('thumburl') or info['url']
            if urlparse(src).hostname!='upload.wikimedia.org' or not src.startswith('https://'):raise ValueError('Unexpected image host')
            result[key]={'title':title,'src':src,'small':src,'source':'https://commons.wikimedia.org/wiki/File:'+quote(filename.replace(' ','_')),'author':author,'license':licence,'licenseUrl':licence_url,'width':info['width'],'height':info['height'],'changes':'Displayed with responsive resizing and layout cropping; image adaptations remain under the indicated licence.'}
        except (KeyError,IndexError,TypeError,ValueError) as error:
            print(f'Photo not included: {key}: {error}')
    return result

def enhance(out):
    out=Path(out);source=(out/'index.html').read_text();match=re.search(r'(<script type="application/json" id="trip-photos">)(.*?)(</script>)',source,re.S)
    if not match:raise ValueError('Photo manifest missing')
    photos=json.loads(match[2]);new={}
    try:new=additional(metadata())
    except Exception as error:print(f'Additional photo lookup unavailable: {error}')
    photos.update(new);report={};(out/'images').mkdir(exist_ok=True)
    for key,p in photos.items():
        try:
            if urlparse(p['src']).hostname!='upload.wikimedia.org':raise ValueError('Unexpected image host')
            payload=request(p['src'],8000000)
            if payload.startswith(bytes.fromhex('ffd8')):suffix='.jpg'
            elif payload.startswith(bytes.fromhex('89504e470d0a1a0a')):suffix='.png'
            else:raise ValueError('Image response was not JPEG or PNG')
            name='images/'+key+suffix;(out/name).write_bytes(payload)
            source=source.replace(html.escape(p['src'],quote=True),name).replace(html.escape(p['small'],quote=True),name)
            p['src']=name;p['small']=name;report[key]='locally hosted'
        except Exception as error:
            report[key]='remote fallback';print(f'Photo download unavailable: {key}: {error}')
    encoded=json.dumps(photos,ensure_ascii=False).replace('<',chr(92)+'u003c')
    source=re.sub(r'(<script type="application/json" id="trip-photos">).*?(</script>)',lambda m:m[1]+encoded+m[2],source,flags=re.S)
    def credit(p):return '<a href="'+html.escape(p['source'],quote=True)+'" target="_blank" rel="noopener noreferrer">Source</a> · '+html.escape(p['author'])+' · <a href="'+html.escape(p['licenseUrl'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(p['license'])+'</a> · Resized / layout-cropped'
    gallery='<div class="gallery-grid">'
    for key,p in photos.items():
        gallery+='<figure class="gallery-item"><button class="gallery-open" type="button" data-photo="'+key+'" aria-label="Enlarge photograph: '+html.escape(p['title'],quote=True)+'"><img src="'+html.escape(p['src'],quote=True)+'" width="'+str(p['width'])+'" height="'+str(p['height'])+'" alt="'+html.escape(p['title'],quote=True)+'" loading="lazy" decoding="async"><span aria-hidden="true">↗</span></button><figcaption><h3>'+html.escape(p['title'])+'</h3><details><summary>Photo credits</summary><p class="photo-credit">'+credit(p)+'</p></details></figcaption></figure>'
    gallery+='</div></section>'
    source,n=re.subn(r'<div class="gallery-grid">.*?</div></section>',lambda m:gallery,source,count=1,flags=re.S)
    if n!=1:raise ValueError('Gallery marker missing')
    source=source.replace('Photographs of Jambiani, Stone Town and Jozani from credited Wikimedia Commons contributors.','Photographs of places in our itinerary from credited Wikimedia Commons contributors.')
    source=source.replace('The photographs show real destinations in our plan: Jambiani, Stone Town and Jozani.','The photographs show real destinations in our plan.')
    source=source.replace('Photographs load from Wikimedia’s image servers; visitors contact that external host.','Photographs are served with the website when the build download succeeds. Remote fallbacks may contact Wikimedia’s image servers.')
    source=source.replace('</head>','<link rel="stylesheet" href="assets/photo-layout.css"><script defer src="assets/photo-coverage.js"></script></head>')
    (out/'assets/photo-layout.css').write_text(CSS);(out/'assets/photo-coverage.js').write_text(JS)
    (out/'assets/resolved-photos.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2))
    (out/'assets/photo-report.json').write_text(json.dumps({'photos':report,'additional_verified':list(new),'additional_unavailable':[p[0] for p in EXTRA if p[0] not in new]},indent=2))
    (out/'index.html').write_text(source)
    print(f'Photo coverage: {len(photos)} photographs; {len(new)} additional sources verified.')

CSS=r'''/* Explicit height overrides intrinsic HTML dimensions. */
.card-photo img{height:auto;aspect-ratio:16/10;max-height:none}
.day-detail:has(.day-photo){min-height:0}
.day-photo{margin-top:22px}.day-photo img{height:auto;aspect-ratio:16/9;max-height:240px}
.photo-credit{overflow-wrap:anywhere}.gallery-item details{margin-top:8px}.gallery-item details .photo-credit{font-size:10px}
#photo-lightbox{width:min(900px,calc(100% - 24px));max-height:calc(100dvh - 24px);padding:24px;overflow:auto}
#photo-lightbox .dialog-head{gap:16px;margin-bottom:14px;align-items:start}
#photo-lightbox h2{font-size:26px;line-height:1.2;overflow-wrap:anywhere}
#photo-lightbox .close{min-width:44px;min-height:44px;flex-shrink:0}
#photo-lightbox img{width:auto;height:auto;max-width:100%;max-height:min(55svh,480px);margin:0 auto;background:transparent;object-fit:contain}
#photo-lightbox .photo-credit{font-size:10px;line-height:1.6;margin:14px 0 0}
@media(max-width:640px){
.gallery-grid{display:flex;gap:14px;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;padding:0 0 14px;scrollbar-width:thin}
.gallery-item{flex:0 0 min(74vw,290px);scroll-snap-align:start;min-width:0}
.gallery-open img{height:auto;aspect-ratio:4/3}.gallery-item h3{font-size:19px;line-height:1.2}
.day-photo img{max-height:180px}.day-detail:has(.day-photo){min-height:0}
#photo-lightbox{padding:16px}#photo-lightbox h2{font-size:20px}#photo-lightbox .dialog-head{margin-bottom:10px}
#photo-lightbox img{max-height:min(44svh,320px)}
}
@media(max-height:500px){#photo-lightbox img{max-height:36svh}}
@media print{.gallery-section,.day-photo,.card-photo{display:none!important}}
'''
JS=r'''(() => {
'use strict';
const photos=JSON.parse(document.getElementById('trip-photos').textContent);
const e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function figure(key){const p=photos[key];return `<figure class="card-photo"><button type="button" data-photo="${key}" aria-label="Enlarge photograph: ${e(p.title)}"><img src="${e(p.src)}" width="${p.width}" height="${p.height}" alt="${e(p.title)}" loading="lazy" decoding="async"></button><figcaption class="photo-credit"><a href="${e(p.source)}" target="_blank" rel="noopener noreferrer">${e(p.title)}</a> · ${e(p.author)} · <a href="${e(p.licenseUrl)}" target="_blank" rel="noopener noreferrer">${e(p.license)}</a> · Resized / layout-cropped</figcaption></figure>`;}
const mapping={rock:'rock',forodhani:'forodhani',prison:'prison',jozani:'colobus'};
const previousCard=card;
card=function(p){let markup=previousCard(p);const key=mapping[p[0]];if(!key||!photos[key])return markup;markup=markup.replace(/<figure class="card-photo">[\s\S]*?<\/figure>/,'');return markup.replace("<div class='card-top'>",figure(key)+"<div class='card-top'>");};
const previousDay=renderDay;
renderDay=function(){previousDay();const key=({21:'colobus',28:'forodhani',29:'prison'})[days[dayIndex][0]];if(!key||!photos[key])return;const target=document.getElementById('day-detail');target.querySelector('.day-photo')?.remove();target.insertAdjacentHTML('beforeend',figure(key).replace('class="card-photo"','class="day-photo"'));};
renderPlaces();renderSaved();renderDay();
})();
'''

if __name__=='__main__':enhance(Path(__file__).resolve().parent.parent/'_site')
