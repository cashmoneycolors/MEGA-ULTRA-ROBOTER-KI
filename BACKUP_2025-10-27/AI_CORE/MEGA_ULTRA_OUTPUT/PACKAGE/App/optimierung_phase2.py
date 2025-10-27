#!/usr/bin/env python3
"""
🚀 MEGA ULTRA SYSTEM - OPTIMIERUNG PHASE 2  
ERWEITERTE KI FEATURES + FARBTHEORIE + TYPOGRAPHY AI
"""

import colorsys
import math
import json
from datetime import datetime
import random

class MegaUltraColorTheoryAI:
    """Intelligente Farbtheorie mit KI-Algorithmen"""
    
    def __init__(self):
        self.version = "COLOR_AI_2025"
        
        # Farbtheorie-Regeln
        self.color_harmonies = {
            'complementary': {'angle': 180, 'colors': 2},
            'triadic': {'angle': 120, 'colors': 3},
            'tetradic': {'angle': 90, 'colors': 4},
            'analogous': {'angle': 30, 'colors': 3},
            'split_complementary': {'angle': 150, 'colors': 3},
            'monochromatic': {'angle': 0, 'colors': 5}
        }
        
        # Psychologie der Farben
        self.color_psychology = {
            'tech': {'primary': '#2196F3', 'emotions': ['trust', 'innovation', 'stability']},
            'nature': {'primary': '#4CAF50', 'emotions': ['growth', 'harmony', 'fresh']},
            'energy': {'primary': '#FF5722', 'emotions': ['passion', 'action', 'power']},
            'luxury': {'primary': '#9C27B0', 'emotions': ['elegance', 'premium', 'mystery']},
            'health': {'primary': '#00BCD4', 'emotions': ['clean', 'medical', 'trust']},
            'finance': {'primary': '#1976D2', 'emotions': ['security', 'professional', 'stability']}
        }
        
        print("🎨 MEGA ULTRA COLOR THEORY AI INITIALIZED")
        
    def analyze_brand_colors(self, brand_type, mood='professional'):
        """KI-basierte Farbanalyse für Marken"""
        
        base_colors = self.color_psychology.get(brand_type, self.color_psychology['tech'])
        primary_color = base_colors['primary']
        
        # Konvertiere zu HSV für bessere Kontrolle
        primary_hsv = self.hex_to_hsv(primary_color)
        
        # Generiere harmonische Farbpalette
        harmony_type = self.select_optimal_harmony(brand_type, mood)
        color_palette = self.generate_harmony_palette(primary_hsv, harmony_type)
        
        # KI-Optimierung basierend auf Kontrast und Lesbarkeit
        optimized_palette = self.optimize_for_accessibility(color_palette)
        
        analysis = {
            'brand_type': brand_type,
            'mood': mood,
            'primary_color': primary_color,
            'harmony_type': harmony_type,
            'palette': optimized_palette,
            'emotions': base_colors['emotions'],
            'accessibility_score': self.calculate_accessibility_score(optimized_palette),
            'use_cases': self.suggest_use_cases(optimized_palette)
        }
        
        print(f"🎯 Color Analysis: {brand_type} -> {harmony_type} harmony")
        print(f"🌈 Generated {len(optimized_palette)} colors")
        
        return analysis
    
    def select_optimal_harmony(self, brand_type, mood):
        """KI-Auswahl der optimalen Farbharmonie"""
        
        # Intelligente Auswahl basierend auf Markentyp
        harmony_rules = {
            'tech': ['complementary', 'triadic'],
            'nature': ['analogous', 'monochromatic'],
            'energy': ['complementary', 'split_complementary'],
            'luxury': ['monochromatic', 'tetradic'],
            'health': ['analogous', 'complementary'],
            'finance': ['complementary', 'monochromatic']
        }
        
        mood_modifiers = {
            'professional': ['monochromatic', 'complementary'],
            'creative': ['triadic', 'tetradic'],
            'energetic': ['complementary', 'split_complementary'],
            'calm': ['analogous', 'monochromatic']
        }
        
        brand_options = harmony_rules.get(brand_type, ['complementary'])
        mood_options = mood_modifiers.get(mood, ['complementary'])
        
        # Finde Überschneidung oder wähle beste Option
        intersection = list(set(brand_options) & set(mood_options))
        
        if intersection:
            return intersection[0]
        else:
            return brand_options[0]
    
    def generate_harmony_palette(self, primary_hsv, harmony_type):
        """Generiere harmonische Farbpalette"""
        
        h, s, v = primary_hsv
        harmony = self.color_harmonies[harmony_type]
        colors = []
        
        # Hauptfarbe
        colors.append(self.hsv_to_hex(h, s, v))
        
        if harmony_type == 'complementary':
            comp_h = (h + 180) % 360
            colors.append(self.hsv_to_hex(comp_h, s, v))
            
        elif harmony_type == 'triadic':
            for i in [120, 240]:
                new_h = (h + i) % 360
                colors.append(self.hsv_to_hex(new_h, s, v))
                
        elif harmony_type == 'tetradic':
            for i in [90, 180, 270]:
                new_h = (h + i) % 360
                colors.append(self.hsv_to_hex(new_h, s, v))
                
        elif harmony_type == 'analogous':
            for i in [-30, 30]:
                new_h = (h + i) % 360
                colors.append(self.hsv_to_hex(new_h, s, v))
                
        elif harmony_type == 'monochromatic':
            # Variiere Sättigung und Helligkeit
            variations = [
                (h, s * 0.3, v * 1.2),  # Hell
                (h, s * 0.7, v * 0.9),  # Medium
                (h, s * 1.0, v * 0.7),  # Dunkel
                (h, s * 0.5, v * 0.5)   # Sehr dunkel
            ]
            
            for var_h, var_s, var_v in variations:
                # Begrenze Werte
                var_s = min(1.0, max(0.0, var_s))
                var_v = min(1.0, max(0.0, var_v))
                colors.append(self.hsv_to_hex(var_h, var_s, var_v))
        
        return colors[:harmony['colors']]
    
    def optimize_for_accessibility(self, colors):
        """Optimiere Farbpalette für Barrierefreiheit"""
        
        optimized = []
        
        for color in colors:
            # Konvertiere zu RGB für Kontrastberechnung
            rgb = self.hex_to_rgb(color)
            
            # Berechne Luminanz
            luminance = self.calculate_luminance(rgb)
            
            # Optimiere für besseren Kontrast
            if luminance < 0.2:  # Zu dunkel
                # Erhöhe Helligkeit
                hsv = self.hex_to_hsv(color)
                h, s, v = hsv
                v = min(1.0, v + 0.2)
                color = self.hsv_to_hex(h, s, v)
            elif luminance > 0.8:  # Zu hell
                # Reduziere Helligkeit
                hsv = self.hex_to_hsv(color)
                h, s, v = hsv
                v = max(0.2, v - 0.2)
                color = self.hsv_to_hex(h, s, v)
            
            optimized.append(color)
        
        return optimized
    
    def calculate_accessibility_score(self, colors):
        """Berechne Barrierefreiheits-Score"""
        
        if len(colors) < 2:
            return 0.5
        
        total_contrast = 0
        comparisons = 0
        
        for i, color1 in enumerate(colors):
            for color2 in colors[i+1:]:
                contrast = self.calculate_contrast_ratio(color1, color2)
                total_contrast += contrast
                comparisons += 1
        
        avg_contrast = total_contrast / comparisons if comparisons > 0 else 0
        
        # Normalisiere auf 0-1 Skala
        score = min(1.0, avg_contrast / 7.0)  # 7:1 ist AAA Standard
        
        return score
    
    def suggest_use_cases(self, colors):
        """Schlage Verwendungszwecke für Farben vor"""
        
        if len(colors) == 0:
            return {}
        
        use_cases = {
            'primary': colors[0],  # Hauptfarbe
            'background': '#FFFFFF',  # Standard weiß
            'text': '#000000'  # Standard schwarz
        }
        
        if len(colors) >= 2:
            use_cases['accent'] = colors[1]
            
        if len(colors) >= 3:
            use_cases['secondary'] = colors[2]
            
        if len(colors) >= 4:
            use_cases['border'] = colors[3]
        
        # Optimiere Text-/Hintergrundfarben für Kontrast
        for bg_color in colors:
            white_contrast = self.calculate_contrast_ratio(bg_color, '#FFFFFF')
            black_contrast = self.calculate_contrast_ratio(bg_color, '#000000')
            
            if white_contrast > black_contrast:
                use_cases[f'text_on_{bg_color}'] = '#FFFFFF'
            else:
                use_cases[f'text_on_{bg_color}'] = '#000000'
        
        return use_cases
    
    def hex_to_rgb(self, hex_color):
        """Konvertiere Hex zu RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def hex_to_hsv(self, hex_color):
        """Konvertiere Hex zu HSV"""
        rgb = self.hex_to_rgb(hex_color)
        r, g, b = [x/255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h * 360, s, v)
    
    def hsv_to_hex(self, h, s, v):
        """Konvertiere HSV zu Hex"""
        r, g, b = colorsys.hsv_to_rgb(h/360.0, s, v)
        r, g, b = int(r*255), int(g*255), int(b*255)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def calculate_luminance(self, rgb):
        """Berechne relative Luminanz"""
        r, g, b = [x/255.0 for x in rgb]
        
        # sRGB zu lineare RGB Konversion
        def linearize(c):
            if c <= 0.03928:
                return c / 12.92
            else:
                return pow((c + 0.055) / 1.055, 2.4)
        
        r_lin = linearize(r)
        g_lin = linearize(g)
        b_lin = linearize(b)
        
        # ITU-R BT.709 Gewichtung
        return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
    
    def calculate_contrast_ratio(self, color1, color2):
        """Berechne Kontrastverhältnis zwischen zwei Farben"""
        
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        lum1 = self.calculate_luminance(rgb1)
        lum2 = self.calculate_luminance(rgb2)
        
        # Hellere Farbe zuerst
        if lum1 < lum2:
            lum1, lum2 = lum2, lum1
        
        return (lum1 + 0.05) / (lum2 + 0.05)

class MegaUltraTypographyAI:
    """KI-gesteuerte Typography-Optimierung"""
    
    def __init__(self):
        self.version = "TYPOGRAPHY_AI_2025"
        
        # Font-Klassifikationen
        self.font_categories = {
            'serif': {
                'fonts': ['Times New Roman', 'Georgia', 'Book Antiqua'],
                'personality': ['traditional', 'authoritative', 'elegant'],
                'use_cases': ['print', 'long_text', 'formal']
            },
            'sans_serif': {
                'fonts': ['Arial', 'Helvetica', 'Calibri', 'Segoe UI'],
                'personality': ['modern', 'clean', 'friendly'],
                'use_cases': ['digital', 'ui', 'headings']
            },
            'display': {
                'fonts': ['Impact', 'Arial Black', 'Trebuchet MS'],
                'personality': ['bold', 'attention_grabbing', 'powerful'],
                'use_cases': ['headlines', 'logos', 'posters']
            },
            'script': {
                'fonts': ['Brush Script MT', 'Lucida Handwriting'],
                'personality': ['elegant', 'personal', 'artistic'],
                'use_cases': ['invitations', 'luxury', 'personal_branding']
            }
        }
        
        # Typographische Regeln
        self.typography_rules = {
            'golden_ratio': 1.618,
            'scale_ratios': [1.125, 1.2, 1.25, 1.333, 1.414, 1.5, 1.618],
            'line_height_ratios': [1.2, 1.4, 1.5, 1.6],
            'optimal_line_length': {'min': 45, 'max': 75, 'optimal': 66}  # Zeichen
        }
        
        print("📝 MEGA ULTRA TYPOGRAPHY AI INITIALIZED")
    
    def analyze_typography_needs(self, content_type, brand_personality, target_audience):
        """KI-Analyse der Typography-Anforderungen"""
        
        # Analysiere Content-Typ
        type_requirements = {
            'logo': {'hierarchy': 1, 'readability': 'high', 'personality': 'strong'},
            'headline': {'hierarchy': 1, 'readability': 'high', 'personality': 'attention'},
            'body_text': {'hierarchy': 3, 'readability': 'maximum', 'personality': 'neutral'},
            'button': {'hierarchy': 2, 'readability': 'high', 'personality': 'action'},
            'caption': {'hierarchy': 4, 'readability': 'good', 'personality': 'subtle'}
        }
        
        requirements = type_requirements.get(content_type, type_requirements['body_text'])
        
        # Wähle optimale Font-Kategorie
        font_category = self.select_optimal_font_category(brand_personality, content_type)
        
        # Berechne optimale Größenverhältnisse
        size_system = self.calculate_size_system(requirements['hierarchy'])
        
        # Generiere Typography-System
        typography_system = {
            'content_type': content_type,
            'font_category': font_category,
            'recommended_fonts': self.font_categories[font_category]['fonts'],
            'size_system': size_system,
            'line_height': self.calculate_optimal_line_height(size_system['base_size']),
            'letter_spacing': self.calculate_letter_spacing(font_category, size_system['base_size']),
            'color_contrast': self.suggest_text_colors(),
            'accessibility_score': self.calculate_typography_accessibility(size_system, font_category)
        }
        
        print(f"📝 Typography Analysis: {content_type} -> {font_category}")
        print(f"🎯 Base size: {size_system['base_size']}px")
        
        return typography_system
    
    def select_optimal_font_category(self, brand_personality, content_type):
        """Wähle optimale Font-Kategorie basierend auf KI-Analyse"""
        
        personality_mapping = {
            'modern': 'sans_serif',
            'traditional': 'serif',
            'elegant': 'serif',
            'bold': 'display',
            'friendly': 'sans_serif',
            'authoritative': 'serif',
            'creative': 'display',
            'luxury': 'script',
            'tech': 'sans_serif',
            'corporate': 'sans_serif'
        }
        
        content_preferences = {
            'logo': ['display', 'sans_serif'],
            'headline': ['display', 'sans_serif'],
            'body_text': ['serif', 'sans_serif'],
            'button': ['sans_serif', 'display']
        }
        
        # Primäre Auswahl basierend auf Persönlichkeit
        primary_choice = personality_mapping.get(brand_personality, 'sans_serif')
        
        # Validiere gegen Content-Typ Präferenzen
        content_prefs = content_preferences.get(content_type, ['sans_serif'])
        
        if primary_choice in content_prefs:
            return primary_choice
        else:
            return content_prefs[0]
    
    def calculate_size_system(self, hierarchy_level):
        """Berechne harmonisches Größensystem"""
        
        # Basis-Größen nach Hierarchy
        base_sizes = {
            1: 48,  # Headlines, Logos
            2: 24,  # Subheadings, Buttons
            3: 16,  # Body Text
            4: 12   # Captions, Small Text
        }
        
        base_size = base_sizes.get(hierarchy_level, 16)
        
        # Verwende Golden Ratio für Größenverhältnisse
        golden_ratio = self.typography_rules['golden_ratio']
        
        size_system = {
            'base_size': base_size,
            'large': int(base_size * golden_ratio),
            'medium': base_size,
            'small': int(base_size / golden_ratio),
            'tiny': int(base_size / (golden_ratio ** 2))
        }
        
        return size_system
    
    def calculate_optimal_line_height(self, font_size):
        """Berechne optimale Zeilenhöhe"""
        
        # Basis-Regel: 1.4-1.6 für Fließtext, 1.2-1.3 für Headlines
        if font_size >= 24:  # Headlines
            base_ratio = 1.25
        else:  # Body text
            base_ratio = 1.5
        
        # Anpassung basierend auf Schriftgröße
        if font_size < 12:
            base_ratio += 0.1  # Kleinere Schrift braucht mehr Zeilenabstand
        elif font_size > 48:
            base_ratio -= 0.1  # Größere Schrift braucht weniger
        
        return round(font_size * base_ratio, 1)
    
    def calculate_letter_spacing(self, font_category, font_size):
        """Berechne optimalen Buchstabenabstand"""
        
        # Basis-Werte nach Kategorie
        base_spacing = {
            'serif': 0,
            'sans_serif': 0.01,
            'display': 0.02,
            'script': 0
        }
        
        spacing = base_spacing.get(font_category, 0)
        
        # Anpassung für große Schriften
        if font_size > 24:
            spacing += 0.02
        elif font_size < 12:
            spacing += 0.01
        
        return round(font_size * spacing, 2)
    
    def suggest_text_colors(self):
        """Schlage optimale Textfarben vor"""
        
        return {
            'primary_text': '#212121',    # Dunkelgrau statt Schwarz
            'secondary_text': '#757575',  # Mittleres Grau
            'disabled_text': '#BDBDBD',   # Helles Grau
            'inverse_text': '#FFFFFF',    # Weiß für dunkle Hintergründe
            'link_text': '#1976D2',       # Blaue Links
            'error_text': '#D32F2F'       # Rot für Fehler
        }
    
    def calculate_typography_accessibility(self, size_system, font_category):
        """Berechne Typography Barrierefreiheits-Score"""
        
        score = 0.0
        
        # Größen-Score (WCAG Mindestgröße: 16px)
        if size_system['base_size'] >= 16:
            score += 0.3
        elif size_system['base_size'] >= 14:
            score += 0.2
        else:
            score += 0.1
        
        # Font-Kategorie Score (Sans-Serif meist besser lesbar)
        category_scores = {
            'sans_serif': 0.3,
            'serif': 0.25,
            'display': 0.2,
            'script': 0.1
        }
        score += category_scores.get(font_category, 0.15)
        
        # Kontrast-Score (vereinfacht)
        score += 0.4  # Annahme: guter Kontrast
        
        return min(1.0, score)

def test_ki_optimierungen():
    """Test der KI-Optimierungen"""
    
    print("🧪 TESTING KI OPTIMIZATIONS...")
    
    # Test Color Theory AI
    color_ai = MegaUltraColorTheoryAI()
    
    brand_types = ['tech', 'luxury', 'nature']
    for brand in brand_types:
        analysis = color_ai.analyze_brand_colors(brand, 'professional')
        print(f"🎨 {brand}: {len(analysis['palette'])} colors, Score: {analysis['accessibility_score']:.2f}")
    
    # Test Typography AI  
    typography_ai = MegaUltraTypographyAI()
    
    content_types = ['logo', 'headline', 'body_text']
    for content in content_types:
        typo = typography_ai.analyze_typography_needs(content, 'modern', 'professional')
        print(f"📝 {content}: {typo['font_category']}, Size: {typo['size_system']['base_size']}px")
    
    print("✅ KI OPTIMIZATION TESTS COMPLETED")

if __name__ == "__main__":
    test_ki_optimierungen()