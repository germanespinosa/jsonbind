import importlib.util

spec = importlib.util.find_spec('pandas')
if not spec:
    raise RuntimeError("pandas not installed")
else:
    import pandas as pd
    from ..object import Object
    from ..list import List


    def to_data_series(self) -> pd.Series:
        """
        Convert the JsonObject into a pandas Series.

        Args:
            recursive (bool, optional): If True, converts nested JsonObjects and JsonLists as well.

        Returns:
            pandas.core.series.Series: A pandas Series representation of the JsonObject.
        """
        values = {key: value.to_data_frame() if isinstance(value, List) else value for key, value in self.get_values()}

        return pd.Series(values)

    Object.to_data_series = to_data_series

    def to_data_frame(self):
        """
        Convert the list to a pandas DataFrame.

        Parameters:
        - recursive (bool): Flag to indicate if nested objects should be recursively converted to DataFrame columns.

        Returns:
        pandas.DataFrame: The DataFrame representation of the list.
        """
        if self.list_type is None:
            raise TypeError("list must have a list_type")

        if issubclass(self.list_type, Object):
            return pd.DataFrame([i.to_data_series() for i in self])
        else:
            return pd.DataFrame(self)


    List.to_data_frame = to_data_frame

    #
    #
    # def from_dataframe(self, df: pd.DataFrame) -> List:
    #     """
    #     Populate the list from a pandas DataFrame.
    #
    #     Parameters:
    #     - df (pandas.DataFrame): The DataFrame to load data from.
    #     """
    #     self.clear()
    #     columns = df.columns
    #     for i, row in df.iterrows():
    #         ni = self.list_type()
    #         for c in columns:
    #             ni[c] = row[c]
    #         self.append(ni)
    #     return self
    #
    # List.from_dataframe = from_dataframe
