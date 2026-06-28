import sys
import os

with open('scripts/generate_seo.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add make_related_guides_links and make_related_brands_links functions
new_funcs = '''
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
    return "\\n".join(links)

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
    return "\\n".join(links)
'''
if 'make_related_guides_links' not in content:
    content = content.replace('def make_related_dtc_links', new_funcs + '\ndef make_related_dtc_links')

# 2. Add injections for templates
content = content.replace('html = html.replace("{{ related_dtc_links }}", make_related_dtc_links(code, DTC_CODES.keys()))', 'html = html.replace("{{ related_dtc_links }}", make_related_dtc_links(code, DTC_CODES.keys()))\n    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))\n    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))')
content = content.replace('html = html.replace("{{ content }}", f"<p class=\'lead text-slate-300 text-base mb-6 font-medium\'>{data[\'intro\']}</p>" + content_html)', 'html = html.replace("{{ content }}", f"<p class=\'lead text-slate-300 text-base mb-6 font-medium\'>{data[\'intro\']}</p>" + content_html)\n    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys(), current=slug))\n    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))')
content = content.replace('html = html.replace("{{ content }}", f"<p class=\'lead text-slate-300 text-base mb-6 font-medium\'>{data[\'intro\']}</p>" + data[\'content\'])', 'html = html.replace("{{ content }}", f"<p class=\'lead text-slate-300 text-base mb-6 font-medium\'>{data[\'intro\']}</p>" + data[\'content\'])\n    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))\n    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))')
content = content.replace('html = html.replace("{{ content }}", data[\'content\'])', 'html = html.replace("{{ content }}", data[\'content\'])\n    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))\n    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys()))')
content = content.replace('html = html.replace("{{ content }}", data[\'text\'])', 'html = html.replace("{{ content }}", data[\'text\'])\n    html = html.replace("{{ related_guides_links }}", make_related_guides_links(SYMPTOMS.keys()))\n    html = html.replace("{{ related_brands_links }}", make_related_brands_links(BRANDS.keys(), current=slug))')

with open('scripts/generate_seo.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('generate_seo.py updated.')
