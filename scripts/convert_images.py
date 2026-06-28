import os
from PIL import Image

def convert_to_webp(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    if not os.path.exists(source_dir):
        print(f"Błąd: Katalog {source_dir} nie istnieje.")
        return

    count = 0
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(source_dir, filename)
            base_name = os.path.splitext(filename)[0]
            
            # Clean filename
            safe_name = base_name.replace(' ', '_').lower()
            dest_filename = f"{safe_name}.webp"
            dest_path = os.path.join(dest_dir, dest_filename)
            
            try:
                with Image.open(src_path) as img:
                    img.save(dest_path, 'webp', quality=85)
                    print(f"Skonwertowano: {filename} -> {dest_filename}")
                    count += 1
            except Exception as e:
                print(f"Błąd przy konwersji {filename}: {e}")

    print(f"Zakończono. Skonwertowano {count} obrazów do WebP.")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(BASE_DIR, "screny ze sklepu")
    dest_dir = os.path.join(BASE_DIR, "assets", "screny")
    
    convert_to_webp(source_dir, dest_dir)
