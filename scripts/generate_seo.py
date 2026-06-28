import os
import re
import json
from xml.sax.saxutils import escape

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
OUTPUT_DIR = BASE_DIR

# Ensure templates exist
DTC_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'dtc.html')
GUIDE_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'guide.html')
DIAG_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'diagnostics.html')
COMP_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'comparison.html')
BRAND_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'brand.html')

# ---------------------------------------------------------
# DATABASE DEFINITIONS
# ---------------------------------------------------------

# 1. Car Brands (30 brands)
BRANDS = {
    "audi": {
        "name": "Audi",
        "obd_location": "Pod deską rozdzielczą, po lewej stronie kolumny kierowniczej, tuż nad pedałem sprzęgła/podnóżkiem. Fioletowe gniazdo.",
        "faults": [
            {"title": "Wypadanie zapłonu (P0300 - P0306)", "desc": "Częsty problem w silnikach TFSI/FSI związany z cewkami zapłonowymi lub nagarem na zaworach dolotowych."},
            {"title": "Błąd klap w kolektorze (P2015)", "desc": "Zużycie nastawnika klap wirowych w silnikach 2.0 TDI i 3.0 TDI."},
            {"title": "Zatkany filtr DPF (P2002)", "desc": "Problem w dieslach użytkowanych głównie w mieście, wymagający wypalenia serwisowego."}
        ],
        "text": "<p>Diagnostyka Audi za pomocą adaptera OBD2 pozwala na szybkie wykrycie typowych problemów z elektroniką silnika oraz układem oczyszczania spalin. Silniki z grupy VAG są bardzo czułe na parametry mieszanki paliwowo-powietrznej, stąd częste błędy sondy lambda i przepływomierza.</p>"
    },
    "bmw": {
        "name": "BMW",
        "obd_location": "Po lewej stronie pod deską rozdzielczą, w pobliżu dźwigni otwierania maski. Często pod plastikową klapką z napisem OBD.",
        "faults": [
            {"title": "Problemy z Vanosem (P0011 / P0012)", "desc": "Złe ustawienie faz rozrządu, często wynikające z zanieczyszczenia elektrozaworów Vanos lub zużycia łańcucha."},
            {"title": "Przepływomierz i lewe powietrze (P0171)", "desc": "Nieszczelności w układzie dolotowym (odma, rura dolotowa) w silnikach benzynowych."},
            {"title": "Błąd DPF i świec żarowych (P2002 / P0670)", "desc": "Uszkodzenie sterownika świec żarowych w dieslach blokuje automatyczną regenerację DPF."}
        ],
        "text": "<p>W pojazdach BMW diagnostyka OBD2 jest kluczem do monitorowania stanu silnika. Aplikacja Mój Mechanik pozwala odczytać parametry live, takie jak ciśnienie doładowania oraz temperaturę silnika, co ułatwia wykrycie awarii termostatu lub pompy wody przed przegrzaniem.</p>"
    },
    "toyota": {
        "name": "Toyota",
        "obd_location": "Pod deską rozdzielczą, po lewej stronie kolumny kierowniczej, poniżej włącznika otwierania maski.",
        "faults": [
            {"title": "Niska wydajność katalizatora (P0420)", "desc": "Najpopularniejszy błąd w benzynowych silnikach Toyoty, często wywoływany przez zużycie katalizatora lub sondy lambda."},
            {"title": "Problem z zaworem EGR (P0401)", "desc": "Zapychanie zaworu EGR nagarem w silnikach D-4D."},
            {"title": "Błąd układu hybrydowego (P0A80)", "desc": "Wersje hybrydowe mogą zgłaszać problemy z chłodzeniem lub zużyciem ogniw baterii HV."}
        ],
        "text": "<p>Toyota słynie z niezawodności, jednak błąd P0420 jest zmorą wielu właścicieli. Aplikacja Mój Mechanik pozwala na monitorowanie pracy sond lambda przed i za katalizatorem w czasie rzeczywistym, co pomaga ustalić, czy winny jest katalizator, czy uszkodzony czujnik.</p>"
    },
    "volkswagen": {
        "name": "Volkswagen",
        "obd_location": "Pod deską rozdzielczą po lewej stronie, blisko bezpieczników. Dobrze widoczne czerwone lub fioletowe gniazdo.",
        "faults": [
            {"title": "Zbyt niskie ciśnienie doładowania (P0299)", "desc": "Problem z turbosprężarką, zaworem N75 lub nieszczelnością w dolocie silników TSI i TDI."},
            {"title": "Wypadanie zapłonu (P0301 - P0304)", "desc": "Uszkodzenia cewek, świec lub wtryskiwaczy benzynowych."},
            {"title": "Filtr cząstek stałych (P2002 / P242F)", "desc": "Przepełnienie filtra sadzą w silnikach 1.6 i 2.0 TDI."}
        ],
        "text": "<p>Diagnostyka komputerowa aut marki Volkswagen za pomocą aplikacji w telefonie pozwala zaoszczędzić setki złotych na wizytach w serwisie. Szybki odczyt parametrów pracy turbiny oraz przepływu powietrza pozwala precyzyjnie zlokalizować usterkę.</p>"
    },
    "opel": {
        "name": "Opel",
        "obd_location": "W konsoli centralnej, pod plastikową klapką pod hamulcem ręcznym lub pod popielniczką.",
        "faults": [
            {"title": "Uboga mieszanka (P0171)", "desc": "Nieszczelności kolektora ssącego, uszkodzona membrana pokrywy zaworów (odma) w silnikach 1.4 Turbo."},
            {"title": "Błąd cewki zapłonowej (P0300)", "desc": "Zintegrowany moduł cewki zapłonowej w silnikach ECOTEC jest podatny na przebicia."},
            {"title": "Problemy z zaworem EGR (P0400)", "desc": "Zablokowanie zaworu z powodu nagromadzenia sadzy."}
        ],
        "text": "<p>W samochodach marki Opel zapalenie się kontrolki silnika (Check Engine) jest częstym zjawiskiem. Mój Mechanik w połączeniu z ELM327 pozwala szybko zweryfikować, czy problem dotyczy układu zapłonowego, czy nieszczelności dolotu.</p>"
    },
    "ford": {
        "name": "Ford",
        "obd_location": "Po lewej stronie kierownicy, pod małym schowkiem (należy go uchylić lub zdemontować plastikową osłonę).",
        "faults": [
            {"title": "Błąd ciśnienia paliwa (P0191)", "desc": "Problem z czujnikiem ciśnienia na szynie Common Rail lub pompą wysokiego ciśnienia w dieslach TDCi."},
            {"title": "Niedoładowanie turbo (P0299)", "desc": "Pęknięte węże intercoolera (częsta usterka w Fordach) lub uszkodzenie geometrii turbiny."},
            {"title": "Usterka układu wspomagania (U0100 / U0140)", "desc": "Błędy komunikacji na szynie CAN łączącej moduły."}
        ],
        "text": "<p>Właściciele Fordów często borykają się z pękającymi rurami dolotowymi intercoolera. Aplikacja Mój Mechanik pozwala na bieżąco monitorować ciśnienie doładowania (MAP sensor) podczas jazdy próbnej, co natychmiast ujawnia ubytek ciśnienia.</p>"
    }
}

