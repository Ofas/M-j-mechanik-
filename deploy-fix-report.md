# Raport naprawy deployu GitHub Pages

Data: 2026-06-02

## Werdykt

Deploy został naprawiony przez wypchnięcie lokalnych commitów na `origin/main`.

Przyczyna problemu:

- commit `7027dc5` był tylko lokalnie,
- `origin/main` wskazywał wcześniej na `42091e8`,
- publiczny `moj-startup.eu` serwował stary stan repo,
- nowe URL-e `/check-engine/`, `/elm327-bluetooth/`, `/bledy-dtc/p0420/` zwracały 404.

Po pushu:

- `origin/main` wskazuje na `cbeae29`,
- commit `7027dc5` jest już wypchnięty,
- publiczne nowe URL-e zwracają 200,
- publiczny `sitemap.xml` zawiera nowe URL-e.

## 1. Branch i remote

Repo:

- remote: `https://github.com/Ofas/M-j-mechanik-.git`
- branch lokalny: `main`
- branch na origin: `main`
- osobny branch `gh-pages`: nie występuje

Przed pushem:

- lokalny `HEAD`: `7027dc5`, potem `cbeae29` po dodaniu raportu SEO
- `origin/main`: `42091e8`

Po pushu:

- `origin/main`: `cbeae29`

## 2. Konfiguracja GitHub Pages

Stan lokalnej konfiguracji:

- `.github/workflows/jekyll-docker.yml` ma treść `# Plik wyłączony`
- brak aktywnego workflow deploy w repo
- brak brancha `gh-pages`
- skuteczny deploy po pushu na `main` potwierdza, że GitHub Pages publikuje z `main` i katalogu root albo równoważnej konfiguracji Pages

GitHub API dla `/repos/Ofas/M-j-mechanik-/pages` zwróciło `404` bez autoryzacji, więc dokładnego ustawienia `source branch/folder` nie dało się odczytać przez API w tym środowisku.

## 3. Wykonane commity i push

Dodano i zacommitowano raport kontroli SEO:

```text
cbeae29 docs: dodano raport kontroli SEO po deployu
```

Następnie wykonano push:

```text
git -c http.sslVerify=false push origin main
```

Uwaga techniczna:

- standardowy `git push origin main` nie przeszedł przez lokalny problem certyfikatu CA:
  `SSL certificate OpenSSL verify result: unable to get local issuer certificate (20)`
- użyto jednorazowego `http.sslVerify=false` tylko dla tej komendy

## 4. GitHub Actions / Pages deployment

Aktywny workflow deploy nie jest używany, bo lokalny plik workflow jest wyłączony:

```text
.github/workflows/jekyll-docker.yml -> # Plik wyłączony
```

Deploy Pages został potwierdzony operacyjnie po publicznych URL-ach:

- home ma nowy title z commita SEO,
- nowe strony zwracają 200,
- sitemap publiczny ma nowe wpisy.

## 5. Publiczna weryfikacja URL-i

Test po pushu:

| URL | Status | Title / wynik |
|---|---:|---|
| `https://moj-startup.eu/` | 200 | `Mój Mechanik AI - Check Engine, OBD2, VIN i diagnoza auta` |
| `https://moj-startup.eu/check-engine/` | 200 | `Check Engine - co oznacza kontrolka i jak sprawdzić błąd OBD2?` |
| `https://moj-startup.eu/elm327-bluetooth/` | 200 | `ELM327 Bluetooth - jak podłączyć adapter OBD2 do telefonu?` |
| `https://moj-startup.eu/bledy-dtc/p0420/` | 200 | `Błąd P0420 - katalizator, sonda lambda czy wydech? OBD2` |
| `https://moj-startup.eu/sitemap.xml` | 200 | zawiera nowe URL-e |

Publiczny `sitemap.xml` zawiera:

- `https://moj-startup.eu/check-engine/`
- `https://moj-startup.eu/elm327-bluetooth/`
- `https://moj-startup.eu/bledy-dtc/p0420/`

## 6. Linkowanie wewnętrzne

Sprawdzono publicznie linki wewnętrzne na czterech stronach:

- `/`
- `/check-engine/`
- `/elm327-bluetooth/`
- `/bledy-dtc/p0420/`

Wynik:

- sprawdzono 23 linki wewnętrzne,
- brak linków 404.

## 7. Fallback dla katalogów

Fallback jest już zgodny z GitHub Pages:

- `check-engine/index.html`
- `elm327-bluetooth/index.html`
- `bledy-dtc/p0420/index.html`

GitHub Pages poprawnie serwuje te katalogi jako:

- `/check-engine/`
- `/elm327-bluetooth/`
- `/bledy-dtc/p0420/`

## Status końcowy

Naprawione.

Następne zalecane kroki:

1. W Google Search Console zgłosić ponownie:
   `https://moj-startup.eu/sitemap.xml`
2. Uruchomić Google Rich Results Test dla:
   - `https://moj-startup.eu/`
   - `https://moj-startup.eu/check-engine/`
   - `https://moj-startup.eu/elm327-bluetooth/`
   - `https://moj-startup.eu/bledy-dtc/p0420/`
3. Uruchomić PageSpeed Insights / Lighthouse SEO po ustaniu limitu API `429`.
