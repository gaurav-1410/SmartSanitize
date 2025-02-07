import pandas as pd

def export_clean_data(df, file_name="cleaned_data"):
    df.to_csv(f"{file_name}.csv", index=False)
    df.to_json(f"{file_name}.json", orient="records")
    print(f"✅ Data exported as {file_name}.csv and {file_name}.json")

if __name__ == "__main__":
    # Example usage with dummy data
    data = {'A': [1, 2, None], 'B': ['X', 'Y', 'Z']}
    df = pd.DataFrame(data).fillna(0)  # Clean missing values
    export_clean_data(df)