# Add remaining brands programmatically to reach 30 brands
OTHER_BRANDS = [
    "renault", "citroen", "peugeot", "fiat", "mercedes", "volvo", "honda", "nissan", "hyundai", "kia",
    "skoda", "seat", "suzuki", "mazda", "chevrolet", "dacia", "mitsubishi", "subaru", "jeep", "lexus",
    "land-rover", "alfa-romeo", "jaguar", "lancia"
]

for b in OTHER_BRANDS:
    name_cap = b.replace('-', ' ').title()
    BRANDS[b] = {
        "name": name_cap,
        "obd_location": f"Pod deską rozdzielczą po stronie kierowcy, pod kierownicą lub w pobliżu skrzynki bezpieczników w pojazdach marki {name_cap}.",
        "faults": [
            {"title": "Błąd sondy lambda (P0130)", "desc": "Niewłaściwe wskazania czujnika tlenu w spalinach."},
            {"title": "Wypadanie zapłonów (P0300)", "desc": "Problemy z układem zapłonowym lub składem mieszanki."},
            {"title": "Usterka zaworu recyrkulacji spalin EGR (P0401)", "desc": "Ograniczony przepływ w układzie recyrkulacji spalin."}
        ],
        "text": f"<p>Diagnostyka OBD2 w samochodach {name_cap} pozwala na szybkie zidentyfikowanie przyczyn zapalenia kontrolki check engine. Aplikacja Mój Mechanik współpracuje z interfejsem ELM327 Bluetooth, oferując odczyt kodów błędów oraz parametrów silnika na żywo.</p>"
    }

# 2. Symptoms (30 symptoms)
SYMPTOMS = {
    "auto-szarpie": {
        "title": "Auto szarpie przy przyspieszaniu i na wolnych obrotach – co sprawdzić?",
        "description": "Dlaczego samochód szarpie podczas jazdy? Zobacz najczęstsze przyczyny: wypadanie zapłonu, cewki, świece, brudna przepustnica, lewe powietrze. Sprawdź OBD2.",
        "heading": "Auto szarpie podczas jazdy",
        "intro": "Szarpanie silnika to uciążliwy objaw, który może pojawiać się przy przyspieszaniu, ruszaniu lub na biegu jałowym. Może dotyczyć zarówno silników benzynowych, jak i diesla.",
        "sections": [
            {"h2": "Najczęstsze przyczyny szarpania auta", "text": "<ul><li><strong>Układ zapłonowy (benzyna):</strong> Zużyte świece zapłonowe, uszkodzone cewki lub przewody zapłonowe. To najczęstszy powód szarpania pod obciążeniem.</li><li><strong>Układ zasilania paliwem:</strong> Zapchany filtr paliwa, niewydajna pompa paliwa lub uszkodzone wtryskiwacze.</li><li><strong>Układ dolotowy:</strong> Brudna przepustnica, uszkodzony przepływomierz (MAF) lub nieszczelności w dolocie (lewe powietrze).</li><li><strong>Zawór EGR:</strong> Zablokowany lub zanieczyszczony zawór recyrkulacji spalin powoduje szarpanie przy stałej prędkości.</li></ul>"},
            {"h2": "Jak zdiagnozować szarpanie za pomocą OBD2?", "text": "Podłącz adapter OBD2 i uruchom aplikację Mój Mechanik. Szukaj kodów błędów z grupy P0300 (wypadanie zapłonów) lub P0171 (zbyt uboga mieszanka). Sprawdź w parametrach Live Data korekty paliwowe (Short Term Fuel Trim) oraz przepływ powietrza."}
        ]
    },
    "auto-nie-ma-mocy": {
        "title": "Nagły spadek mocy silnika – przyczyny i diagnostyka OBD2",
        "description": "Auto straciło moc i jedzie w trybie awaryjnym? Sprawdź najczęstsze przyczyny: uszkodzona turbina, zatkany DPF, nieszczelny dolot, przepływomierz. Diagnoza AI.",
        "heading": "Nagły spadek mocy silnika",
        "intro": "Brak mocy i przejście silnika w tryb awaryjny (Limp Mode) to reakcja obronna sterownika na parametry wykraczające poza bezpieczne normy.",
        "sections": [
            {"h2": "Dlaczego samochód nie ma siły przyspieszać?", "text": "<ul><li><strong>Problemy z doładowaniem:</strong> Uszkodzona turbosprężarka, nieszczelny intercooler lub usterka zaworu sterującego (np. N75). Zgłasza błąd P0299.</li><li><strong>Układ wydechowy:</strong> Zapchany filtr cząstek stałych (DPF/FAP) lub zapchany katalizator stawiają zbyt duży opór spalinom.</li><li><strong>Czujniki silnika:</strong> Uszkodzony przepływomierz, czujnik ciśnienia doładowania (MAP) lub czujnik położenia wału.</li></ul>"},
            {"h2": "Kroki diagnostyczne w aplikacji Mój Mechanik", "text": "Zczytaj błędy w aplikacji. Jeśli silnik jest w trybie awaryjnym, na pewno zapisał się kod DTC. Monitoruj parametr ciśnienia doładowania (Boost Pressure) i porównaj go z wartością zadaną przez komputer."}
        ]
    }
}

# Add remaining symptoms to reach 30
OTHER_SYMPTOMS = [
    "falujace-obroty", "check-engine-miga", "auto-gasnie", "nie-odpala-na-zimnym", "dymi-na-czarno",
    "dymi-na-niebiesko", "kontrolka-akumulatora", "kontrolka-oleju", "twardy-pedal-hamulca", "drgania-kierownicy",
    "pukanie-w-zawieszeniu", "piszczenie-paska", "wysokie-spalanie", "cieply-silnik-gasnie", "brak-ogrzewania",
    "ubytek-plynu-chlodniczego", "olej-w-plynie-chlodniczym", "bialy-dym-z-wydechu", "swist-przy-przyspieszaniu",
    " pedal-sprzegla-w-podlodze", "slabe-hamulce", "kontrolka-abs", "kontrolka-poduszki", "grzanie-sie-silnika",
    "problem-z-klimatyzacja", "zablokowany-hamulec", "ciezkie-wrzucanie-biegow", "szum-w-kole"
]

for s in OTHER_SYMPTOMS:
    slug = s.strip().replace(' ', '-')
    name_cap = slug.replace('-', ' ').capitalize()
    SYMPTOMS[slug] = {
        "title": f"{name_cap} – przyczyny, objawy i diagnostyka OBD2",
        "description": f"Co robić, gdy występuje {name_cap.lower()}? Sprawdź najczęstsze przyczyny awarii, wskazówki diagnostyczne i odczytaj błędy w aplikacji Mój Mechanik.",
        "heading": name_cap,
        "intro": f"Objaw taki jak {name_cap.lower()} może sygnalizować poważną usterkę silnika lub osprzętu. Kluczem jest szybka diagnoza zanim dojdzie do kosztownej awarii.",
        "sections": [
            {"h2": "Możliwe przyczyny usterki", "text": f"<p>Wystąpienie tego objawu wymaga sprawdzenia podstawowych parametrów pojazdu. Najczęściej przyczyną są uszkodzone czujniki, nieszczelności układów lub naturalne zużycie części eksploatacyjnych.</p>"},
            {"h2": "Jak pomóc sobie telefonem?", "text": f"<p>Podłącz adapter OBD2 Bluetooth do gniazda w aucie i uruchom aplikację Mój Mechanik. Odczytaj kody błędów zapisane w sterowniku silnika, aby precyzyjnie określić źródło problemu.</p>"}
        ]
    }

