import os
from mcp import MCPServer
import redis

# Initialize Redis
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Import all MCP servers
from mcp_financial import FinancialHistoryServer
from mcp_stock import LiveStockServer
from mcp_docs import DocumentSearchServer

# Get server name from environment variable
server_name = os.getenv("MCP_SERVER_NAME")

if server_name == "FinancialHistoryServer":
    server = FinancialHistoryServer()
elif server_name == "LiveStockServer":
    server = LiveStockServer()
elif server_name == "DocumentSearchServer":
    server = DocumentSearchServer()
else:
    raise ValueError("Unknown MCP Server Name")

# Start the server
if __name__ == "__main__":
    server.run()
