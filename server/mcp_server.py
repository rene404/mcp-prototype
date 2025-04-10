import os
# from server.base import MCPServer, tool
# import redis

# Redis instance (used in all servers)
# redis_client = redis.Redis(host="redis", port=6379, db=0)

# Import your MCP servers (modular style)
from mcp.docs.doc_search import DocumentSearchServer
# from mcp_financial.financial_history import FinancialHistoryServer
# from mcp_stock.live_stock import LiveStockServer

# Get environment var set in docker-compose
server_name = os.getenv("MCP_SERVER_NAME")

# Dynamically start the correct server
if server_name == "DocumentSearchServer":
    server = DocumentSearchServer()
# elif server_name == "FinancialHistoryServer":
#     server = FinancialHistoryServer()
# elif server_name == "LiveStockServer":
#     server = LiveStockServer()
else:
    raise ValueError(f"Unknown MCP_SERVER_NAME: {server_name}")

# Start the server
if __name__ == "__main__":
    server.run()
