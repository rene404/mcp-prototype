from mcp import tool
from mcp.server.fastmcp import FastMCP
import json
import os

# Load fake database from a JSON file
FAKE_DB_FILE = "fake_stock_data.json"

def load_fake_data():
    if not os.path.exists(FAKE_DB_FILE):
        return []
    with open(FAKE_DB_FILE, "r") as f:
        return json.load(f)

class FinancialHistoryServer(FastMCP):

    @tool
    def get_financial_history(self, stock_symbol: str):
        """Fetch historical stock data from fake JSON database."""
        data = load_fake_data()

        # Filter by stock symbol and sort by date descending
        filtered = [record for record in data if record["symbol"] == stock_symbol]
        filtered.sort(key=lambda x: x["date"], reverse=True)
        result = filtered[:5]

        return {"stock_symbol": stock_symbol, "history": result}

if __name__ == "__main__":
    server = FinancialHistoryServer()
    server.run()