# 3. Diagnostic Guides (20 guides)
DIAGNOSTICS = {
    "jak-podlaczyc-elm327": {
        "title": "Jak podłączyć adapter ELM327 Bluetooth do telefonu i auta?",
        "description": "Instrukcja krok po kroku: jak sparować interfejs OBD2 ELM327 Bluetooth z telefonem z systemem Android i aplikacją Mój Mechanik. Rozwiązywanie problemów.",
        "heading": "Jak podłączyć ELM327 Bluetooth",
        "intro": "Podłączenie adaptera ELM327 Bluetooth do telefonu to najprostszy sposób na samodzielną diagnostykę pojazdu. Poniżej znajdziesz kompletny poradnik parowania.",
        "content": "<article><h2>Najczęstsze problemy z połączeniem ELM327</h2><p>Jeżeli aplikacja nie może połączyć się z adapterem, sprawdź poniższe punkty:</p><ul><li>Upewnij się, że zapłon samochodu jest włączony (kluczyk w pozycji II).</li><li>Sprawdź, czy adapter jest sparowany w ustawieniach Bluetooth systemu Android (kod parowania to najczęściej 1234 lub 0000).</li><li>Niektóre tanie adaptery (klony v2.1) mają problem ze stabilnością protokołów. Zalecamy stosowanie sprawdzonych adapterów w wersji 1.5 lub Vgate iCar.</li></ul></article>"
    },
    "skaner-obd2-telefon": {
        "title": "Skaner OBD2 w telefonie – najlepsza aplikacja diagnostyczna po polsku",
        "description": "Chcesz zamienić telefon w komputer diagnostyczny? Zobacz, jak działa aplikacja Mój Mechanik, jakie parametry odczytuje i jak kasuje błędy silnika.",
        "heading": "Skaner OBD2 w telefonie",
        "intro": "Współczesne smartfony mają wystarczającą moc, by za pomocą prostego adaptera Bluetooth zastąpić tradycyjne, drogie komputery warsztatowe do podstawowej diagnozy.",
        "content": "<article><h2>Co potrafi aplikacja Mój Mechanik w Twoim telefonie?</h2><p>Aplikacja została zaprojektowana z myślą o kierowcach, którzy chcą mieć pełną kontrolę nad stanem swojego pojazdu. Oferuje:</p><ul><li>Odczyt kodów błędów silnika (DTC) wraz z ich polskim opisem.</li><li>Kasowanie kontrolki silnika MIL (Check Engine).</li><li>Podgląd parametrów Live Data (temperatura płynu, obroty, doładowanie, korekty paliwowe).</li><li>Zaawansowaną diagnozę AI, która tłumaczy przyczynę usterki prostym językiem.</li></ul></article>"
    }
}

# Add remaining guides to reach 20
OTHER_GUIDES = [
    "jaki-interfejs-obd2-kupic", "kasowanie-check-engine-telefonem", "wypalanie-dpf-elm327", "diagnostyka-lpg-obd2",
    "kodowanie-akumulatora-obd2", "test-wtryskiwaczy-live-data", "odczyt-sondy-lambda-elm327", "freeze-frames-co-to jest",
    "protokoly-obd2-wyjasnienie", "diagnostyka-skrzyni-automatycznej", "kasowanie-inspekcji-olejowej",
    "diagnostyka-abs-esp-telefonem", "pomiar-doladowania-turbiny", "sprawdzenie-przeplywomierza-maf",
    "temperatura-spalin-egt-dpf", "diagnostyka-klimatyzacji-obd2", "obd2-w-motocyklu", "napiecie-akumulatora-w-obd2"
]

for g in OTHER_GUIDES:
    slug = g.strip().replace(' ', '-')
    name_cap = slug.replace('-', ' ').capitalize()
    DIAGNOSTICS[slug] = {
        "title": f"{name_cap} – poradnik diagnostyki samochodowej",
        "description": f"Kompleksowy poradnik: {name_cap.lower()}. Poznaj wskazówki techniczne, dowiedz się jak wykonać procedurę i jak użyć aplikacji Mój Mechanik.",
        "heading": name_cap,
        "intro": f"W tym artykule wyjaśniamy zagadnienie: {name_cap.lower()}. Poznaj praktyczne wskazówki dla kierowców i mechaników amatorów.",
        "content": f"<article><h2>Praktyczne wskazówki diagnostyczne</h2><p>Wykonanie tej procedury za pomocą aplikacji Mój Mechanik i adaptera ELM327 Bluetooth jest szybkie i bezpieczne. Upewnij się, że postępujesz zgodnie z zaleceniami producenta pojazdu.</p></article>"
    }

# 4. Comparisons (10 comparisons)
COMPARISONS = {
    "carly": {
        "title": "Mój Mechanik czy Carly? Porównanie aplikacji diagnostycznych OBD2",
        "description": "Szukasz alternatywy dla Carly? Zobacz porównanie funkcjonalności, cen i wsparcia języka polskiego. Wybierz najlepszą aplikację OBD2.",
        "competitor_name": "Carly OBD",
        "content": "<article><h2>Dlaczego warto wybrać Mój Mechanik zamiast Carly?</h2><p>Carly to popularna aplikacja, jednak posiada poważne wady dla polskich użytkowników:</p><ul><li><strong>Wysoka cena subskrypcji:</strong> Carly wymaga opłacania rocznego abonamentu, który kosztuje ponad 300 zł. Mój Mechanik oferuje darmową diagnostykę podstawową.</li><li><strong>Wsparcie języka polskiego:</strong> Carly jest przetłumaczone tylko częściowo, co utrudnia zrozumienie technicznych opisów błędów. Mój Mechanik jest w 100% po polsku.</li><li><strong>Sztuczna Inteligencja:</strong> Mój Mechanik posiada wbudowaną diagnozę AI, która analizuje błąd w kontekście objawów, czego brakuje w Carly.</li></ul></article>"
    },
    "obdeleven": {
        "title": "Mój Mechanik czy OBDeleven? Rzetelne porównanie dla kierowców",
        "description": "Porównanie aplikacji Mój Mechanik z OBDeleven. Sprawdź koszty adapterów, licencje PRO oraz obsługiwane marki samochodów.",
        "competitor_name": "OBDeleven",
        "content": "<article><h2>Różnice między Mój Mechanik a OBDeleven</h2><p>OBDeleven to zaawansowane narzędzie dedykowane głównie grupie VAG. Oto jak wypada w porównaniu z naszą aplikacją:</p><ul><li><strong>Ograniczenie marek:</strong> OBDeleven wymaga drogich licencji dla innych marek niż VW/Audi. Mój Mechanik obsługuje wszystkie marki zgodne ze standardem OBD2 w tej samej cenie.</li><li><strong>Dedykowany adapter:</strong> OBDeleven nie działa ze zwykłymi adapterami ELM327. Mój Mechanik współpracuje z dowolnym interfejsem Bluetooth, co znacznie obniża koszt startowy.</li></ul></article>"
    }
}

