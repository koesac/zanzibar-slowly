(() => {
'use strict';
const photos=JSON.parse(document.getElementById('trip-photos').textContent);
const escapeText=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const byId=id=>document.getElementById(id);
function credit(p){return `<a href="${escapeText(p.source)}" target="_blank" rel="noopener noreferrer">${escapeText(p.title)}</a> · ${escapeText(p.author)} · <a href="${escapeText(p.licenseUrl)}" target="_blank" rel="noopener noreferrer">${escapeText(p.license)}</a> · Resized / layout-cropped`;}
function image(p,loading='lazy'){return `<img src="${escapeText(p.src)}" srcset="${escapeText(p.small)} 640w, ${escapeText(p.src)} ${p.width<1280?p.width:(p.title.startsWith('Carved')?960:1280)}w" sizes="(max-width:640px) 90vw, 600px" width="${p.width}" height="${p.height}" alt="${escapeText(p.title)}" loading="${loading}" decoding="async">`;}
function figure(key,cls){const p=photos[key];return `<figure class="${cls}"><button type="button" data-photo="${key}" aria-label="Enlarge photograph: ${escapeText(p.title)}">${image(p)}</button><figcaption class="photo-credit">${credit(p)}</figcaption></figure>`;}
const placePhotos={seaweed:'seaweed',walk:'town',jozani:'jozani'};
const baseCard=card;
card=function(p){const html=baseCard(p),key=placePhotos[p[0]];return key?html.replace("<div class='card-top'>",figure(key,'card-photo')+"<div class='card-top'>"):html;};
const baseDay=renderDay;
renderDay=function(){baseDay();const d=days[dayIndex],key=({18:'seaweed',21:'jozani',27:'town',28:'town'})[d[0]];if(key)byId('day-detail').insertAdjacentHTML('beforeend',figure(key,'day-photo'));};
renderPlaces();renderSaved();renderDay();
const lightbox=document.createElement('dialog');lightbox.id='photo-lightbox';lightbox.setAttribute('aria-labelledby','photo-lightbox-title');lightbox.innerHTML='<div class="dialog-head"><h2 id="photo-lightbox-title"></h2><button class="close" data-close aria-label="Close photograph">×</button></div><div id="photo-lightbox-body"></div>';document.body.append(lightbox);
let returnFocus=null;
document.addEventListener('click',event=>{const button=event.target.closest('[data-photo]');if(!button)return;const p=photos[button.dataset.photo];if(!p)return;returnFocus=button;byId('photo-lightbox-title').textContent=p.title;byId('photo-lightbox-body').innerHTML=image(p,'eager')+`<p class="photo-credit">${credit(p)}<br>${escapeText(p.changes)}</p>`;lightbox.showModal();});
lightbox.addEventListener('close',()=>{if(returnFocus?.isConnected)returnFocus.focus();});
lightbox.addEventListener('click',event=>{if(event.target!==lightbox)return;const r=lightbox.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)lightbox.close();});
document.addEventListener('error',event=>{const img=event.target;if(!(img instanceof HTMLImageElement)||!img.closest('.gallery-item,.card-photo,.day-photo,#photo-lightbox'))return;img.hidden=true;const p=document.createElement('p');p.className='image-unavailable';p.textContent='Photograph unavailable. The credited source link below remains available.';img.parentElement.append(p);},true);
const media=matchMedia('(prefers-color-scheme: dark)');const meta=document.querySelector('meta[name="theme-color"]');function syncChrome(){if(meta)meta.content=media.matches?'#101e20':'#faf8f2';}syncChrome();media.addEventListener('change',syncChrome);
})();
