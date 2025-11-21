import pandas as pd
import numpy as np
import os

class DataPreprocessor:
    def __init__(self, filepath=None, df=None):
        """
        Initialize the DataPreprocessor with a file path or a DataFrame.
        """
        self.df = df
        if filepath:
            self.load_data(filepath)

    def load_data(self, filepath):
        """
        Load data from a CSV or Excel file.
        """
        try:
            if filepath.endswith('.csv'):
                self.df = pd.read_csv(filepath)
            elif filepath.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(filepath)
            else:
                print(f"Unsupported file format: {filepath}")
                return
            print(f"Successfully loaded data from {filepath}")
            print(f"Shape: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")

    def check_duplicates(self):
        """
        Check for and report duplicated rows.
        """
        if self.df is None:
            print("No data loaded.")
            return 0
        
        duplicates = self.df.duplicated().sum()
        print(f"Number of duplicated rows: {duplicates}")
        return duplicates

    def remove_duplicates(self):
        """
        Remove duplicated rows.
        """
        if self.df is None:
            print("No data loaded.")
            return

        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.df)
        print(f"Removed {removed_rows} duplicated rows.")

    def check_missing_values(self):
        """
        Check for missing values in each column.
        """
        if self.df is None:
            print("No data loaded.")
            return

        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            print("No missing values found.")
        else:
            print("Missing values per column:")
            print(missing)
            print("\nPercentage of missing values:")
            print((missing / len(self.df)) * 100)

    def handle_missing_values(self, strategy='drop', fill_value=None):
        """
        Handle missing values.
        strategy: 'drop', 'mean', 'median', 'mode', 'constant'
        """
        if self.df is None:
            print("No data loaded.")
            return

        if strategy == 'drop':
            self.df.dropna(inplace=True)
            print("Dropped rows with missing values.")
        elif strategy == 'constant' and fill_value is not None:
            self.df.fillna(fill_value, inplace=True)
            print(f"Filled missing values with {fill_value}.")
        elif strategy in ['mean', 'median', 'mode']:
            # Apply only to numeric columns for mean/median
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            
            for col in self.df.columns:
                if self.df[col].isnull().any():
                    if col in numeric_cols:
                        if strategy == 'mean':
                            self.df[col].fillna(self.df[col].mean(), inplace=True)
                        elif strategy == 'median':
                            self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        # For categorical columns, mode is often used or just ignored if strategy is mean/median
                        if strategy == 'mode':
                            self.df[col].fillna(self.df[col].mode()[0], inplace=True)
            print(f"Filled missing values using {strategy} strategy.")
        else:
            print(f"Unknown strategy: {strategy}")

    def get_summary(self):
        """
        Print a summary of the dataset.
        """
        if self.df is None:
            print("No data loaded.")
            return

        print("\n--- Dataset Info ---")
        print(self.df.info())
        print("\n--- Descriptive Statistics ---")
        print(self.df.describe(include='all'))
        print("\n--- Head ---")
        print(self.df.head())

    def save_data(self, output_path):
        """
        Save the processed DataFrame to a file.
        """
        if self.df is None:
            print("No data loaded.")
            return

        try:
            if output_path.endswith('.csv'):
                self.df.to_csv(output_path, index=False)
            elif output_path.endswith(('.xls', '.xlsx')):
                self.df.to_excel(output_path, index=False)
            else:
                print("Unsupported output format. Saving as CSV.")
                self.df.to_csv(output_path + '.csv', index=False)
            print(f"Data saved to {output_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

if __name__ == "__main__":
    # Example usage
    # Create a dummy dataset for demonstration
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Eve', None],
        'Age': [25, 30, 35, 25, 28, 22],
        'Salary': [50000, 60000, None, 50000, 55000, 45000],
        'City': ['New York', 'Los Angeles', 'Chicago', 'New York', None, 'Boston']
    }
    
    print("Creating a dummy dataset for demonstration...")
    df_dummy = pd.DataFrame(data)
    
    # Initialize preprocessor with the dummy dataframe
    preprocessor = DataPreprocessor(df=df_dummy)
    
    print("\n--- Initial Data ---")
    print(preprocessor.df)

    print("\n--- Checking Duplicates ---")
    preprocessor.check_duplicates()
    
    print("\n--- Removing Duplicates ---")
    preprocessor.remove_duplicates()
    
    print("\n--- Checking Missing Values ---")
    preprocessor.check_missing_values()
    
    print("\n--- Handling Missing Values (filling numeric with mean, categorical with mode) ---")
    # Simple demonstration: fill numeric with mean
    preprocessor.handle_missing_values(strategy='mean')
    # Fill remaining categorical with mode
    preprocessor.handle_missing_values(strategy='mode')

    print("\n--- Final Summary ---")
    preprocessor.get_summary()
    
    # To use with a real file, you would do:
    # preprocessor = DataPreprocessor(filepath='path/to/your/data.csv')
    # preprocessor.check_duplicates()
    # ...