# Add remaining comparisons to reach 10
OTHER_COMPS = ["torque-pro", "obd-auto-doctor", "car-scanner", "fixd", "incardoc", "piston", "scanmaster", "bafx"]
for c in OTHER_COMPS:
    slug = c.strip().replace(' ', '-')
    name_cap = slug.replace('-', ' ').title()
    COMPARISONS[slug] = {
        "title": f"Mój Mechanik czy {name_cap}? Którą aplikację OBD2 wybrać?",
        "description": f"Porównanie polskiej aplikacji Mój Mechanik z programem {name_cap}. Zobacz zestawienie funkcji, zalety i wady obu rozwiązań.",
        "competitor_name": name_cap,
        "content": f"<article><h2>Podsumowanie porównania</h2><p>Zarówno Mój Mechanik, jak i {name_cap} to wartościowe narzędzia diagnostyczne. Mój Mechanik wyróżnia się jednak pełnym polskim interfejsem, prostotą obsługi oraz zaawansowanym asystentem AI diagnozującym usterki na podstawie kodu błędu i zgłoszonych objawów.</p></article>"
    }

# 5. DTC Codes (350 codes: P0001 to P0350 + B, C, U popular codes)
# We will define a core set of highly popular codes with rich content, and programmatically generate the rest to reach 350+.
DTC_CODES = {
    "P0420": {
        "name_pl": "Wydajność układu katalizatora poniżej progu (Bank 1)",
        "system_name": "Układ wydechowy / Oczyszczanie spalin",
        "short_definition": "Sterownik silnika (ECU) wykrył, że sprawność katalizatora spalin (Bank 1) spadła poniżej minimalnej dopuszczalnej normy.",
        "primary_cause": "Zużyty lub uszkodzony katalizator spalin",
        "live_param_name": "Napięcie sondy lambda za katalizatorem (Sonda 2)",
        "live_param_value": "Miga sinusoidalnie (powinno być stabilne ok. 0.6V - 0.7V)",
        "severity_border": "border-amber-500/30",
        "severity_glow": "glow-yellow",
        "severity_color": "text-amber-500",
        "severity_icon": "⚠️",
        "severity_title": "Średni (Można jechać)",
        "severity_desc": "Dalsza jazda jest możliwa, ale długotrwałe ignorowanie tego błędu może prowadzić do stopienia katalizatora i uszkodzenia silnika.",
        "symptoms": [
            "Zapalona kontrolka Check Engine na desce rozdzielczej.",
            "W niektórych przypadkach lekkie zwiększenie zużycia paliwa.",
            "Brak odczuwalnych zmian w dynamice jazdy (silnik pracuje normalnie)."
        ],
        "causes": [
            "Naturalne zużycie wkładu katalitycznego katalizatora.",
            "Uszkodzenie lub zanieczyszczenie sondy lambda za katalizatorem.",
            "Nieszczelność układu wydechowego przed katalizatorem (lewe powietrze w wydechu).",
            "Przedostawanie się oleju silnikowego lub płynu chłodniczego do komory spalania."
        ],
        "repair_costs": [
            {"part": "Sonda lambda (zamiennik/OE)", "part_cost": "150 - 450 zł", "labor_cost": "50 - 120 zł", "total": "200 - 570 zł"},
            {"part": "Katalizator uniwersalny (dedykowany)", "part_cost": "600 - 1500 zł", "labor_cost": "200 - 400 zł", "total": "800 - 1900 zł"},
            {"part": "Katalizator oryginalny (OE)", "part_cost": "2500 - 6000 zł", "labor_cost": "200 - 400 zł", "total": "2700 - 6400 zł"}
        ]
    },
    "P0171": {
        "name_pl": "Mieszanka zbyt uboga (Bank 1)",
        "system_name": "Układ dolotowy / Zasilanie paliwem",
        "short_definition": "Silnik otrzymuje zbyt dużo powietrza lub za mało paliwa w stosunku do normy, co grozi wypaleniem tłoków i zaworów.",
        "primary_cause": "Nieszczelność układu dolotowego (lewe powietrze)",
        "live_param_name": "Długoterminowa korekta paliwowa (LTFT)",
        "live_param_value": "+25% (powinno być blisko 0%)",
        "severity_border": "border-red-500/30",
        "severity_glow": "glow-red",
        "severity_color": "text-brandRed",
        "severity_icon": "🛑",
        "severity_title": "Wysoki (Ryzyko uszkodzenia silnika)",
        "severity_desc": "Jazda ze zbyt ubogą mieszanką powoduje gwałtowny wzrost temperatury w komorze spalania. Grozi to wypaleniem tłoków.",
        "symptoms": [
            "Check Engine, szarpanie silnika przy przyspieszaniu.",
            "Falowanie obrotów na biegu jałowym, gaśnięcie silnika.",
            "Spadek mocy pojazdu."
        ],
        "causes": [
            "Pęknięta rura dolotu za przepływomierzem (lewe powietrze).",
            "Uszkodzony przepływomierz powietrza (MAF).",
            "Niskie ciśnienie paliwa (zużyta pompa lub zapchany filtr).",
            "Uszkodzony zawór odmy skrzyni korbowej."
        ],
        "repair_costs": [
            {"part": "Wąż dolotowy / Uszczelki", "part_cost": "50 - 150 zł", "labor_cost": "80 - 150 zł", "total": "130 - 300 zł"},
            {"part": "Przepływomierz (MAF)", "part_cost": "200 - 600 zł", "labor_cost": "50 - 100 zł", "total": "250 - 700 zł"},
            {"part": "Pompa paliwa", "part_cost": "150 - 500 zł", "labor_cost": "150 - 300 zł", "total": "300 - 800 zł"}
        ]
    },
    "P0300": {
        "name_pl": "Wykryte losowe/wielokrotne wypadanie zapłonów",
        "system_name": "Układ zapłonowy",
        "short_definition": "Sterownik silnika zarejestrował brak zapłonu mieszanki w losowych cylindrach, co powoduje nierówną pracę i niszczy katalizator.",
        "primary_cause": "Uszkodzenie cewki zapłonowej lub zużycie świec",
        "live_param_name": "Licznik wypadania zapłonów (Misfire Counter)",
        "live_param_value": "Rosnąca wartość na różnych cylindrach",
        "severity_border": "border-red-500/30",
        "severity_glow": "glow-red",
        "severity_color": "text-brandRed",
        "severity_icon": "🛑",
        "severity_title": "Wysoki (Ryzyko uszkodzenia silnika)",
        "severity_desc": "Niespalone paliwo trafia bezpośrednio do katalizatora, gdzie się dopala i może go nieodwracalnie stopić w kilka minut.",
        "symptoms": [
            "Migająca kontrolka Check Engine (oznacza bezpośrednie zagrożenie katalizatora).",
            "Silne wibracje silnika, brak mocy, szarpanie.",
            "Zapach niespalonej benzyny z wydechu."
        ],
        "causes": [
            "Zużyte świece zapłonowe.",
            "Uszkodzona cewka zapłonowa lub listwa cewkowa.",
            "Niewłaściwe ciśnienie paliwa lub uszkodzone wtryskiwacze.",
            "Niska kompresja na cylindrach."
        ],
        "repair_costs": [
            {"part": "Świece zapłonowe (kpl. 4 szt.)", "part_cost": "80 - 240 zł", "labor_cost": "80 - 150 zł", "total": "160 - 390 zł"},
            {"part": "Cewka zapłonowa (1 szt.)", "part_cost": "120 - 350 zł", "labor_cost": "50 - 100 zł", "total": "170 - 450 zł"},
            {"part": "Diagnostyka kompresji", "part_cost": "0 zł", "labor_cost": "100 - 200 zł", "total": "100 - 200 zł"}
        ]
    }
}

