from server.base import MCPServer, tool
import psycopg2
import redis
import json

# Initialize Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRATION = 600  # 10 minutes

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=finance user=admin password=secret")
cursor = conn.cursor()

class FinancialHistoryServer(MCPServer):

    @tool
    def get_financial_history(self, stock_symbol: str):
        """Fetch historical stock data."""
        cache_key = f"financial:{stock_symbol}"

        # Check cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        # Query database if not in cache
        query = f"SELECT * FROM stock_prices WHERE symbol='{stock_symbol}' ORDER BY date DESC LIMIT 5"
        cursor.execute(query)
        result = cursor.fetchall()

        response = {"stock_symbol": stock_symbol, "history": result}
        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(response))

        return response

if __name__ == "__main__":
    server = FinancialHistoryServer()
    server.run()
