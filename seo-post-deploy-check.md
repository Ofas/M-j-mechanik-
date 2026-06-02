# SEO post-deploy check

Data kontroli: 2026-06-02  
Commit wskazany do sprawdzenia: `7027dc5`

## Werdykt

Lokalne repo po commicie `7027dc5` jest poprawne pod wymagane elementy SEO: nowe pliki istnieją, URL-e działają na lokalnym serwerze, sitemap zawiera nowe adresy, każda sprawdzana strona ma unikalny title, unikalny meta description, dokładnie jeden H1, canonical, FAQPage schema i link do Google Play.

Publiczny deploy `https://moj-startup.eu` nie jest jeszcze zsynchronizowany z commitem:

- `/` działa, ale nadal pokazuje stary title.
- `/check-engine/` zwraca 404.
- `/elm327-bluetooth/` zwraca 404.
- `/bledy-dtc/p0420/` zwraca 404.
- publiczny `sitemap.xml` nie zawiera nowych URL-i.

Wniosek: wdrożenie jest poprawne w repo, ale nie jest jeszcze opublikowane online.

## 1. Czy nowe URL-e działają?

### Lokalnie, z repo

Test: tymczasowy serwer `python -m http.server` na `127.0.0.1:4173`.

| URL | Status lokalny |
|---|---:|
| `/` | 200 |
| `/check-engine/` | 200 |
| `/elm327-bluetooth/` | 200 |
| `/bledy-dtc/p0420/` | 200 |
| `/sitemap.xml` | 200 |

### Publicznie

Test: `Invoke-WebRequest` do `https://moj-startup.eu`.

| URL | Status publiczny | Wynik |
|---|---:|---|
| `/` | 200 | działa, ale title jest stary: `Mój Mechanik AI - skaner OBD2, VIN i diagnoza auta` |
| `/check-engine/` | 404 | nieopublikowane |
| `/elm327-bluetooth/` | 404 | nieopublikowane |
| `/bledy-dtc/p0420/` | 404 | nieopublikowane |

## 2. Sitemap.xml

### Lokalnie, z repo

`sitemap.xml` zawiera wszystkie nowe URL-e:

- `https://moj-startup.eu/`
- `https://moj-startup.eu/check-engine/`
- `https://moj-startup.eu/elm327-bluetooth/`
- `https://moj-startup.eu/bledy-dtc/p0420/`

### Publicznie

Publiczny `https://moj-startup.eu/sitemap.xml` nadal ma stary stan z `lastmod` 2026-05-31 i nie zawiera:

- `https://moj-startup.eu/check-engine/`
- `https://moj-startup.eu/elm327-bluetooth/`
- `https://moj-startup.eu/bledy-dtc/p0420/`

## 3. Walidacja każdej strony

Wynik lokalnej walidacji HTML:

| URL | Unikalny title | Unikalny meta description | H1 | FAQPage schema | Canonical | Google Play link |
|---|---|---|---:|---:|---|---|
| `/` | OK | OK | 1 | 1 schema / 4 pytania | OK | OK |
| `/check-engine/` | OK | OK | 1 | 1 schema / 3 pytania | OK | OK |
| `/elm327-bluetooth/` | OK | OK | 1 | 1 schema / 3 pytania | OK | OK |
| `/bledy-dtc/p0420/` | OK | OK | 1 | 1 schema / 3 pytania | OK | OK |

Link Google Play obecny na każdej stronie:

`https://play.google.com/store/apps/details?id=com.lukasz.mojmechanik&hl=pl&gl=PL`

## 4. Linkowanie wewnętrzne

Lokalna kontrola linków wewnętrznych w czterech stronach:

