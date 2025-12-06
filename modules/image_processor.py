"""Image Processor - Bildverarbeitung & Optimierung"""
from core.key_check import require_keys

@require_keys
def run():
    """Verarbeitet und optimiert Bilder"""
    images = ["image1.jpg", "image2.png", "image3.jpg"]
    processed = process_images(images)
    
    print(f"✅ {processed} Bilder verarbeitet")
    return {"status": "success", "processed": processed}

def process_images(images):
    """Verarbeitet Bilder"""
    processed = 0
    for img in images:
        if validate_image(img):
            optimize_image(img)
            processed += 1
    return processed

def validate_image(filename):
    """Validiert Bilddatei"""
    valid_formats = [".jpg", ".png", ".gif", ".webp"]
    return any(filename.lower().endswith(fmt) for fmt in valid_formats)

def optimize_image(filename):
    """Optimiert Bild"""
    return {"file": filename, "optimized": True, "size_reduction": "30%"}

def install():
    """Installiert das Modul"""
    print("📦 Image Processor installiert")
