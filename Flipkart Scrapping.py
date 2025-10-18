from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# --- User input ---
item_name = input("Enter the product name to search on Flipkart: ")

# --- Open Chrome ---
driver = webdriver.Chrome()
driver.get("https://www.flipkart.com")
time.sleep(2)  # wait for page to load

# --- Close login popup if present ---
try:
    close_button = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
    close_button.click()
except:
    pass

# --- Search for the item ---
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(item_name)
search_box.send_keys(Keys.RETURN)
time.sleep(5)  # wait for search results to load

# --- Find product titles and prices ---
titles = driver.find_elements(By.CLASS_NAME, "KzDlHZ")
prices = driver.find_elements(By.CSS_SELECTOR, "div.Nx9bqj._4b5DiR")  # use CSS selector for multiple classes

print(f"\n🛒 Top products for '{item_name}':\n")
for i in range(min(20, len(titles))):
    title = titles[i].text
    price = prices[i].text if i < len(prices) else "Price not available"
    print(f"{i+1}. {title} >>>>> {price}")

# --- Keep browser open to check ---
time.sleep(10)
driver.quit()