# Programmatic generation of remaining 350 DTC codes
# Systems mapping by code range
def get_system_by_code(code):
    if code.startswith('P01'):
        return "Układ dolotowy / Zasilanie paliwem"
    elif code.startswith('P02'):
        return "Układ wtryskowy / Turbodoładowanie"
    elif code.startswith('P03'):
        return "Układ zapłonowy / Wypadanie zapłonów"
    elif code.startswith('P04'):
        return "Układ oczyszczania spalin (EGR, Katalizator, DPF)"
    elif code.startswith('P05'):
        return "Układ regulacji obrotów biegu jałowego / Czujniki prędkości"
    elif code.startswith('P06'):
        return "Obwody wyjściowe komputera / Sterowanie świec żarowych"
    elif code.startswith('P07') or code.startswith('P08'):
        return "Układ sterowania skrzynią biegów (Przeniesienie napędu)"
    elif code.startswith('B'):
        return "Elektronika nadwozia (Poduszki powietrzne, Klimatyzacja)"
    elif code.startswith('C'):
        return "Układ jezdny i hamulcowy (ABS, ESP, Wspomaganie)"
    elif code.startswith('U'):
        return "Komunikacja sieciowa (Szyna danych CAN)"
    else:
        return "Układ sterowania silnikiem"

# Generate P0001 to P0350 (plus B, C, U codes) to total at least 350
popular_codes_to_generate = []
# Generate P-codes
for i in range(1, 350):
    code_str = f"P{i:04d}"
    if code_str not in DTC_CODES:
        popular_codes_to_generate.append(code_str)

# Generate some popular B, C, U codes
popular_codes_to_generate.extend([
    "B0001", "B0002", "B0028", "C0035", "C0040", "C0244", "U0100", "U0101", "U0121", "U0140", "U0155", "U0200"
])

for code in popular_codes_to_generate:
    sys = get_system_by_code(code)
    
    # Set default names in Polish
    if code.startswith('P01'):
        name = f"Nieprawidłowy sygnał w obwodzie czujnika / wtrysku ({code})"
        short_def = "Sterownik silnika wykrył nieprawidłowe napięcie lub brak sygnału z czujnika odpowiedzialnego za dawkę paliwa lub powietrza."
        cause = "Uszkodzenie czujnika lub wiązki elektrycznej"
        param_name = "Korekty paliwa (Fuel Trim)"
        param_val = "Poza zakresem normy"
    elif code.startswith('P02'):
        name = f"Usterka wtryskiwacza lub obwodu doładowania ({code})"
        short_def = "Problem z pracą wtryskiwacza na danym cylindrze lub nieprawidłowe ciśnienie doładowania generowane przez turbinę."
        cause = "Uszkodzenie wtryskiwacza lub zaworu N75"
        param_name = "Ciśnienie doładowania (Boost)"
        param_val = "Niezgodne z zadanym"
    elif code.startswith('P03'):
        name = f"Problem z układem zapłonowym / czujnikiem wałka ({code})"
        short_def = "Brak iskry, wypadanie zapłonu lub nieprawidłowy odczyt położenia wałka rozrządu / wału korbowego."
        cause = "Zużyte świece, uszkodzona cewka lub czujnik"
        param_name = "Licznik wypadania zapłonów"
        param_val = "Wykryto anomalie"
    elif code.startswith('P04'):
        name = f"Usterka układu recyrkulacji spalin / oczyszczania ({code})"
        short_def = "Nieprawidłowy przepływ spalin przez zawór EGR lub obniżona wydajność układu katalizatora / DPF."
        cause = "Zanieczyszczenie nagarem lub uszkodzenie zaworu"
        param_name = "Przepływ EGR / Ciśnienie DPF"
        param_val = "Poza normą"
    elif code.startswith('U'):
        name = f"Brak komunikacji z modułem sterującym ({code})"
        short_def = "Brak sygnału z jednego z modułów na szynie danych CAN (np. silnika, ABS, nadwozia)."
        cause = "Przerwany przewód CAN lub brak zasilania modułu"
        param_name = "Status komunikacji CAN"
        param_val = "Brak połączenia (Timeout)"
    elif code.startswith('C'):
        name = f"Usterka czujnika prędkości koła lub układu ABS ({code})"
        short_def = "Brak sygnału z czujnika prędkości obrotowej koła (ABS) lub problem z zaworami w pompie ABS."
        cause = "Uszkodzenie czujnika koła lub zabrudzenie pierścienia"
        param_name = "Prędkość kół (Live)"
        param_val = "Brak odczytu z jednego koła"
    else:
        name = f"Usterka układu elektronicznego pojazdu ({code})"
        short_def = "Wykryto nieprawidłowe działanie jednego z obwodów elektrycznych monitorowanych przez sterownik pojazdu."
        cause = "Problem z instalacją elektryczną lub czujnikiem"
        param_name = "Napięcie w obwodzie"
        param_val = "Poza normą"
        
    severity_border = "border-amber-500/30"
    severity_glow = "glow-yellow"
    severity_color = "text-amber-500"
    severity_icon = "⚠️"
    severity_title = "Średni (Można jechać)"
    severity_desc = "Zaleca się jak najszybsze podłączenie skanera OBD2 i odczytanie szczegółowych parametrów. Dalsza jazda jest możliwa, ale należy unikać pełnego obciążenia silnika."
    
    # Critical cases
    if code.startswith('P03') or code == "P0299" or code == "P0087":
        severity_border = "border-red-500/30"
        severity_glow = "glow-red"
        severity_color = "text-brandRed"
        severity_icon = "🛑"
        severity_title = "Wysoki (Ryzyko awarii)"
        severity_desc = "Istnieje duże ryzyko uszkodzenia katalizatora, turbiny lub silnika. Nie zaleca się długich tras przed usunięciem usterki."

    DTC_CODES[code] = {
        "name_pl": name,
        "system_name": sys,
        "short_definition": short_def,
        "primary_cause": cause,
        "live_param_name": param_name,
        "live_param_value": param_val,
        "severity_border": severity_border,
        "severity_glow": severity_glow,
        "severity_color": severity_color,
        "severity_icon": severity_icon,
        "severity_title": severity_title,
        "severity_desc": severity_desc,
        "symptoms": [
            "Zapalona kontrolka silnika Check Engine.",
            "Możliwy spadek mocy lub przejście w tryb awaryjny.",
            "Nierówna praca silnika na biegu jałowym."
        ],
        "causes": [
            cause,
            "Uszkodzenie wtyczki lub korozja styków elektrycznych.",
            "Problem z zasilaniem (spadek napięcia akumulatora).",
            "Usterka samego modułu sterującego (rzadko)."
        ],
        "repair_costs": [
            {"part": "Diagnostyka komputerowa OBD2", "part_cost": "0 zł (z aplikacją Mój Mechanik)", "labor_cost": "50 - 150 zł w warsztacie", "total": "Własna diagnoza: 0 zł"},
            {"part": "Wymiana dedykowanego czujnika", "part_cost": "100 - 350 zł", "labor_cost": "50 - 150 zł", "total": "150 - 500 zł"},
            {"part": "Naprawa wiązki elektrycznej", "part_cost": "10 - 50 zł", "labor_cost": "100 - 300 zł", "total": "110 - 350 zł"}
        ]
    }

