from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def scale_column(df, column: str, range_tup: tuple = (0, 1)) -> pd.DataFrame:
    """
        Returns the objects DataFrames column normalized using Normalizer
        Parameters
    """
    try:
        std_column_df = pd.DataFrame(df[column])
        std_column_values = std_column_df.values
        minmax_scaler = MinMaxScaler(feature_range=range_tup)
        normalized_data = minmax_scaler.fit_transform(std_column_values)
        df[column] = normalized_data
        return df
    except Exception as e:
        print(f"scale_column----->{e}")

def scale_columns(df, columns: list, range_tup: tuple = (0, 1)) -> pd.DataFrame:
    try:
        for col in columns:
            df = scale_column(df, col, range_tup)
        return df
    except Exception as e:
        return None

def change_datatypes(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    A simple function which changes the data types of the dataframe and returns it
    """
    try:
        data_types = dataframe.dtypes
        changes = ['float64', 'int64']
        for col in data_types.index:
            if(data_types[col] in changes):
                if(data_types[col] == 'float64'):
                    dataframe[col] = pd.to_numeric(
                        dataframe[col], downcast='float')
                elif(data_types[col] == 'int64'):
                    dataframe[col] = pd.to_numeric(
                        dataframe[col], downcast='unsigned')     
    except Exception as e:
        print(e)

    return dataframe