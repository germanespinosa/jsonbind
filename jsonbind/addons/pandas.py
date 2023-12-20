import importlib.util

spec = importlib.util.find_spec('pandas')
if not spec:
    raise RuntimeError("pandas not installed")
else:
    import pandas as pd
    from ..special.object import Object
    from ..special.list import List


    def to_data_series(self) -> pd.Series:
        """
        Convert the JsonObject into a pandas Series.

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

    @classmethod
    def from_data_frame(list_cls: type, data_frame:pd.DataFrame, list_type: type = None):
        if not issubclass(list_cls, List):
            raise TypeError("list_cls must inherit from List")

        new_list = list_cls()

        if list_type is not None:
            new_list.list_type = list_type

        if new_list.list_type is None:
            raise TypeError("list must have a list_type")
        if not issubclass(new_list.list_type, Object):
            raise TypeError("list_type must inherit from Object")
        columns = data_frame.dtypes.to_dict()
        for i, row in data_frame.iterrows():
            ni = new_list.list_type()
            for column_name, column_type in columns.items():
                ni[column_name] = row[column_name].item()
            new_list.append(ni)
        return new_list

    List.from_data_frame = from_data_frame
