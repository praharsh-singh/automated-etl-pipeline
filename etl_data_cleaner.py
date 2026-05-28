import os
import glob
import pandas as pd  # Pandas is a powerful data manipulation library (standard industry tool)
import numpy as np   # NumPy is used for complex mathematical arrays and handling empty spaces

class CorporateDataCleaner:
    """
    An Object-Oriented Programming (OOP) approach to building a reusable,
    modular ETL (Extract, Transform, Load) pipeline.
    
    Jargon Glossary:
    - OOP (Object-Oriented Programming): Structuring code using reusable "objects" rather than messy blocks of text.
    - ETL (Extract, Transform, Load): The process of grabbing raw data, cleaning it, and saving it properly.
    """
    def __init__(self, input_folder, output_file):
        self.input_folder = input_folder
        self.output_file = output_file
        self.combined_dataframe = pd.DataFrame()

    def extract_raw_data(self):
        """
        EXTRACT: Programmatically gathers all Excel/CSV files in a directory using glob pattern matching.
        """
        # glob looks for matching file names in a directory (like searching for *.csv)
        file_pattern = os.path.join(self.input_folder, "*.csv")
        all_files = glob.glob(file_pattern)
        
        if not all_files:
            print(f"[-] No raw data files found in {self.input_folder}")
            return False
            
        print(f"[+] Found {len(all_files)} raw data files. Initiating ingestion pipeline...")
        # Read and append all separate files into one master data holder (DataFrame)
        list_of_dfs = [pd.read_csv(file) for file in all_files]
        self.combined_dataframe = pd.concat(list_of_dfs, ignore_index=True)
        return True

    def transform_and_scrub(self):
        """
        TRANSFORM: Implements strict data scrubbing routines to sanitize the messy dataset.
        """
        print("[+] Initiating data transformation and scrubbing routines...")
        
        # 1. Deduplication (Removing exact clone rows that ruin data integrity)
        initial_count = len(self.combined_dataframe)
        self.combined_dataframe.drop_duplicates(inplace=True)
        print(f"    -> Removed {initial_count - len(self.combined_dataframe)} duplicate rows.")

        # 2. Schema Standardization (Trimming hidden spaces in column titles)
        self.combined_dataframe.columns = self.combined_dataframe.columns.str.strip()

        # 3. Imputation (Handling missing/empty fields so the system doesn't crash)
        # We fill empty text fields with "Unknown" and empty numeric fields with 0
        text_columns = self.combined_dataframe.select_dtypes(include=['object']).columns
        self.combined_dataframe[text_columns] = self.combined_dataframe[text_columns].fillna("Unknown")
        
        numeric_columns = self.combined_dataframe.select_dtypes(include=['number']).columns
        self.combined_dataframe[numeric_columns] = self.combined_dataframe[numeric_columns].fillna(0)
        
        print("[+] Data normalization and scrubbing complete.")

    def load_clean_dataset(self):
        """
        LOAD: Saves the pristine, standardized dataset into a final production-ready file.
        """
        if self.combined_dataframe.empty:
            print("[-] Transformation buffer is empty. Aborting load phase.")
            return
            
        # Save the clean data back to a master CSV file
        self.combined_dataframe.to_csv(self.output_file, index=False)
        print(f"[==>] SUCCESS: Pristine production dataset compiled at: {self.output_file}")

# Executing the automated script pipeline
if __name__ == "__main__":
    # Define setup folders (simulating a corporate environment)
    RAW_DATA_DIR = "raw_corporate_reports"
    CLEAN_OUTPUT_FILE = "production_cleaned_sales_data.csv"
    
    # Create the folder automatically if it doesn't exist yet
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)
        print(f"[*] Created '{RAW_DATA_DIR}' directory. Drop your messy CSVs inside it!")

    # Instantiate our engineered pipeline object
    pipeline = CorporateDataCleaner(input_folder=RAW_DATA_DIR, output_file=CLEAN_OUTPUT_FILE)
    
    # Run the automated pipeline steps sequentially
    if pipeline.extract_raw_data():
        pipeline.transform_and_scrub()
        pipeline.load_clean_dataset()