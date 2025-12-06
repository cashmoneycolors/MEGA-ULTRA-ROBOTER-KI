"""
GitHub Integration für Autonomous Zenith Optimizer
Nutzt die GitHub Tokens aus der .env Datei
"""
import os
import requests
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_TOKEN_BACKUP = os.getenv('GITHUB_TOKEN_BACKUP')

class GitHubClient:
    """Client für GitHub API Integration"""
    
    def __init__(self, token=None):
        self.token = token or GITHUB_TOKEN
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def test_connection(self):
        """Teste GitHub Verbindung"""
        try:
            response = requests.get(
                f'{self.base_url}/user',
                headers=self.headers,
                timeout=10,
                verify=True
            )
            response.raise_for_status()
            user_data = response.json()
            return {
                'status': 'success',
                'user': user_data.get('login'),
                'name': user_data.get('name'),
                'email': user_data.get('email'),
                'public_repos': user_data.get('public_repos')
            }
        except requests.exceptions.HTTPError as e:
            return {
                'status': 'error',
                'message': f'HTTP {e.response.status_code}: {e.response.text}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_repo_info(self, owner, repo):
        """Hole Repository Informationen"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{owner}/{repo}',
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Fehler beim Abrufen der Repo-Infos: {e}")
            return None
    
    def create_issue(self, owner, repo, title, body):
        """Erstelle ein GitHub Issue"""
        try:
            response = requests.post(
                f'{self.base_url}/repos/{owner}/{repo}/issues',
                headers=self.headers,
                json={'title': title, 'body': body},
                timeout=10
            )
            if response.status_code == 201:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Fehler beim Erstellen des Issues: {e}")
            return None

def test_github_integration():
    """Teste die GitHub Integration"""
    print("=== GitHub Integration Test ===")
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN nicht in .env gefunden!")
        return False
    
    print(f"✓ GITHUB_TOKEN gefunden: {GITHUB_TOKEN[:20]}...")
    
    client = GitHubClient()
    result = client.test_connection()
    
    if result['status'] == 'success':
        print(f"✓ GitHub Verbindung erfolgreich!")
        print(f"  Benutzer: {result.get('user')}")
        print(f"  Name: {result.get('name')}")
        return True
    else:
        print(f"❌ GitHub Verbindung fehlgeschlagen: {result.get('message')}")
        
        # Versuche Backup Token
        if GITHUB_TOKEN_BACKUP:
            print("\nVersuche Backup Token...")
            client_backup = GitHubClient(GITHUB_TOKEN_BACKUP)
            result_backup = client_backup.test_connection()
            
            if result_backup['status'] == 'success':
                print(f"✓ Backup Token funktioniert!")
                print(f"  Benutzer: {result_backup.get('user')}")
                return True
        
        return False

if __name__ == "__main__":
    test_github_integration()