- znalezione linki względne zostały zmapowane do plików w repo,
- brak wykrytych 404 lokalnie,
- nowe strony linkują między sobą:
  - `/check-engine/` -> `/elm327-bluetooth/`, `/bledy-dtc/p0420/`, `/bledy-dtc.html`
  - `/elm327-bluetooth/` -> `/check-engine/`, `/bledy-dtc/p0420/`, `/skaner-obd2-live.html`
  - `/bledy-dtc/p0420/` -> `/check-engine/`, `/elm327-bluetooth/`, `/bledy-dtc.html`
  - `/` -> wszystkie trzy nowe URL-e

Publicznie linkowanie do nowych stron będzie dawało 404 do momentu deployu commita.

## 5. Google Rich Results Test

Nie udało się wykonać pełnego Google Rich Results Test dla nowych publicznych URL-i, ponieważ publiczne adresy zwracają 404. Test Rich Results na tych URL-ach przed deployem byłby niemiarodajny.

Lokalna walidacja FAQPage schema:

- JSON-LD parsuje się poprawnie na każdej stronie.
- Każda strona ma `@type: FAQPage`.
- Każda strona ma `mainEntity`.
- Każde pytanie ma `Question`, `name`, `acceptedAnswer`, `Answer`, `text`.
- Brak błędów parsowania JSON-LD.

Wniosek: lokalnie brak krytycznych błędów FAQ schema. Pełny Google Rich Results Test należy powtórzyć po opublikowaniu nowych URL-i.

## 6. Lighthouse SEO minimum 90

Nie udało się wiarygodnie potwierdzić Lighthouse SEO score w tym środowisku:

- lokalny `npx lighthouse` przekroczył limit czasu i nie wygenerował wyników,
- `npx --yes lighthouse --version` również przekroczył limit czasu,
- Google PageSpeed Insights API zwróciło `429 Too Many Requests`,
- publiczne nowe URL-e zwracają 404, więc publiczny Lighthouse dla nich nie byłby testem commita `7027dc5`.

Lokalne checklisty SEO odpowiadające kluczowym audytom Lighthouse SEO są spełnione:

- strony są indeksowalne (`robots=index, follow`),
- mają title,
- mają meta description,
- mają canonical,
- mają crawlable links (`a href`),
- mają dokładnie jeden H1,
- mają poprawny JSON-LD FAQPage,
- mają tekstową treść widoczną w HTML,
- mają link do Google Play.

Status wymogu `Lighthouse SEO >= 90`: **niepotwierdzony narzędziowo**. Do powtórzenia po deployu i po zdjęciu limitu `429` w PageSpeed Insights.

## Rekomendowane akcje

1. Sprawdzić pipeline/deploy GitHub Pages lub hostingu dla `moj-startup.eu`.
2. Po deployu ponownie sprawdzić:
   - `https://moj-startup.eu/check-engine/`
   - `https://moj-startup.eu/elm327-bluetooth/`
   - `https://moj-startup.eu/bledy-dtc/p0420/`
   - `https://moj-startup.eu/sitemap.xml`
3. Po publicznym 200 dla nowych URL-i uruchomić:
   - Google Rich Results Test dla każdej strony,
   - PageSpeed Insights / Lighthouse SEO dla każdej strony.
4. W Google Search Console zgłosić zaktualizowany sitemap:
   - `https://moj-startup.eu/sitemap.xml`

## Podsumowanie statusów

| Obszar | Lokalnie repo | Publicznie moj-startup.eu |
|---|---|---|
| Nowe URL-e | OK, 200 | FAIL, nowe URL-e 404 |
| Sitemap | OK, zawiera nowe URL-e | FAIL, stary sitemap |
| Title/meta/H1/canonical | OK | Niezweryfikowane dla nowych URL-i, bo 404 |
| FAQPage schema | OK lokalnie | Niezweryfikowane dla nowych URL-i, bo 404 |
| Linkowanie wewnętrzne | OK lokalnie | FAIL dla nowych URL-i, bo 404 |
| Rich Results Test | Lokalny JSON-LD OK | Do powtórzenia po deployu |
| Lighthouse SEO >= 90 | Niepotwierdzone przez narzędzie | Do powtórzenia po deployu |
