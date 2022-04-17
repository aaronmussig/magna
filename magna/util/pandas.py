import numpy as np
import pandas as pd


def optimise_df(df: pd.DataFrame, integers: bool = True, floats: bool = True):
    """Optimise a Pandas DataFrame by using the smallest possible data type.

    Args:
        df: The Pandas DataFrame to optimise.
        integers: Whether to optimise the integers.
        floats: Whether to optimise the floats.
    """
    if floats:
        float_types = [np.float16, np.float32]
        float_cols = df.select_dtypes('float').columns
        for float_col in float_cols:
            for float_type in float_types:
                if np.min(df[float_col] - df[float_col].astype(float_type)) == 0:
                    df[float_col] = df[float_col].astype(float_type)
                    break

    if integers:
        sint_types = [np.int8, np.int16, np.int32, np.int64]
        uint_types = [np.uint8, np.uint16, np.uint32, np.uint64]
        sint_info = [np.iinfo(t) for t in sint_types]
        uint_info = [np.iinfo(t) for t in uint_types]

        int_cols = df.select_dtypes('integer').columns
        for int_col in int_cols:
            col_min, col_max = df[int_col].min(), df[int_col].max()

            # Determine which data types to use
            if col_min >= 0:
                int_info = uint_info
            else:
                int_info = sint_info

            # Set the data type
            for info in int_info:
                if col_min >= info.min and col_max <= info.max:
                    df[int_col] = df[int_col].astype(info.dtype)
                    break
