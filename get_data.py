import pandas as pd
import numpy as np
import os

# Target our main folder destination to overwrite it with pure chaos
TARGET_DIR = "raw_corporate_reports"
os.makedirs(TARGET_DIR, exist_ok=True)

print(f"[*] Generating 100 rows of high-chaos retail data into '{TARGET_DIR}'...")

# 1. Create a baseline of 80 rows
np.random.seed(42)
data = {
    "Transaction ID ": np.random.randint(10000, 99999, size=80),
    " Product Name": np.random.choice(["Laptop Sleeve", " Ergonomic Mouse ", "USB-C Hub", "Mechanical Keyboard"], size=80),
    "Category": np.random.choice(["Electronics", "Accessories", "Office Supplies"], size=80),
    "Quantity Ordered": np.random.randint(1, 5, size=80).astype(str), # saved as raw string
    "Unit Price": np.round(np.random.uniform(15.0, 150.0, size=80), 2)
}
df = pd.DataFrame(data)

# 2. INJECT CHAOS: Clone 15 rows completely to create blatant duplicates
duplicates = df.iloc[10:25].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 3. INJECT CHAOS: Scatter true missing values (NaN) inside Price and Quantity
for _ in range(8):
    df.loc[np.random.randint(0, 95), "Unit Price"] = np.nan
    df.loc[np.random.randint(0, 95), "Quantity Ordered"] = np.nan

# 4. INJECT CHAOS: Slip bad string data into numerical columns
df.loc[5, "Quantity Ordered"] = "UNKNOWN"
df.loc[12, "Quantity Ordered"] = "five"
df["Unit Price"] = df["Unit Price"].astype(object)  # Change the column layout to 'object' first so it accepts raw text mixing
df.loc[45, "Unit Price"] = "ERROR_VAL"

# 5. Expand rows out to exactly 100 rows
while len(df) < 100:
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

# Split into our primary multi-file targets
jan_sales = df.iloc[:50]
feb_sales = df.iloc[50:]

# Save them into our primary corporate folder
jan_sales.to_csv(f"{TARGET_DIR}/january_sales.csv", index=False)
feb_sales.to_csv(f"{TARGET_DIR}/february_sales.csv", index=False)

print(f"[==>] SUCCESS: Built a 100-row chaotic matrix inside '{TARGET_DIR}/'!")