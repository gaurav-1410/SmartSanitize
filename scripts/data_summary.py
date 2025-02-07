import pandas as pd

def summarize_data(file_path):
    df = pd.read_csv(file_path)
    print("\n🔍 Dataset Summary:")
    print(df.info())
    print("\n📊 Missing Values:")
    print(df.isnull().sum())
    print("\n📏 Column Statistics:")
    print(df.describe())

if __name__ == "__main__":
    file_path = input("Enter the dataset path: ")
    summarize_data(file_path)
