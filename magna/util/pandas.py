import pandas as pd


def optimise_df(df: pd.DataFrame):
    """Optimise a Pandas DataFrame by using the smallest possible data type.

    Args:
        df: The Pandas DataFrame to optimise.
    """

    float_cols = df.select_dtypes('float').columns
    int_cols = df.select_dtypes('integer').columns
    df[float_cols] = df[float_cols].apply(pd.to_numeric, downcast='float')
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')
