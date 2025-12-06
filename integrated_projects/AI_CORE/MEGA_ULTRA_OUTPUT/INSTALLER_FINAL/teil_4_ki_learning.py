#!/usr/bin/env python3
"""
🚀 MEGA ULTRA SYSTEM - TEIL 4: KI LEARNING SYSTEM
Echtes maschinelles Lernen für kontinuierliche Verbesserung
"""

import sqlite3
import json
import numpy as np
from datetime import datetime, timedelta
import re
import hashlib

class MegaUltraKILearning:
    """Ultra Intelligence Learning System"""
    
    def __init__(self, db_path="MEGA_ULTRA_SYSTEM/mega_ultra.db"):
        self.version = "KI_LEARNING_2025"
        self.db_path = db_path
        self.learning_rate = 0.1
        
        # Command Pattern Analysis
        self.command_patterns = {
            'logo': ['logo', 'brand', 'marke', 'emblem', 'symbol'],
            'banner': ['banner', 'werbung', 'anzeige', 'header', 'promo'],
            'icon': ['icon', 'app', 'symbol', 'button'],
            'poster': ['poster', 'plakat', 'flyer', 'event'],
            'business_card': ['visitenkarte', 'business card', 'karte'],
            'color_palette': ['farbe', 'color', 'palette', 'farbschema']
        }
        
        # Quality Metrics
        self.quality_factors = {
            'resolution': 0.25,
            'color_harmony': 0.20,
            'typography': 0.20,
            'composition': 0.15,
            'brand_consistency': 0.20
        }
        
        self.init_learning_database()
        print("🧠 MEGA ULTRA KI LEARNING SYSTEM INITIALIZED")
        
    def init_learning_database(self):
        """Initialize learning database with advanced tables"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Command Analysis Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS command_analysis (
                id INTEGER PRIMARY KEY,
                command_hash TEXT UNIQUE,
                original_command TEXT,
                detected_type TEXT,
                confidence_score REAL,
                keywords JSON,
                success_rate REAL,
                avg_quality REAL,
                usage_count INTEGER DEFAULT 1,
                last_used DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Learning Feedback Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS learning_feedback (
                id INTEGER PRIMARY KEY,
                generation_id INTEGER,
                command_hash TEXT,
                user_satisfaction INTEGER,
                quality_metrics JSON,
                improvement_suggestions JSON,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Pattern Evolution Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pattern_evolution (
                id INTEGER PRIMARY KEY,
                pattern_type TEXT,
                old_weights JSON,
                new_weights JSON,
                improvement_factor REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def analyze_command(self, command):
        """Advanced command analysis with learning"""
        
        command_lower = command.lower()
        command_hash = hashlib.md5(command.encode()).hexdigest()
        
        # Check if we've seen this command before
        previous_analysis = self.get_previous_analysis(command_hash)
        
        if previous_analysis:
            # Update usage count and return enhanced analysis
            return self.update_command_usage(command_hash, command)
        
        # New command - perform full analysis
        analysis = {
            'command_hash': command_hash,
            'original_command': command,
            'detected_type': self.detect_command_type(command_lower),
            'confidence_score': 0.0,
            'keywords': self.extract_keywords(command_lower),
            'complexity_level': self.assess_complexity(command),
            'suggested_settings': {}
        }
        
        # Calculate confidence based on keyword matches
        analysis['confidence_score'] = self.calculate_confidence(analysis)
        
        # Generate optimal settings based on learning
        analysis['suggested_settings'] = self.generate_optimal_settings(analysis)
        
        # Store analysis for future learning
        self.store_command_analysis(analysis)
        
        print(f"🧠 COMMAND ANALYZED: {analysis['detected_type']} (Confidence: {analysis['confidence_score']:.2f})")
        
        return analysis
    
    def detect_command_type(self, command_lower):
        """Detect command type using pattern matching"""
        
        type_scores = {}
        
        for cmd_type, keywords in self.command_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in command_lower:
                    score += 1
                    # Bonus for exact matches
                    if keyword == command_lower.strip():
                        score += 2
            
            if score > 0:
                type_scores[cmd_type] = score
        
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return 'generic'
    
    def extract_keywords(self, command_lower):
        """Extract relevant keywords for learning"""
        
        # Remove common words
        stop_words = ['ein', 'eine', 'der', 'die', 'das', 'für', 'mit', 'und', 'oder']
        
        # Split and clean
        words = re.findall(r'\b\w+\b', command_lower)
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def assess_complexity(self, command):
        """Assess command complexity for resource allocation"""
        
        complexity_indicators = {
            'simple': ['logo', 'icon', 'einfach', 'basic'],
            'medium': ['banner', 'poster', 'professional', 'business'],
            'complex': ['3d', 'animation', '8k', 'ultra', 'premium', 'advanced']
        }
        
        command_lower = command.lower()
        scores = {'simple': 0, 'medium': 0, 'complex': 0}
        
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in command_lower:
                    scores[level] += 1
        
        return max(scores, key=scores.get) if any(scores.values()) else 'medium'
    
    def calculate_confidence(self, analysis):
        """Calculate confidence score based on various factors"""
        
        factors = {
            'keyword_matches': len(analysis['keywords']) * 0.15,
            'type_detection': 0.3 if analysis['detected_type'] != 'generic' else 0.1,
            'command_length': min(len(analysis['original_command']) * 0.01, 0.2),
            'complexity_clarity': 0.2 if analysis['complexity_level'] != 'medium' else 0.1
        }
        
        confidence = sum(factors.values())
        return min(confidence, 1.0)  # Cap at 1.0
    
    def generate_optimal_settings(self, analysis):
        """Generate optimal settings based on learning"""
        
        base_settings = {
            'logo': {
                'resolution': (2048, 2048),
                'format': 'SVG',
                'colors': 2,
                'typography': 'modern'
            },
            'banner': {
                'resolution': (1920, 1080),
                'format': 'PNG',
                'colors': 3,
                'typography': 'bold'
            },
            'icon': {
                'resolution': (512, 512),
                'format': 'PNG',
                'colors': 2,
                'typography': 'clean'
            }
        }
        
        cmd_type = analysis['detected_type']
        settings = base_settings.get(cmd_type, base_settings['logo'])
        
        # Enhance based on complexity
        if analysis['complexity_level'] == 'complex':
            settings['resolution'] = tuple(x * 2 for x in settings['resolution'])
            settings['anti_alias'] = True
            settings['premium_effects'] = True
        
        return settings
    
    def store_command_analysis(self, analysis):
        """Store analysis for future learning"""
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            conn.execute('''
                INSERT INTO command_analysis 
                (command_hash, original_command, detected_type, confidence_score, 
                 keywords, success_rate, avg_quality, last_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                analysis['command_hash'],
                analysis['original_command'],
                analysis['detected_type'],
                analysis['confidence_score'],
                json.dumps(analysis['keywords']),
                1.0,  # Initial success rate
                0.8,  # Initial quality estimate
                datetime.now().isoformat()
            ))
            
            conn.commit()
            
        except sqlite3.IntegrityError:
            # Command already exists, update it
            pass
        
        conn.close()
    
    def get_previous_analysis(self, command_hash):
        """Get previous analysis for learning enhancement"""
        
        conn = sqlite3.connect(self.db_path)
        
        cursor = conn.execute('''
            SELECT * FROM command_analysis WHERE command_hash = ?
        ''', (command_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def update_command_usage(self, command_hash, command):
        """Update usage statistics and return enhanced analysis"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Get current stats
        cursor = conn.execute('''
            SELECT detected_type, confidence_score, keywords, success_rate, avg_quality, usage_count
            FROM command_analysis WHERE command_hash = ?
        ''', (command_hash,))
        
        result = cursor.fetchone()
        
        if result:
            detected_type, confidence, keywords_json, success_rate, avg_quality, usage_count = result
            
            # Update usage count and timestamp
            conn.execute('''
                UPDATE command_analysis 
                SET usage_count = usage_count + 1, last_used = ?
                WHERE command_hash = ?
            ''', (datetime.now().isoformat(), command_hash))
            
            conn.commit()
            
            # Return enhanced analysis
            analysis = {
                'command_hash': command_hash,
                'original_command': command,
                'detected_type': detected_type,
                'confidence_score': min(confidence + (usage_count * 0.05), 1.0),  # Increase confidence with usage
                'keywords': json.loads(keywords_json),
                'success_rate': success_rate,
                'avg_quality': avg_quality,
                'usage_count': usage_count + 1,
                'is_learned': True
            }
            
            print(f"🧠 ENHANCED ANALYSIS (Used {usage_count + 1} times): {detected_type}")
            
            conn.close()
            return analysis
        
        conn.close()
        return None
    
    def learn_from_feedback(self, generation_id, command_hash, satisfaction, quality_metrics):
        """Learn from user feedback"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Store feedback
        conn.execute('''
            INSERT INTO learning_feedback 
            (generation_id, command_hash, user_satisfaction, quality_metrics)
            VALUES (?, ?, ?, ?)
        ''', (
            generation_id,
            command_hash,
            satisfaction,
            json.dumps(quality_metrics)
        ))
        
        # Update command analysis with new quality data
        conn.execute('''
            UPDATE command_analysis 
            SET avg_quality = (avg_quality + ?) / 2,
                success_rate = CASE 
                    WHEN ? >= 4 THEN (success_rate + 0.1)
                    ELSE (success_rate - 0.05)
                END
            WHERE command_hash = ?
        ''', (
            quality_metrics.get('overall', 0.5),
            satisfaction,
            command_hash
        ))
        
        conn.commit()
        conn.close()
        
        print(f"📈 LEARNED FROM FEEDBACK: Satisfaction {satisfaction}/5")
    
    def get_learning_stats(self):
        """Get comprehensive learning statistics"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Total commands learned
        cursor = conn.execute('SELECT COUNT(*) FROM command_analysis')
        total_commands = cursor.fetchone()[0]
        
        # Average success rate
        cursor = conn.execute('SELECT AVG(success_rate) FROM command_analysis')
        avg_success = cursor.fetchone()[0] or 0
        
        # Most used command type
        cursor = conn.execute('''
            SELECT detected_type, SUM(usage_count) as total_usage
            FROM command_analysis 
            GROUP BY detected_type 
            ORDER BY total_usage DESC 
            LIMIT 1
        ''')
        
        most_used = cursor.fetchone()
        
        conn.close()
        
        stats = {
            'total_commands_learned': total_commands,
            'average_success_rate': round(avg_success, 3),
            'most_used_type': most_used[0] if most_used else 'None',
            'most_used_count': most_used[1] if most_used else 0,
            'learning_efficiency': min(total_commands * 0.02, 1.0)
        }
        
        print("📊 LEARNING STATISTICS:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return stats
    
    def test_learning_system(self):
        """Test the learning system"""
        print("🧪 TESTING KI LEARNING SYSTEM...")
        
        # Test commands
        test_commands = [
            "Erstelle ein modernes Logo für Tech-Firma",
            "Generiere Banner für Online-Shop",
            "Mache Icon für Fitness-App",
            "Erstelle ein modernes Logo für Tech-Firma"  # Repeat to test learning
        ]
        
        for cmd in test_commands:
            analysis = self.analyze_command(cmd)
            print(f"  -> {cmd[:30]}... = {analysis['detected_type']}")
        
        # Show learning stats
        self.get_learning_stats()
        
        print("🎯 LEARNING SYSTEM TEST COMPLETED")

if __name__ == "__main__":
    learning_system = MegaUltraKILearning()
    learning_system.test_learning_system()