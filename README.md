# LYNN / UNBUILT

Nederlandstalig conceptarchief over anime en bouwkunde. Lynn blijft een anonieme maker. Responsive HTML, twee originele AI-beelden, categoriefilters en uitklapbare bouwkundige uitleg. Geen build of dependencies nodig.

Open `index.html` voor de lokale versie.

## WordPress

Vul `.env` met `WP_URL`, `WP_USER` (inlognaam) en `WP_APP_PASSWORD` (WordPress-applicatiewachtwoord). Publiceer met `python3 scripts/wordpress.py`. Het script controleert eerst de authenticatie, bewaart de oorspronkelijke homepage en instellingen in het genegeerde `backups/`, uploadt de beelden en werkt de bestaande statische homepage bij. De omringende Customizr-opmaak wordt op de nieuwe homepage verborgen. Controleer de gepubliceerde weergave in WordPress; integratie is nog niet visueel geverifieerd.

## AI-beelden

Gemaakt met de ingebouwde image_gen-tool. Definitieve bestanden:

- `assets/megacity.png`: panoramische anime-megastructuur.
- `assets/pavilion.png`: houten paviljoen boven stil water.

De volledige generatieprompts staan in `output/image-prompts.md`. Alle gebouwen zijn fictieve conceptstudies.

## Controles

HTML geparseerd; lokale afbeeldingspaden en alt-teksten gecontroleerd. Python-publicatiescript gecompileerd. Browsercontrole niet beschikbaar in deze sessie. Gepubliceerd op https://lynnbout.nl/; homepage, inline interacties en beide afbeeldingen gecontroleerd via HTTP (200).
