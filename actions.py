from langchain_core.tools import tool
from selenium import webdriver
from browser_use import Agent as BrowserAgent
from langchain_groq import ChatGroq
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

# 🔧 Existing static setup
driver = webdriver.Chrome()
driver.get("https://coreui.io/react/#/dashboard")

@tool
def go_to_dashboard():
    """Navigate to the dashboard page."""
    dashboard_button = driver.find_element("id", "dashboard")
    dashboard_button.click()
    return "Navigated to Dashboard"

@tool
def go_to_settings():
    """Open the settings page."""
    settings_button = driver.find_element("id", "settings")
    settings_button.click()
    return "Opened Settings"

@tool
def explain_feature():
    """Explain the current page feature."""
    return "This is the analytics dashboard showing KPIs in real time."

# browser_agent = None
# @tool
# def browse_with_agent(command: str):
#     """Use browser AI to follow open-ended instructions like 'search', 'click', 'scroll', 'summarize'."""
#     if browser_agent is None:
#         return "❌ Browser agent not initialized."
#     return asyncio.run(browser_agent.run(command))