from langchain_core.tools import tool
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv()

# 🔧 Static setup for browser
driver = webdriver.Chrome()
driver.get("https://zehraarshad.vercel.app/")  # 🔁 Replace with your actual website

@tool
def go_to_home():
    """Navigate to the Home page."""
    link = driver.find_element(By.LINK_TEXT, "Home")
    link.click()
    return "Navigated to Home page."

@tool
def go_to_tools():
    """Navigate to the Tools page."""
    link = driver.find_element(By.LINK_TEXT, "Tools")
    link.click()
    return "Navigated to Tools page."

@tool
def go_to_achievements():
    """Navigate to the Achievements page."""
    link = driver.find_element(By.LINK_TEXT, "Achievements")
    link.click()
    return "Navigated to Achievements page."

@tool
def go_to_projects():
    """Navigate to the Projects page."""
    link = driver.find_element(By.LINK_TEXT, "Projects")
    link.click()
    return "Navigated to Projects page."

@tool
def explain_feature():
    """Explain the current page."""
    return "This is a portfolio-style page with different sections like Home, Tools, Achievements, and Projects."

@tool
def summarize_page():
    """Summarize the visible content of the current page."""
    body = driver.find_element(By.TAG_NAME, "body").text
    # Truncate or clean text as needed
    return body[:1000]  # Send the first 1000 characters to avoid overload
    