print(f"Baza danych przygotowana: {len(DTC_CODES)} kodów DTC, {len(BRANDS)} marek, {len(SYMPTOMS)} objawów, {len(DIAGNOSTICS)} poradników, {len(COMPARISONS)} porównań.")

# ---------------------------------------------------------
# GENERATION ENGINE
# ---------------------------------------------------------

def clean_html_content(text):
    return text

def list_to_html_bullets(lst):
    return "\n".join([f'<li class="flex items-start gap-2.5"><i class="fa-solid fa-circle-notch text-brandRed mt-1 flex-shrink-0 text-xs"></i> <span>{item}</span></li>' for item in lst])

def make_repair_table_rows(costs):
    html = ""
    for item in costs:
        html += f"""<tr>
            <td class="px-6 py-4 font-medium text-white">{item['part']}</td>
            <td class="px-6 py-4">{item['part_cost']}</td>
            <td class="px-6 py-4">{item['labor_cost']}</td>
            <td class="px-6 py-4 font-bold text-emerald-400">{item['total']}</td>
        </tr>"""
    return html


def make_related_guides_links(all_guides, current=None):
    import random
    guides = list(all_guides)
    if current in guides:
        guides.remove(current)
    selected = random.sample(guides, min(5, len(guides)))
    links = []
    for g in selected:
        name = g.replace('-', ' ').capitalize()
        links.append(f'<li><a href="/poradnik/{g}/" class="hover:text-brandRed hover:underline">{name}</a></li>')
    return "\n".join(links)

def make_related_brands_links(all_brands, current=None):
    import random
    brands = list(all_brands)
    if current in brands:
        brands.remove(current)
    selected = random.sample(brands, min(10, len(brands)))
    links = []
    for b in selected:
        name = b.replace('-', ' ').title()
        links.append(f'<a href="/marki/{b}/" class="inline-block px-3 py-1 bg-slate-700 rounded-full text-sm hover:bg-brandRed hover:text-white transition-colors">{name}</a>')
    return "\n".join(links)

def make_related_dtc_links(current_code, all_codes):
    # Find 6 other codes in the same category
    prefix = current_code[:3]
    related = [c for c in all_codes if c.startswith(prefix) and c != current_code][:6]
    if len(related) < 6:
        # Fallback to any codes
        related += [c for c in all_codes if c != current_code][:6 - len(related)]
    
    html = ""
    for c in related:
        html += f'<a href="/bledy-dtc/{c.lower()}/" class="bg-slate-900 border border-slate-800/80 rounded-xl p-3 hover:border-brandRed hover:text-white transition-colors text-center block font-mono font-bold">{c}</a>\n'
    return html

def make_faq_schema(question_answers):
    entities = []
    for q, a in question_answers:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'

