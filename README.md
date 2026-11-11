# Zanzibar, slowly.

A mobile-first December 2026 trip journal. Static HTML/CSS/JS; Python standard library builds the site. No npm, API keys, database or analytics.

## Build and publish

Run `python3 tools/build.py`, then `python3 tools/photo_pipeline.py`, then `python3 -m http.server 8080 --directory _site`. Preview http://localhost:8080. Deploy _site, not the editorial root index.html. GitHub Pages must use GitHub Actions; the workflow runs both build steps and publishes _site.

## Editing

The current Jambiani accommodation is in assets/accommodation.json: The Loop Beach Resort, Jambiani, Tanzania, check-in 17 December and check-out 27 December 2026 (10 nights), confirmed by the traveller on 11 November 2026. This record supersedes the original Blue Oyster references in the editorial index.html template. tools/build.py applies the current hotel card, links, arrival/transfer wording, date note and checklist wording to the published site. Edit this JSON for first-leg hotel details; also review the itinerary arrays if changing the actual travel dates. The Stone Town leg remains unchanged.

Edit days, places, checklist and official arrays in index.html. Keep place IDs stable. Update dates and summary counts when needed. Original photography records are in assets/photos.json. tools/build.py creates the base gallery and loads assets/enrich.css/js. tools/photo_pipeline.py adds mobile sizing, extra photo coverage and local photo hosting. Update HTML markers in the build scripts if the source structure changes. Do not edit _site manually.

## Mobile image sizing

Original image dimensions remain in the HTML for aspect information, but CSS explicitly sets height:auto for thumbnails and enlarged photos. Cards use a 16:10 crop; day photos use 16:9 without oversized minimum-height sections. The mobile gallery is a single swipeable row. Lightbox images retain their natural ratio and are capped at 44svh/320px on mobile, with a lower landscape cap. Credits expand separately in the gallery.

## Photo coverage and reliability

The second build step requests Commons metadata for The Rock, Forodhani, Prison Island and red colobus at Jozani. It checks destination descriptions, author credits and reusable CC BY/BY-SA or public-domain licensing before adding a photograph. Unsupported or unavailable records are omitted, not relabelled or replaced with unrelated images. Existing four photographs are retained.

Verified JPEG/PNG downloads up to 8 MB are hosted in _site/images. Failed downloads retain remote URLs. Network lookups are bounded and non-fatal: the sizing fix and existing site still deploy if Commons is unavailable. _site/assets/photo-report.json lists locally hosted/remote images and unresolved extra sources; resolved-photos.json holds the published credits and URLs. This does not guarantee all four additions will resolve on every build. Source and licence links remain visible; resizing/layout cropping is disclosed. No hotel or operator imagery is implied. Cave and hotel photographs still require verified sources/rights.

Focused fixture tests cover 320/390/430px mobile, landscape, thumbnail and lightbox height limits, swipe-gallery overflow, new photo mappings and offline build fallbacks. Network metadata and images were mocked in tests; check the live photo report and deployment. Light/dark continues to follow system preferences; print stays light.

## Privacy and uncertainty

The original source is the supplied Zanzibar.pdf, with the first-leg hotel and dates superseded by the traveller's 11 November 2026 update. Dates and hotel names are public; activities are suggestions, not reservations. The 16/17 December hotel discrepancy is resolved: The Loop check-in is 17 December. No invented flight details, allergy-safe restaurant endorsements or live forecasts. Check current official entry and health guidance.

The PDF, booking/session codes and personal medical details are excluded. Notes, checklist and saves remain browser-local, not encrypted or synced. Never commit private exports. Projects on the same Pages hostname share an origin. Keep travel documents and emergency information separately offline.
