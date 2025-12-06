"""Performance Optimization"""
import functools
import time
from core.logging import logger

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.execution_times = []
    
    def cache_result(self, ttl=300):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = f"{func.__name__}_{args}_{kwargs}"
                if key in self.cache:
                    return self.cache[key]
                result = func(*args, **kwargs)
                self.cache[key] = result
                return result
            return wrapper
        return decorator
    
    def measure_time(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            self.execution_times.append(duration)
            logger.info(f"{func.__name__} took {duration:.2f}ms")
            return result
        return wrapper
    
    def get_avg_execution_time(self):
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0

optimizer = PerformanceOptimizer()