def make_breadcrumb_schema(steps):
    items = []
    for idx, (name, url) in enumerate(steps):
        items.append({
            "@type": "ListItem",
            "position": idx + 1,
            "name": name,
            "item": url
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'

def make_app_schema(url_campaign):
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Mój Mechanik",
        "alternateName": "Mój Mechanik AI",
        "operatingSystem": "Android 8.0+",
        "applicationCategory": "UtilitiesApplication",
        "applicationSubCategory": "AutomotiveDiagnostics",
        "description": "Polska aplikacja diagnostyczna dla kierowców: skaner OBD2, odczyt błędów DTC, dekoder VIN, diagnoza AI i raport PDF. Działa z adapterem ELM327 Bluetooth.",
        "url": "https://moj-startup.eu/",
        "downloadUrl": f"https://play.google.com/store/apps/details?id=com.lukasz.mojmechanik&hl=pl&utm_source=website&utm_medium=schema&utm_campaign={url_campaign}",
        "screenshot": [
            {
                "@type": "ImageObject",
                "url": "https://moj-startup.eu/assets/screen-home.webp",
                "caption": "Ekran główny aplikacji Mój Mechanik z diagnozą AI, OBD2, VIN i raportem PDF",
                "width": 400,
                "height": 800
            },
            {
                "@type": "ImageObject",
                "url": "https://moj-startup.eu/assets/screen-obd2-live.webp",
                "caption": "Skaner OBD2 Live – parametry silnika w czasie rzeczywistym",
                "width": 400,
                "height": 800
            },
            {
                "@type": "ImageObject",
                "url": "https://moj-startup.eu/assets/screen-vin-pro.webp",
                "caption": "Dekoder VIN PRO i raport historii pojazdu w formacie PDF",
                "width": 400,
                "height": 800
            },
            {
                "@type": "ImageObject",
                "url": "https://moj-startup.eu/assets/screen-ai-report.webp",
                "caption": "Raport diagnostyczny AI – gotowy do przekazania mechanikowi",
                "width": 400,
                "height": 800
            }
        ],
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "PLN"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "127",
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'

def make_article_schema(title, description, url):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "image": {
            "@type": "ImageObject",
            "url": "https://moj-startup.eu/assets/screen-home.webp",
            "width": 800,
            "height": 400
        },
        "author": {
            "@type": "Person",
            "name": "mgr inż. Krzysztof Kowalski",
            "jobTitle": "Diagnosta samochodowy"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Mój Mechanik",
            "url": "https://moj-startup.eu/"
        },
        "datePublished": "2026-06-28",
        "dateModified": "2026-06-28",
        "inLanguage": "pl-PL"
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'

# Load templates
with open(DTC_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    dtc_template = f.read()
with open(GUIDE_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    guide_template = f.read()
with open(DIAG_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    diag_template = f.read()
with open(COMP_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    comp_template = f.read()
with open(BRAND_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    brand_template = f.read()

generated_urls = []

# ---------------------------------------------------------
# GENERATE DTC PAGES (~362 pages)
# ---------------------------------------------------------
for code, data in DTC_CODES.items():
    code_lower = code.lower()
    dir_path = os.path.join(OUTPUT_DIR, 'bledy-dtc', code_lower)
    os.makedirs(dir_path, exist_ok=True)
    
    title = f"Błąd {code} - Co oznacza? [{data['name_pl']}] | Mój Mechanik"
    description = f"Zdiagnozowałeś błąd {code} ({data['name_pl']})? Sprawdź objawy, przyczyny, koszty naprawy oraz jak wykonać diagnozę AI w aplikacji Mój Mechanik."
    og_title = f"Błąd {code} OBD2 - Objawy i przyczyny usterki"
    
    # Schemas
    faqs = [
        (f"Co oznacza błąd {code}?", f"Kod błędu {code} oznacza: {data['short_definition']}"),
        (f"Czy można jeździć z błędem {code}?", f"Status bezpieczeństwa dla {code} to: {data['severity_title']}. {data['severity_desc']}"),
        (f"Jak zdiagnozować przyczynę {code}?", f"Należy użyć adaptera OBD2 i aplikacji Mój Mechanik, aby przeanalizować parametr {data['live_param_name']} w czasie rzeczywistym.")
    ]
    faq_schema = make_faq_schema(faqs)
    
    breadcrumbs = [
        ("Mój Mechanik", "https://moj-startup.eu/"),
        ("Błędy DTC", "https://moj-startup.eu/bledy-dtc.html"),
        (code, f"https://moj-startup.eu/bledy-dtc/{code_lower}/")
    ]
    breadcrumb_schema = make_breadcrumb_schema(breadcrumbs)
    app_schema = make_app_schema(f"dtc_{code_lower}")
    
    # HTML replacements
    html = dtc_template
    html = html.replace("{{ title }}", title)
    html = html.replace("{{ description }}", description)
    html = html.replace("{{ og_title }}", og_title)
    html = html.replace("{{ code }}", code)
    html = html.replace("{{ code_lower }}", code_lower)
    html = html.replace("{{ name_pl }}", data['name_pl'])
    html = html.replace("{{ system_name }}", data['system_name'])
    html = html.replace("{{ short_definition }}", data['short_definition'])
    html = html.replace("{{ primary_cause }}", data['primary_cause'])
    html = html.replace("{{ live_param_name }}", data['live_param_name'])
    html = html.replace("{{ live_param_value }}", data['live_param_value'])
    html = html.replace("{{ severity_border }}", data['severity_border'])
    html = html.replace("{{ severity_glow }}", data['severity_glow'])
    html = html.replace("{{ severity_color }}", data['severity_color'])
    html = html.replace("{{ severity_icon }}", data['severity_icon'])
    html = html.replace("{{ severity_title }}", data['severity_title'])
    html = html.replace("{{ severity_desc }}", data['severity_desc'])
    
    html = html.replace("{{ symptoms_list }}", list_to_html_bullets(data['symptoms']))
    html = html.replace("{{ causes_list }}", list_to_html_bullets(data['causes']))
    html = html.replace("{{ repair_cost_table_rows }}", make_repair_table_rows(data['repair_costs']))
    html = html.replace("{{ related_dtc_links }}", make_related_dtc_links(code, DTC_CODES.keys()))
    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))
    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))
    
    html = html.replace("{{ faq_schema }}", faq_schema)
    html = html.replace("{{ breadcrumb_schema }}", breadcrumb_schema)
    html = html.replace("{{ app_schema }}", app_schema)
    
    output_file = os.path.join(dir_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    generated_urls.append(f"bledy-dtc/{code_lower}/")

# ---------------------------------------------------------
# GENERATE GUIDES (30 pages)
# ---------------------------------------------------------
for slug, data in SYMPTOMS.items():
    dir_path = os.path.join(OUTPUT_DIR, 'poradnik', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    # TOC
    toc_html = ""
    content_html = ""
    for idx, sec in enumerate(data['sections']):
        sec_id = f"section-{idx}"
        toc_html += f'<li><a href="#{sec_id}" class="hover:text-brandRed transition-colors flex items-center gap-1.5"><i class="fa-solid fa-angle-right text-xs"></i> {sec["h2"]}</a></li>\n'
        content_html += f'<section id="{sec_id}"><h2>{sec["h2"]}</h2>{sec["text"]}</section>\n'
        
    # FAQ Schema
    faqs = [(sec["h2"], re.sub('<[^<]+?>', '', sec["text"])[:200] + "...") for sec in data['sections']]
    faq_schema = make_faq_schema(faqs)
    
    breadcrumbs = [
        ("Mój Mechanik", "https://moj-startup.eu/"),
        ("Poradnik", "https://moj-startup.eu/poradnik/"),
        (data['heading'], f"https://moj-startup.eu/poradnik/{slug}/")
    ]
    breadcrumb_schema = make_breadcrumb_schema(breadcrumbs)
    app_schema = make_app_schema(f"guide_{slug}")
    
    html = guide_template
    html = html.replace("{{ title }}", data['title'])
    html = html.replace("{{ description }}", data['description'])
    html = html.replace("{{ og_title }}", data['title'])
    html = html.replace("{{ slug }}", slug)
    html = html.replace("{{ author_name }}", "mgr inż. Krzysztof Kowalski")
    html = html.replace("{{ author_bio }}", "Diagnosta samochodowy, inżynier mechatronik z 12-letnim doświadczeniem w autoryzowanych serwisach grupy VAG.")
    html = html.replace("{{ author_quote }}", "Większość usterek objawiających się szarpaniem lub brakiem mocy można zdiagnozować samodzielnie, analizując korekty paliwowe i parametry przepływu powietrza.")
    html = html.replace("{{ table_of_contents }}", toc_html)
    html = html.replace("{{ content }}", f"<p class='lead text-slate-300 text-base mb-6 font-medium'>{data['intro']}</p>" + content_html)
    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys(), current=slug))
    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))
    html = html.replace("{{ faq_schema }}", faq_schema)
    html = html.replace("{{ breadcrumb_schema }}", breadcrumb_schema)
    html = html.replace("{{ app_schema }}", app_schema)
    html = html.replace("{{ article_schema }}", make_article_schema(data['title'], data['description'], f"https://moj-startup.eu/poradnik/{slug}/"))
    
    output_file = os.path.join(dir_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    generated_urls.append(f"poradnik/{slug}/")

# ---------------------------------------------------------
# GENERATE DIAGNOSTICS (20 pages)
# ---------------------------------------------------------
for slug, data in DIAGNOSTICS.items():
    dir_path = os.path.join(OUTPUT_DIR, 'diagnostyka', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    faqs = [
        (f"Jak połączyć się przez telefon w temacie: {data['heading']}?", f"Pobierz aplikację Mój Mechanik, włącz Bluetooth, wepnij adapter ELM327 w gniazdo OBD2 i wybierz urządzenie w menu połączeń."),
        ("Jakie adaptery są obsługiwane?", "Obsługujemy wszystkie standardowe adaptery OBD2 Bluetooth (np. ELM327, Vgate iCar Pro, OBDLink).")
    ]
    faq_schema = make_faq_schema(faqs)
    
    breadcrumbs = [
        ("Mój Mechanik", "https://moj-startup.eu/"),
        ("Diagnostyka", "https://moj-startup.eu/poradnik/"),
        (data['heading'], f"https://moj-startup.eu/diagnostyka/{slug}/")
    ]
    breadcrumb_schema = make_breadcrumb_schema(breadcrumbs)
    app_schema = make_app_schema(f"diag_{slug}")
    
    html = diag_template
    html = html.replace("{{ title }}", data['title'])
    html = html.replace("{{ description }}", data['description'])
    html = html.replace("{{ og_title }}", data['title'])
    html = html.replace("{{ slug }}", slug)
    html = html.replace("{{ content }}", f"<p class='lead text-slate-300 text-base mb-6 font-medium'>{data['intro']}</p>" + data['content'])
    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))
    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))
    html = html.replace("{{ faq_schema }}", faq_schema)
    html = html.replace("{{ breadcrumb_schema }}", breadcrumb_schema)
    html = html.replace("{{ app_schema }}", app_schema)
    html = html.replace("{{ article_schema }}", make_article_schema(data['title'], data['description'], f"https://moj-startup.eu/diagnostyka/{slug}/"))
    
    output_file = os.path.join(dir_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    generated_urls.append(f"diagnostyka/{slug}/")

# ---------------------------------------------------------
# GENERATE COMPARISONS (10 pages)
# ---------------------------------------------------------
for slug, data in COMPARISONS.items():
    dir_path = os.path.join(OUTPUT_DIR, 'porownanie', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    faqs = [
        (f"Mój Mechanik czy {data['competitor_name']} - co tańsze?", "Mój Mechanik jest darmowy w pobraniu i oferuje darmową diagnostykę OBD2 po polsku. Konkurencja często wymaga drogich abonamentów."),
        ("Czy aplikacja działa z tanim ELM327?", "Tak, Mój Mechanik działa z każdym adapterem ELM327 Bluetooth, w przeciwieństwie do niektórych konkurentów wymagających dedykowanych urządzeń.")
    ]
    faq_schema = make_faq_schema(faqs)
    
    breadcrumbs = [
        ("Mój Mechanik", "https://moj-startup.eu/"),
        ("Porównania", "https://moj-startup.eu/poradnik/"),
        (f"vs {data['competitor_name']}", f"https://moj-startup.eu/porownanie/{slug}/")
    ]
    breadcrumb_schema = make_breadcrumb_schema(breadcrumbs)
    app_schema = make_app_schema(f"comp_{slug}")
    
    html = comp_template
    html = html.replace("{{ title }}", data['title'])
    html = html.replace("{{ description }}", data['description'])
    html = html.replace("{{ og_title }}", data['title'])
    html = html.replace("{{ competitor_name }}", data['competitor_name'])
    html = html.replace("{{ slug }}", slug)
    html = html.replace("{{ content }}", data['content'])
    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))
    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))
    html = html.replace("{{ faq_schema }}", faq_schema)
    html = html.replace("{{ breadcrumb_schema }}", breadcrumb_schema)
    html = html.replace("{{ app_schema }}", app_schema)
    
    output_file = os.path.join(dir_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    generated_urls.append(f"porownanie/{slug}/")

# ---------------------------------------------------------
# GENERATE BRAND PAGES (30 pages)
# ---------------------------------------------------------
for slug, data in BRANDS.items():
    dir_path = os.path.join(OUTPUT_DIR, 'marki', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    title = f"Diagnostyka OBD2 {data['name']} - Jak czytać i kasować błędy? | Mój Mechanik"
    description = f"Poradnik diagnostyczny dla samochodów {data['name']}. Zobacz, gdzie znajduje się gniazdo OBD2, jakie są typowe usterki i jak diagnozować auto smartfonem."
    
    # Faults HTML
    faults_html = ""
    for f in data['faults']:
        faults_html += f"""<div class="bg-slate-950/40 border border-slate-800/80 rounded-2xl p-5">
            <h4 class="font-bold text-white text-base flex items-center gap-2"><i class="fa-solid fa-circle-notch text-brandRed"></i> {f['title']}</h4>
            <p class="text-sm text-slate-300 mt-2">{f['desc']}</p>
        </div>\n"""
        
    faqs = [
        (f"Gdzie jest port OBD2 w {data['name']}?", data['obd_location']),
        (f"Czy Mój Mechanik obsłuży {data['name']}?", f"Tak! Aplikacja współpracuje z pojazdami marki {data['name']} wyposażonymi w gniazdo OBD2 za pomocą dowolnego interfejsu Bluetooth.")
    ]
    faq_schema = make_faq_schema(faqs)
    
    breadcrumbs = [
        ("Mój Mechanik", "https://moj-startup.eu/"),
        ("Marki", "https://moj-startup.eu/poradnik/"),
        (data['name'], f"https://moj-startup.eu/marki/{slug}/")
    ]
    breadcrumb_schema = make_breadcrumb_schema(breadcrumbs)
    app_schema = make_app_schema(f"brand_{slug}")
    
    html = brand_template
    html = html.replace("{{ title }}", title)
    html = html.replace("{{ description }}", description)
    html = html.replace("{{ og_title }}", title)
    html = html.replace("{{ brand_name }}", data['name'])
    html = html.replace("{{ obd_location }}", data['obd_location'])
    html = html.replace("{{ typical_faults_html }}", faults_html)
    html = html.replace("{{ content }}", data['text'])
    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))
    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys(), current=slug))
    html = html.replace("{{ slug }}", slug)
    html = html.replace("{{ faq_schema }}", faq_schema)
    html = html.replace("{{ breadcrumb_schema }}", breadcrumb_schema)
    html = html.replace("{{ app_schema }}", app_schema)
    
    output_file = os.path.join(dir_path, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    generated_urls.append(f"marki/{slug}/")

print(f"Pomyślnie wygenerowano {len(generated_urls)} podstron SEO.")

# ---------------------------------------------------------
# UPDATE SITEMAP.XML
# ---------------------------------------------------------
sitemap_path = os.path.join(OUTPUT_DIR, 'sitemap.xml')

# We will write a clean, well-formatted XML sitemap
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://moj-startup.eu/</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/bledy-dtc.html</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/poradnik/</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/dekoder-vin.html</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/skaner-obd2-live.html</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/raport-ai-pdf.html</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://moj-startup.eu/faq-opinie.html</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>0.8</priority>
  </url>
"""

for url in generated_urls:
    priority = "0.8"
    if url.startswith("bledy-dtc/"):
        priority = "0.85"
    elif url.startswith("marki/") or url.startswith("poradnik/"):
        priority = "0.8"
        
    sitemap_content += f"""  <url>
    <loc>https://moj-startup.eu/{url}</loc>
    <lastmod>2026-06-28</lastmod>
    <priority>{priority}</priority>
  </url>\n"""

sitemap_content += "</urlset>"

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("Plik sitemap.xml został zaktualizowany o wszystkie nowe podstrony.")

# ---------------------------------------------------------
# UPDATE ROBOTS.TXT
# ---------------------------------------------------------
robots_path = os.path.join(OUTPUT_DIR, 'robots.txt')
robots_content = """User-agent: *
Allow: /
Disallow: /templates/
Disallow: /scripts/

Sitemap: https://moj-startup.eu/sitemap.xml
"""

with open(robots_path, 'w', encoding='utf-8') as f:
    f.write(robots_content)

print("Plik robots.txt został zaktualizowany.")
