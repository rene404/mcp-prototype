from mcp import MCPServer, tool
import requests
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)
STOCK_API_URL = "https://financial-api.com/stocks/"
CACHE_EXPIRATION = 60  # 1 minute

class LiveStockServer(MCPServer):

    @tool
    def get_stock_price(self, symbol: str):
        """Fetch live stock price."""
        cache_key = f"stock:{symbol}"

        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        # Call external API
        response = requests.get(f"{STOCK_API_URL}{symbol}").json()
        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(response))

        return response

if __name__ == "__main__":
    server = LiveStockServer()
    server.run()
