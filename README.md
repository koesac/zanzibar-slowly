# Zanzibar, slowly.

A mobile-first December 2026 trip journal. Static HTML/CSS/JS; no npm, API keys, database or analytics. Python standard library assembles the deployable site.

## Build and publish

Run `python3 tools/build.py`, then `python3 -m http.server 8080 --directory _site`. Preview http://localhost:8080. Root index.html is the editorial source; preview and deploy _site for the enhanced version. The build replaces stock images and adds destination photography, credits and system-controlled appearance. GitHub Pages must use GitHub Actions; the workflow builds and publishes _site. Check Actions for deployment status. Expected URL: https://koesac.github.io/zanzibar-slowly/.

## Update

Edit days, places, checklist and official arrays in index.html; keep place IDs stable. Update dates and summary counts when needed. Photography records, source links and licences are in assets/photos.json; styling and gallery behaviour are in assets/enrich.css and assets/enrich.js. Update tools/build.py if its source HTML markers change. Do not edit _site manually.

## Appearance and photographs

Light/dark follows prefers-color-scheme, including live changes, without a stored override or toggle. Native controls and browser theme colour follow the appearance; print uses light colours. Four destination photographs: Jambiani seaweed farm (Matt Kieffer, CC BY-SA 2.0); Harvesting seaweed in Jambiani (Yann Macherez, source crop/rotation by Andrew J.Kurbiko, CC BY-SA 4.0); carved Stone Town door (Richard Mortel, CC BY 2.0); Jozani entrance (MacElwee, CC BY 2.0). Full source/licence links and resizing/layout-cropping notices appear in gallery credits. Image adaptations retain the stated licences. These are not hotel or tour-operator photographs.

The build needs no network access. Images load from Wikimedia's external upload server using thumbnail URLs derived from verified Commons filenames. Their live availability is not guaranteed; source links and unavailable-image messages remain. Do not add copyrighted hotel images without permission or an appropriate licence. Focused fixture tests cover build substitutions, image/card/day integration, light/dark changes, gallery Escape/focus, 390px overflow and print. External image responses were mocked; full live deployment and image availability still need checking.

## Privacy and uncertainty

Source: supplied Zanzibar.pdf. Jambiani first, Stone Town second. Arrival is planned for 17 December but the Blue Oyster search began on 16 December: confirm check-in. Thirteen planned nights means ten in Jambiani and three in Stone Town. Activities are suggestions, not bookings. Restaurant leads are unverified, not allergy-safe endorsements. Check current official entry and health guidance.

The public repository contains planned dates and hotel names, not booking/session codes, the PDF or personal medical details. Notes, checklist and saves remain browser-local; not encrypted, synced or sent to GitHub. Never commit private backups. GitHub Pages projects on the same hostname share an origin. Keep emergency information and documents separately offline; external images and links require internet.
