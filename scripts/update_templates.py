import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_DIR = os.path.join(BASE_DIR, "templates")

# Universal CTA Snippet
CTA_SNIPPET = """
<div class="my-8 p-6 bg-slate-800 rounded-xl border border-slate-700 flex flex-col md:flex-row items-center gap-6 justify-between">
    <div>
        <h3 class="text-xl font-bold text-white mb-2">Pobierz aplikację Mój Mechanik</h3>
        <p class="text-slate-300">Sprawdź VIN, odczytaj błędy OBD2 i skorzystaj z diagnozy AI. Zobacz dlaczego kierowcy wybierają nasz skaner.</p>
    </div>
    <a href="https://play.google.com/store/apps/details?id=com.lukasz.mojmechanik&hl=pl&gl=PL&utm_source=website&utm_medium=cta" target="_blank" rel="noopener" class="flex-shrink-0 bg-brandRed hover:bg-brandRedHover text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-brandRed/30 transition-all flex items-center gap-2">
        <i class="fa-brands fa-google-play"></i> Pobierz z Google Play
    </a>
</div>
"""

# App Rating / Screenshot / Hero Block (Above the fold without fake stats)
HERO_CTA_SNIPPET = """
        <!-- App Download CTA -->
        <div class="mt-8">
            <a href="https://play.google.com/store/apps/details?id=com.lukasz.mojmechanik&hl=pl&gl=PL&utm_source=website&utm_medium=hero" target="_blank" rel="noopener" class="inline-flex items-center gap-3 bg-brandRed hover:bg-brandRedHover text-white px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-lg hover:shadow-brandRed/30">
                <i class="fa-brands fa-google-play text-2xl"></i>
                Pobierz z Google Play
            </a>
            <p class="mt-3 text-sm text-slate-400"><i class="fa-solid fa-star text-accentYellow"></i> Oficjalna aplikacja diagnostyczna Android</p>
        </div>
"""

