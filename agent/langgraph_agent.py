import os
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.tools import Tool
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# LLM setup
llm = ChatOpenAI(model="gpt-4", temperature=0)

# MCP Server URLs
MCP_DOCS_URL = "http://localhost:8003"
MCP_FINANCIAL_URL = "http://localhost:8001"
MCP_STOCK_URL = "http://localhost:8002"

# Define MCP tools
def search_papers(keyword):
    res = requests.post(f"{MCP_DOCS_URL}/tools/search_research_papers", json={"keyword": keyword})
    return res.json()

def get_financial_data(symbol):
    res = requests.post(f"{MCP_FINANCIAL_URL}/tools/get_financial_history", json={"stock_symbol": symbol})
    return res.json()

def get_stock_price(symbol):
    res = requests.post(f"{MCP_STOCK_URL}/tools/get_stock_price", json={"symbol": symbol})
    return res.json()

# Wrap tools
search_tool = Tool(name="SearchDocs", func=search_papers)
history_tool = Tool(name="StockHistory", func=get_financial_data)
price_tool = Tool(name="LivePrice", func=get_stock_price)

# Agent state
class AgentState:
    context: dict

# Main LangGraph node using LLM to orchestrate tool calls
def llm_orchestrator(state):
    question = "Give me an update on Apple Inc. with current stock info and recent financial context."

    # LLM decides which tools to call based on the question
    messages = [
        SystemMessage(content="You are a financial assistant."),
        HumanMessage(content=question)
    ]

    response = llm(messages)

    # Simulate basic LLM tool routing (you could also parse with structured output / ReAct)
    tools_called = {
        "stock": price_tool.invoke("AAPL"),
        "history": history_tool.invoke("AAPL"),
        "docs": search_tool.invoke("Apple Inc.")
    }

    return {
        "response": f"""📘 Docs: {tools_called['docs']}
📉 History: {tools_called['history']}
💰 Live Price: {tools_called['stock']}"""
    }

# LangGraph Workflow
workflow = StateGraph(AgentState)
workflow.add_node("llm_decision", llm_orchestrator)
workflow.set_entry_point("llm_decision")
workflow.set_finish_point(END)
agent_executor = workflow.compile()

# Run it
if __name__ == "__main__":
    result = agent_executor.invoke({})
    print("\n🧠 AI Agent Final Output:")
    print(result["response"])
