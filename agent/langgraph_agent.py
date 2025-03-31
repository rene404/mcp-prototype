import requests
from langchain.tools import Tool
from langgraph.graph import StateGraph, END

# MCP Server URLs (assumed exposed on these ports)
MCP_DOCS_URL = "http://localhost:8003"
MCP_FINANCIAL_URL = "http://localhost:8001"
MCP_STOCK_URL = "http://localhost:8002"

# MCP tool wrappers
def search_papers(keyword):
    res = requests.post(f"{MCP_DOCS_URL}/tools/search_research_papers", json={"keyword": keyword})
    return res.json()

def get_financial_data(symbol):
    res = requests.post(f"{MCP_FINANCIAL_URL}/tools/get_financial_history", json={"stock_symbol": symbol})
    return res.json()

def get_stock_price(symbol):
    res = requests.post(f"{MCP_STOCK_URL}/tools/get_stock_price", json={"symbol": symbol})
    return res.json()

# Wrap as LangGraph tools
search_tool = Tool(name="SearchDocs", func=search_papers)
history_tool = Tool(name="StockHistory", func=get_financial_data)
price_tool = Tool(name="LivePrice", func=get_stock_price)

# Agent state
class AgentState:
    context: dict

workflow = StateGraph(AgentState)

def orchestrate_query(state):
    symbol = "AAPL"
    docs = search_tool.invoke("Apple")
    history = history_tool.invoke(symbol)
    live = price_tool.invoke(symbol)

    return {
        "response": f"📘 Docs: {docs}\n📉 History: {history}\n💰 Live Price: {live}"
    }

workflow.add_node("process", orchestrate_query)
workflow.set_entry_point("process")
workflow.set_finish_point(END)

# Run it!
agent_executor = workflow.compile()

if __name__ == "__main__":
    result = agent_executor.invoke({})
    print("\n🧠 AI Agent Final Output:")
    print(result["response"])
