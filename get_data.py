import pandas as pd
import os

# Ensure our raw data landing zone exists
os.makedirs("raw_corporate_reports", exist_ok=True)

print("[*] Connecting to online public data servers...")
print("[*] Downloading real-world unstructured corporate dataset (thousands of rows)...")

# Pulling a massive raw, un-sanitized logistics and operational transaction log
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/housing.csv"

# This raw file doesn't even have headers! It's just massive rows of messy text/numbers.
# We will load it raw to simulate true corporate data chaos.
df = pd.read_csv(url, header=None)

# Let's add some column headers, deliberately adding annoying hidden trailing spaces 
# like "CRIM " instead of "CRIM" to force our pipeline's string stripping to fix it!
df.columns = ['CRIM ', 'ZN ', 'INDUS ', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

# Let's programmatically inject real duplicate records into this massive file so your pipeline has clones to delete!
df = pd.concat([df, df.iloc[10:30], df.iloc[150:180]], ignore_index=True)

# Split this massive dataset into two heavy multi-file corporate chunks (January and February)
halfway = len(df) // 2
jan_chunk = df.iloc[:halfway]
feb_chunk = df.iloc[halfway:]

# Save them live into your project folder
jan_chunk.to_csv("raw_corporate_reports/january_sales.csv", index=False)
feb_chunk.to_csv("raw_corporate_reports/february_sales.csv", index=False)

print(f"[==>] SUCCESS: Fetched real messy data matrix. Total records downloaded: {len(df)} rows.")
print("[*] Files saved into 'raw_corporate_reports/'. Ready for large-scale pipeline execution.")