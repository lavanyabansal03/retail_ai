import pandas as pd


def load_and_process(path):
    """
    Load raw retail CSV, clean and return processed DataFrame.
    Keeps original 'Customer ID' column name for consistency
    with the rest of the codebase.
    """
    df = pd.read_csv(path)

    df = df[df['Quantity'] > 0]
    df = df.dropna(subset=['Customer ID'])

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice']  = df['Quantity'] * df['UnitPrice']

    return df