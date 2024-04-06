import pandas as pd

# Load data from a file (CSV is assumed here)
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None

# Identify and remove duplicate rows
def remove_duplicates(df):
    return df.drop_duplicates()

# Fill missing values in a column with the column's mean or median, or a specified value
def fill_missing_values(df, strategy='mean', columns=None, fill_value=None):
    if columns is None:
        columns = df.columns
    for column in columns:
        if strategy == 'mean':
            df[column].fillna(df[column].mean(), inplace=True)
        elif strategy == 'median':
            df[column].fillna(df[column].median(), inplace=True)
        elif strategy == 'value' and fill_value is not None:
            df[column].fillna(fill_value, inplace=True)
    return df

# Convert columns to the best possible dtypes, reducing memory usage
def optimize_dtypes(df):
    return df.convert_dtypes()

# Standardize string columns to have consistent case
def standardize_text(df, columns=None):
    if columns is None:
        columns = df.select_dtypes(include=['string', 'object']).columns
    for column in columns:
        df[column] = df[column].str.lower().str.strip()
    return df

# Drop columns with too many missing values
def drop_sparse_columns(df, threshold=0.5):
    return df.dropna(axis=1, thresh=int(threshold * len(df)))

# Remove outliers from a dataframe by column, removing rows that are n standard deviations from mean
def remove_outliers(df, n=2):
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        mean = df[column].mean()
        std = df[column].std()
        df = df[(df[column] > (mean - n * std)) & (df[column] < (mean + n * std))]
    return df

# Save the cleaned data to a new CSV file
def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

if __name__ == '__main__':
    # Replace 'path_to_your_data.csv' with the path to the file you want to clean
    data_file_path = 'path_to_your_data.csv'
    cleaned_data_file_path = 'path_to_cleaned_data.csv'

    # Load the data
    data = load_data(data_file_path)
    if data is not None:
        # Apply cleaning functions
        data = remove_duplicates(data)
        data = fill_missing_values(data)
        data = optimize_dtypes(data)
        data = standardize_text(data)
        data = drop_sparse_columns(data)
        data = remove_outliers(data)

        # Save the cleaned data
        save_data(data, cleaned_data_file_path)