import sys
import os

with open('scripts/seo_meta_fix.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add make_website_schema and make_itemlist_schema functions
new_schemas = '''
def build_website_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Mój Mechanik",
        "url": "https://moj-startup.eu/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://moj-startup.eu/bledy-dtc.html?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    return f\'<script type="application/ld+json">\\n{json.dumps(schema, ensure_ascii=False, indent=2)}\\n</script>\'

def build_itemlist_schema(page_type):
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": []
    }
    if page_type == "dtc_hub":
        schema["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "url": "https://moj-startup.eu/bledy-dtc/p0420/"},
            {"@type": "ListItem", "position": 2, "url": "https://moj-startup.eu/bledy-dtc/p0171/"},
            {"@type": "ListItem", "position": 3, "url": "https://moj-startup.eu/bledy-dtc/p0300/"}
        ]
    elif page_type == "guide_hub":
        schema["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "url": "https://moj-startup.eu/poradnik/auto-szarpie/"},
            {"@type": "ListItem", "position": 2, "url": "https://moj-startup.eu/poradnik/auto-nie-ma-mocy/"}
        ]
    return f\'<script type="application/ld+json">\\n{json.dumps(schema, ensure_ascii=False, indent=2)}\\n</script>\'
'''

if 'build_website_schema' not in content:
    content = content.replace('def build_complete_head_block', new_schemas + '\ndef build_complete_head_block')

# Inject into head block
injection = '''    # WebSite schema on homepage
    if meta.get("is_homepage"):
        schemas.append(build_website_schema())

    # ItemList schema on hubs
    if meta.get("page_type") == "website" and "dtc" in url:
        schemas.append(build_itemlist_schema("dtc_hub"))
    elif meta.get("page_type") == "hub":
        schemas.append(build_itemlist_schema("guide_hub"))
'''
if '# WebSite schema on homepage' not in content:
    content = content.replace('    # Organization schema on homepage only', injection + '\n    # Organization schema on homepage only')

with open('scripts/seo_meta_fix.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('seo_meta_fix.py updated.')
