# agent.py

import os
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
# Import your tool functions
from actions import go_to_home, go_to_projects, go_to_tools, go_to_achievements, summarize_page
# browse_with_agent
import actions

# ✅ Step 1: Define tools list
tools = [go_to_home, go_to_projects, go_to_tools, go_to_achievements,summarize_page]
# tools = [browse_with_agent]
tools_by_name = {tool.name: tool for tool in tools} 

# ✅ Step 2: Initialize LLM and bind tools
llm = ChatGroq(
    model_name="llama3-8b-8192",  # or "llama3-70b-8192"
    api_key=os.getenv("GROQ_API_KEY"),
).bind_tools(tools)

# browser_agent = BrowserAgent(llm=llm, task="You are a voice-controlled demo agent. Perform user instructions like clicking, scrolling, and explaining what's on the screen.")
# actions.browser_agent = browser_agent
# ✅ Step 3: Node functions

def llm_node(state: dict):
    """Calls the LLM and adds its response to the message list."""
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages.insert(
            0,
            SystemMessage(
                content="You are a voice-based demo assistant. Help the user by navigating the UI and explaining features."
            )
        )
    result = llm.invoke(messages)
    return {"messages": messages + [result]}


def action_node(state: dict):
    """Executes tool calls and appends ToolMessages to the state."""
    tool_messages = []
    last_msg = state["messages"][-1]
    for call in last_msg.tool_calls:
        tool = tools_by_name[call["name"]]
        output = tool.invoke(call["args"])
        tool_messages.append(
            ToolMessage(content=str(output), tool_call_id=call["id"])
        )
    return {"messages": state["messages"] + tool_messages}


def should_continue(state: dict) -> Literal["Action", END]:
    """Checks if the LLM made tool calls."""
    last = state["messages"][-1]
    return "Action" if getattr(last, "tool_calls", None) else END

# ✅ Step 4: Build LangGraph agent
graph = StateGraph(dict)
graph.add_node("llm", llm_node)
graph.add_node("action", action_node)
graph.set_entry_point("llm")

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "Action": "action",
        END: END,
    },
)
graph.add_edge("action", "llm")

agent = graph.compile()
