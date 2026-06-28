import os
import re

templates = [
    ('templates/guide.html', 'assets/screny/02_ai_mechanik_telefon_1080x1920.webp', 'Aplikacja Moj Mechanik - diagnoza AI usterki auta'),
    ('templates/diagnostics.html', 'assets/screny/07_raport_pdf_telefon_1080x1920.webp', 'Aplikacja Moj Mechanik - raport PDF i diagnostyka OBD2'),
    ('templates/brand.html', 'assets/screny/04_dekoder_vin_telefon_1080x1920.webp', 'Aplikacja Moj Mechanik - dekoder VIN i historia pojazdu'),
    ('templates/comparison.html', 'assets/screny/05_ocena_oferty_telefon_1080x1920.webp', 'Aplikacja Moj Mechanik - ocena oferty zakupu auta'),
]

for tpl, img, alt in templates:
    with open(tpl, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove pb-24 md:pb-0 from body (mobile padding fix)
    content = content.replace('min-h-screen pb-24 md:pb-0', 'min-h-screen')

    # Remove fake stars and rating block below button in sidebar
    content = re.sub(
        r'<!-- Reviews rating under button -->.*?</div>\s*</div>',
        '<p class="text-center text-xs text-slate-500 mt-3">Bezplatna aplikacja na Android</p>\n                </div>',
        content, flags=re.DOTALL
    )

    # Remove fake stars in sticky mobile banner
    content = re.sub(
        r'<div class="flex text-amber-400 text-\[8px\] mt-0\.5">.*?</div>',
        '',
        content, flags=re.DOTALL
    )

    # Replace existing screenshot images with correct WebP files
    content = re.sub(
        r'<img\s[^>]*src="/assets/screny/[^"]+\"[^>]*>',
        f'<img src="/{img}" alt="{alt}" class="w-48 sm:w-56 md:w-64 lg:w-72 rounded-3xl shadow-2xl border-4 border-slate-800 object-cover" loading="lazy" width="400" height="800">',
        content
    )

    with open(tpl, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated: {tpl}')

print('All templates patched.')
