from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# --- User input ---
text = input("Enter the text to seach in Chatgpt ")

# --- Open Chrome ---
driver = webdriver.Chrome()
driver.get("https://chatgpt.com/")
time.sleep(2)  # wait for page to load
search_box = driver.find_element(By.CLASS_NAME, "pl")
search_box.send_keys(text)
search_box.send_keys(Keys.RETURN)