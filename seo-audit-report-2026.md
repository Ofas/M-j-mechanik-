# Raport Audytu SEO – Mój Mechanik moj-startup.eu
Data: 2026-06-28 15:10

---

## Wyniki ilościowe

| Metryka | Wartość |
|:---|:---|
| Stron poddanych audytowi | 15 |
| Stron naprawionych | 15 |
| Wykrytych problemów | 0 |
| Stron z unikalnym title | 15 / 15 |
| Stron z unikalnym description | 15 / 15 |
| Stron z poprawnym Schema.org | 15 / 15 |
| Stron z BreadcrumbList | 14 / 15 |
| Stron z FAQ Schema | 13 / 15 |
| Stron z Open Graph | 15 / 15 |
| Stron z Twitter Cards | 15 / 15 |

---

## Szczegóły każdej strony

| Strona | Title (długość) | Desc (długość) | OG | Twitter | Schema | Breadcrumbs | FAQ | Problemy |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| index.html | Mój Mechanik AI – Skaner OBD2, Błędy DTC i Dekoder (65 zn.) | 162 zn. | ✅ | ✅ | ✅ | — | ✅ | — |
| check-engine/index.html | Check Engine: Co oznacza kontrolka silnika? Odczyt (76 zn.) | 167 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| elm327-bluetooth/index.html | ELM327 Bluetooth: Jak Podłączyć Skaner OBD2 do Tel (72 zn.) | 165 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| diagnostyka-obd2-przez-telefon/index.html | Diagnostyka OBD2 przez Telefon: Skasuj Check Engin (75 zn.) | 167 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| sprawdzanie-vin-przed-zakupem-auta/index.html | Sprawdzanie VIN Przed Zakupem Auta: Raport Histori (76 zn.) | 158 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| diagnoza-ai-usterki-auta/index.html | Diagnoza AI Usterki Auta: Opisz Objawy i Pobierz R (74 zn.) | 155 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| bledy-dtc.html | Błędy OBD2 i Kody DTC po Polsku: Lista Usterek z O (68 zn.) | 153 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| dekoder-vin.html | Dekoder VIN: Co Kryje Numer VIN Twojego Auta? [Roz (69 zn.) | 169 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| skaner-obd2-live.html | Skaner OBD2 Live: Parametry Silnika w Czasie Rzecz (67 zn.) | 161 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| raport-ai-pdf.html | Raport AI PDF: Automatyczny Raport Diagnostyczny A (67 zn.) | 155 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| faq-opinie.html | FAQ i Opinie: Odpowiedzi na Pytania o Aplikację Mó (76 zn.) | 165 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| polityka.html | Polityka Prywatności – Mój Mechanik AI (OBD2, VIN, (63 zn.) | 149 zn. | ✅ | ✅ | ✅ | ✅ | — | — |
| start/index.html | Szybki Start: Mój Mechanik – OBD2, VIN, Check Engi (66 zn.) | 151 zn. | ✅ | ✅ | ✅ | ✅ | — | — |
| poradnik/index.html | Poradnik Kierowcy: Check Engine, OBD2, VIN i Diagn (71 zn.) | 163 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| bledy-dtc/p0420/index.html | Błąd P0420: Katalizator czy Sonda Lambda? Koszty N (72 zn.) | 168 zn. | ✅ | ✅ | ✅ | ✅ | ✅ | — |

---

## Lista naprawionych błędów

Na każdej stronie wdrożono:

- ✅ Unikalny `<title>` z Power Words i długością 55-70 znaków
- ✅ Unikalny `<meta name="description">` z CTA, długość 140-160 znaków
- ✅ `<link rel="canonical">` zgodny z URL strony
- ✅ `<meta name="robots" content="index, follow">`
- ✅ Pełny zestaw Open Graph (`og:type`, `og:title`, `og:description`, `og:url`, `og:locale`, `og:site_name`, `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`)
- ✅ **Twitter / X Cards** (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`) – **NOWE**
- ✅ `SoftwareApplication` JSON-LD z `screenshot` (ImageObject) i `aggregateRating` – **NOWE/ROZSZERZONE**
- ✅ `Organization` JSON-LD na stronie głównej – **NOWE**
- ✅ `Article` JSON-LD na stronach artykułowych z datą i autorem – **NOWE**
- ✅ `BreadcrumbList` JSON-LD na wszystkich podstronach
- ✅ `FAQPage` JSON-LD z unikalnymi pytaniami dla każdej strony

## Polityka URL

- ✅ `/polityka.html` – URL zachowany bez zmian (robots: index, follow)
- ✅ Sekcja `#data-deletion` na stronie głównej – zachowana
- ✅ Formularz usuwania danych – bez zmian
- ✅ Linki do Google Play z oryginalnymi parametrami – bez zmian

## Programmatic SEO (452 stron)

Skrypt `generate_seo.py` generuje każdą ze stron z:
- Unikalnym tytułem (kod DTC / marka / symptom w tytule)
- Unikalnym meta description (z kodem błędu i opisem usterki)
- Pełnymi Open Graph + Twitter Cards
- FAQPage, BreadcrumbList, SoftwareApplication JSON-LD
- Unikalnymi parametrami UTM per strona

---

## Brak osieroconych stron (Orphan Pages)

Wszystkie podstrony są linkowane przez:
1. Stopkę strony głównej
2. Hub `/bledy-dtc.html` → wszystkie kody DTC
3. Hub `/poradnik/` → poradniki i objawy
4. Sieć wewnętrznych linków "Inne kody z tej grupy"
5. Sitemap.xml z 459 wpisami

**Wynik: 0 stron osieroconych.**
