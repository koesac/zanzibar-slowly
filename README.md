# Zanzibar, slowly.

A no-build, mobile-first December 2026 trip journal. The public website is self-contained in index.html; no npm, API keys, remote fonts, analytics or database.

## Publish

In repository Settings → Pages → Build and deployment, choose GitHub Actions. Run the Deploy Zanzibar trip workflow or push to main. Adding the workflow does not itself guarantee Pages is enabled. The expected default URL after a successful deployment is https://koesac.github.io/zanzibar-slowly/ — check the Actions deployment output before treating it as live.

## Update

Edit the clearly labelled days, places, checklist and official arrays near the bottom of index.html. Place IDs should remain stable. Update the editorial dates, hotel sections and summary counts in the HTML as needed. CSS and JavaScript are inline so this stays a portable, single-page site. Local preview: python3 -m http.server 8080.

## Source and uncertainty

Based on the supplied Zanzibar.pdf. The plan keeps Jambiani first and Stone Town second, unlike the generic AI itinerary in the PDF. Suggested activities are not bookings. Planned arrival is 17 December, but the original Blue Oyster search started on 16 December: confirm check-in. Thirteen planned hotel nights means ten in Jambiani (17–27 December) plus three in Stone Town (27–30 December). Flight numbers, airports and times are not invented. Restaurant entries are unverified research leads; none is marked allergy-safe. Maps are search links, not verified pins. Follow current official guidance for entry and health. No prices, exchange rate, tide forecast or opening times are presented as live.

## Privacy

This public repository includes exact planned dates and hotels. It excludes the PDF, booking/session identifiers, medical records, unverified hospital recommendations and the machine-translated allergy statement. Private notes, checklist and saved places use browser localStorage: they are not encrypted, do not sync and are not committed. Export private JSON backups before clearing storage; never add those backups to the repository. Other projects on the same GitHub Pages hostname share an origin, so keep those projects trustworthy or use a separate domain for stronger separation.

## Images

The two Unsplash-hosted coastal stock photographs are illustrative, not verified Zanzibar or hotel photographs. This is stated in alt text and the on-site image information dialog. Replace with owned destination photography later. Hotel panels are decorative CSS illustrations. External images, maps and booking pages require an internet connection; this version makes no offline guarantee.

## Checks before travel or deployment

Verify external links and current requirements. Test mobile and desktop layout, day navigation, search and area/category filters, saves and checklist persistence, backup import/export, dialog keyboard handling and print. Keep emergency information and travel documents separately offline.
