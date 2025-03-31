import os
import redis

# Redis instance (used in all servers)
redis_client = redis.Redis(host="redis", port=6379, db=0)

# MCPServer base class and tool decorator (you can define them right here or import from a shared utils file if needed)
class MCPServer:
    def run(self):
        print(f"Running {self.__class__.__name__}...")

def tool(func):
    return func
