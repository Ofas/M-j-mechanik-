# Raport wdrożenia SEO ROI

Data: 2026-06-02

## Wdrożone zmiany

1. FAQPage Schema
   - Dodano `FAQPage` JSON-LD na stronie głównej.
   - FAQ jest widoczne w treści strony, żeby dane strukturalne były zgodne z HTML.
   - Pytania obejmują: Check Engine, ELM327 Bluetooth, P0420 i rolę aplikacji.

2. Strona `/check-engine/`
   - Dodano nowy landing SEO: `check-engine/index.html`.
   - Intencja: użytkownik z zapaloną kontrolką Check Engine.
   - Zawiera: H1, meta description, FAQPage schema, kroki diagnostyczne, ryzyka jazdy, CTA do Google Play.

3. Strona `/elm327-bluetooth/`
   - Dodano nowy landing SEO: `elm327-bluetooth/index.html`.
   - Intencja: adapter ELM327 Bluetooth, OBD2 i problemy z połączeniem.
   - Zawiera: instrukcję podłączenia, checklistę problemów, FAQPage schema, CTA do Google Play.

4. Strona `/bledy-dtc/p0420/`
   - Dodano nowy landing SEO: `bledy-dtc/p0420/index.html`.
   - Intencja: kod błędu P0420, katalizator, sonda lambda, wydech.
   - Zawiera: objawy, możliwe przyczyny, kroki diagnostyczne, FAQPage schema, CTA do Google Play.

5. Przebudowa hero strony głównej
   - Hero przeniesiono z ogólnego claimu funkcjonalnego na problem użytkownika: `Zapaliła się kontrolka? Sprawdź auto przed warsztatem`.
   - Dodano szybkie linki do: Check Engine, ELM327 Bluetooth, P0420, VIN, OBD2 live, raport AI PDF.
   - Dodano sekcję `Najkrótsza odpowiedź` pod GEO/AI SEO.

## Linkowanie wewnętrzne

- Home linkuje do:
  - `/check-engine/`
  - `/elm327-bluetooth/`
  - `/bledy-dtc/p0420/`
  - `dekoder-vin.html`
  - `skaner-obd2-live.html`
  - `raport-ai-pdf.html`
- Nowe landing pages linkują między sobą i do głównych funkcji.
- Footer strony głównej zawiera linki do nowych stron SEO.

## Sitemap

Zaktualizowano `sitemap.xml`:

- `https://moj-startup.eu/`
- `https://moj-startup.eu/check-engine/`
- `https://moj-startup.eu/elm327-bluetooth/`
- `https://moj-startup.eu/bledy-dtc/p0420/`
- istniejące podstrony funkcji i polityka prywatności

## Wpływ biznesowy

- Wyższy potencjał organiczny dla fraz z jasnym bólem użytkownika: `check engine`, `ELM327 Bluetooth`, `P0420`.
- Lepsza gotowość pod AI Overviews dzięki krótkim odpowiedziom, FAQ i semantycznym sekcjom.
- Lepszy funnel do Google Play przez CTA na stronach problemowych.
- Niższe ryzyko obietnic medyczno-serwisowych: treść jasno mówi, że aplikacja wspiera diagnostykę i nie zastępuje warsztatu.

## Ryzyka i następne kroki

- Warto dodać kolejne strony DTC: P0171, P0300, P0401, P0101.
- Warto dodać `BreadcrumbList` schema na nowych stronach.
- Warto dodać realne opinie Google Play dopiero po potwierdzeniu danych.
- Warto skonfigurować przekierowania lub routing hostingu, jeżeli serwer nie obsługuje katalogów z `index.html`.
