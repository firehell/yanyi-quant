import pandas as pd
from sqlalchemy import create_engine

# Database connection details
db_config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'Zz941029',
    'database': 'stock-america'
}

def clean_historical_data():
    # Construct the database connection string
    engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    try:
        # Read historical data from the 'stock_data' table (adjust table name if needed)
        query = "SELECT ticker, volume, open, close, high, low, window_start FROM stock_data"
        df = pd.read_sql(query, engine)
        print("Successfully read historical data.")

        # Mark missing values (example: fill with 0 or NaN, depending on your requirement)
        df.fillna(0, inplace=True)
        print("Missing values marked.")

        # Mark price and volume outliers (example: using interquartile range - adjust thresholds as needed)
        for col in ['open', 'close', 'high', 'low', 'volume']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[f'{col}_is_outlier'] = (df[col] < lower_bound) | (df[col] > upper_bound)
        print("Price and volume outliers marked.")

        # You can add more data cleaning steps here as needed

        # For demonstration, print the first few rows of the cleaned data
        print("\nCleaned Data Preview:")
        print(df.head())

        # TODO: Here you would typically save the cleaned data back to the database or a new file

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_historical_data()