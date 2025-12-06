"""Rate Limiting + Caching"""
import time
from typing import Dict, Any
from collections import defaultdict
import hashlib
import json

class RateLimiter:
    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limit"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_id] = [t for t in self.requests[client_id] if t > minute_ago]
        
        if len(self.requests[client_id]) < self.requests_per_minute:
            self.requests[client_id].append(now)
            return True
        return False
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        minute_ago = now - 60
        self.requests[client_id] = [t for t in self.requests[client_id] if t > minute_ago]
        return max(0, self.requests_per_minute - len(self.requests[client_id]))

class Cache:
    def __init__(self, ttl: int = 300):
        self.cache = {}
        self.ttl = ttl
    
    def _key(self, module: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key"""
        data = f"{module}:{json.dumps(args)}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, module: str, args: tuple = (), kwargs: dict = None) -> Any:
        """Get cached result"""
        if kwargs is None:
            kwargs = {}
        
        key = self._key(module, args, kwargs)
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, module: str, result: Any, args: tuple = (), kwargs: dict = None):
        """Cache result"""
        if kwargs is None:
            kwargs = {}
        
        key = self._key(module, args, kwargs)
        self.cache[key] = (result, time.time())
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        now = time.time()
        valid = sum(1 for _, (_, ts) in self.cache.items() if now - ts < self.ttl)
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid,
            "expired_entries": len(self.cache) - valid
        }

rate_limiter = RateLimiter(requests_per_minute=100)
cache = Cache(ttl=300)
