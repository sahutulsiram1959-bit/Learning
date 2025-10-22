import requests
import pandas as pd

# Step 1: API URL
url = "https://catfact.ninja/facts"

# Step 2: Send GET request
response = requests.get(url)
data = response.json()  # Convert to Python dictionary

# Step 3: Extract the 'data' part from JSON
facts = data['data']

# Step 4: Convert to DataFrame
df = pd.DataFrame(facts)

# Step 5: Save to Excel
df.to_excel("cat_facts.xlsx", index=False)

print("✅ Data extracted and saved to 'cat_facts.xlsx'")