def update_dtc():
    path = os.path.join(TPL_DIR, "dtc.html")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace artificial mockups and stats with real screenshot
    content = re.sub(
        r'<div class="relative w-64 h-\[500px\] bg-slate-900 rounded-3xl border-4 border-slate-800 shadow-2xl overflow-hidden">.*?</div>\s*</div>',
        '<img src="/assets/screny/01_diagnostyka_auta_telefon_1080x1920.webp" alt="Diagnoza usterki Mój Mechanik" class="rounded-3xl shadow-2xl border-4 border-slate-800 w-full max-w-[280px] mx-auto md:ml-auto">',
        content,
        flags=re.DOTALL
    )

    # Replace hero fake stats (e.g. 4.8/5) with the clean CTA
    content = re.sub(
        r'<div class="flex flex-col sm:flex-row gap-4 mt-8">.*?<div class="flex items-center gap-2 text-slate-400 text-sm mt-4">.*?</div>',
        HERO_CTA_SNIPPET,
        content,
        flags=re.DOTALL
    )

    # 2. Add TOC, Symptomy, Przyczyny, Koszty, Czy można jechać
    # Let's completely replace the main <article> structure to ensure all required fields exist
    new_article = f"""
        <article class="prose prose-invert prose-lg max-w-none">
            {CTA_SNIPPET}
            
            <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 mb-8">
                <h2 class="text-xl font-bold mt-0 mb-4 border-b border-slate-700 pb-2">Spis treści</h2>
                <ul class="list-none pl-0 space-y-2 m-0 text-base">
                    <li><a href="#co-oznacza" class="text-brandRed hover:underline">1. Co oznacza błąd {{{{ code }}}}?</a></li>
                    <li><a href="#objawy" class="text-brandRed hover:underline">2. Główne objawy</a></li>
                    <li><a href="#przyczyny" class="text-brandRed hover:underline">3. Możliwe przyczyny</a></li>
                    <li><a href="#czy-mozna-jechac" class="text-brandRed hover:underline">4. Czy można jechać dalej?</a></li>
                    <li><a href="#koszty" class="text-brandRed hover:underline">5. Szacunkowe koszty naprawy</a></li>
                </ul>
            </div>

            <h2 id="co-oznacza">Co oznacza błąd {{{{ code }}}}?</h2>
            <p>Kod błędu <strong>{{{{ code }}}}</strong> ({{{{ name_pl }}}}) to błąd powiązany z sekcją <em>{{{{ system_name }}}}</em>. Oznacza to, że: {{{{ short_definition }}}}</p>
            <p>Najczęstszą przyczyną zgłoszenia tego błędu przez komputer (ECU) jest: <strong>{{{{ primary_cause }}}}</strong>.</p>
            
            {CTA_SNIPPET.replace("cta", "cta_mid1")}

            <h2 id="objawy">Jakie są objawy usterki?</h2>
            <p>Zapaleniu się kontrolki silnika w przypadku błędu {{{{ code }}}} najczęściej towarzyszą następujące symptomy:</p>
            <ul class="space-y-2">
                {{{{ symptoms_list }}}}
            </ul>

            <h2 id="przyczyny">Najczęstsze przyczyny błędu {{{{ code }}}}</h2>
            <p>Aby trwale rozwiązać problem, mechanik lub aplikacja diagnostyczna powinna zwrócić uwagę na:</p>
            <ul class="space-y-2">
                {{{{ causes_list }}}}
            </ul>

            <h2 id="czy-mozna-jechac">Czy można jechać z błędem {{{{ code }}}}?</h2>
            <div class="flex items-start gap-4 p-5 rounded-lg border border-slate-700 bg-slate-800/50 mt-4">
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 text-2xl {{{{ severity_color }}}} border {{{{ severity_border }}}} shadow-lg {{{{ severity_glow }}}}">
                    <i class="fa-solid {{{{ severity_icon }}}}"></i>
                </div>
                <div>
                    <h3 class="text-xl font-bold mb-1 mt-0">{{{{ severity_title }}}}</h3>
                    <p class="m-0 text-slate-300">{{{{ severity_desc }}}}</p>
                </div>
            </div>

            {CTA_SNIPPET.replace("cta", "cta_mid2")}

            <h2 id="koszty">Szacunkowe koszty naprawy (2026)</h2>
            <div class="overflow-x-auto my-6">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-800 border-b border-slate-700">
                            <th class="p-4 font-bold text-slate-200">Element do sprawdzenia / wymiany</th>
                            <th class="p-4 font-bold text-slate-200 w-48">Szacunkowy koszt</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {{{{ repair_cost_table_rows }}}}
                    </tbody>
                </table>
                <p class="text-sm text-slate-400 mt-2 italic">* Podane ceny są orientacyjne i zawierają koszt robocizny w niezależnym warsztacie.</p>
            </div>
            
            <h2 id="powiazane">Powiązane błędy DTC</h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 not-prose">
                {{{{ related_dtc_links }}}}
            </div>
            
            <div class="mt-12">
                <h2 class="text-2xl font-bold mb-4">Powiązane marki i poradniki</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 not-prose">
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <h3 class="font-bold text-white mb-2">Poradniki</h3>
                        <ul class="space-y-1 text-slate-300">
                            {{{{ related_guides_links }}}}
                        </ul>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <h3 class="font-bold text-white mb-2">Marki</h3>
                        <div class="flex flex-wrap gap-2">
                            {{{{ related_brands_links }}}}
                        </div>
                    </div>
                </div>
            </div>

        </article>
"""
    # Replace old article content
    content = re.sub(r'<article.*?</article>', new_article, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_other_templates():
    templates = ['guide.html', 'diagnostics.html', 'brand.html', 'comparison.html']
    
    for tpl in templates:
        path = os.path.join(TPL_DIR, tpl)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace mockup images with real ones
        if tpl == 'guide.html':
            img_src = "/assets/screny/02_ai_mechanik_telefon_1080x1920.webp"
        elif tpl == 'diagnostics.html':
            img_src = "/assets/screny/07_raport_pdf_telefon_1080x1920.webp"
        elif tpl == 'brand.html':
            img_src = "/assets/screny/04_dekoder_vin_telefon_1080x1920.webp"
        else:
            img_src = "/assets/screny/05_ocena_oferty_telefon_1080x1920.webp"

        content = re.sub(
            r'<div class="relative w-64 h-\[500px\].*?</div>\s*</div>',
            f'<img src="{img_src}" alt="Mój Mechanik Aplikacja" class="rounded-3xl shadow-2xl border-4 border-slate-800 w-full max-w-[280px] mx-auto md:ml-auto">',
            content,
            flags=re.DOTALL
        )

        content = re.sub(
            r'<img src="https://moj-startup.eu/assets/screen-ai-report.webp".*?>',
            f'<img src="{img_src}" alt="Mój Mechanik Aplikacja" class="rounded-3xl shadow-2xl border-4 border-slate-800 w-full max-w-[280px] mx-auto md:ml-auto">',
            content,
            flags=re.DOTALL
        )

        content = re.sub(
            r'<div class="flex flex-col sm:flex-row gap-4 mt-8">.*?<div class="flex items-center gap-2 text-slate-400 text-sm mt-4">.*?</div>',
            HERO_CTA_SNIPPET,
            content,
            flags=re.DOTALL
        )
        
        # Inject Related links block right before </article>
        related_block = f"""
            {CTA_SNIPPET.replace('cta', 'cta_bottom')}
            <div class="mt-12 not-prose">
                <h2 class="text-2xl font-bold mb-4 text-white">Sprawdź również</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <h3 class="font-bold text-white mb-2">Powiązane Poradniki</h3>
                        <ul class="space-y-1 text-slate-300">
                            {{{{ related_guides_links }}}}
                        </ul>
                    </div>
                    <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
                        <h3 class="font-bold text-white mb-2">Diagnostyka Marek</h3>
                        <div class="flex flex-wrap gap-2">
                            {{{{ related_brands_links }}}}
                        </div>
                    </div>
                </div>
            </div>
"""
        content = content.replace("</article>", related_block + "\n</article>")
        
        # Guide TOC
        if 'guide.html' in tpl or 'diagnostics.html' in tpl:
            # We already have table_of_contents variable in guide.html, make sure it's wrapped properly
            pass

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    update_dtc()
    update_other_templates()
    print("Szablony zaktualizowane.")
