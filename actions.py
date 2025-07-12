# actions.py

from langchain_core.tools import tool
from selenium import webdriver

driver = webdriver.Chrome()  # or use remote driver
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
