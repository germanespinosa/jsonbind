import importlib.util

spec = importlib.util.find_spec('numpy')
if not spec:
    raise RuntimeError("pandas not installed")
else:
    import numpy as np
    from ..object import Object
    from ..list import List

    def to_numpy_array(self):
        """
        Convert the list to a numpy array.

        Returns:
        numpy.array: The numpy array representation of the list.

        Notes:
        Only supports conversion if the list contains simple types (int, float, bool) or JsonObject instances.
        """
        if self.list_type is None:
            raise TypeError("list must have a list_type")

        if issubclass(self.list_type, Object):
            if not self:
                return np.array()
            columns = self[0].get_columns()
            values = [tuple([column_value for column_name, column_value in i.get_values()]) for i in self]
            return np.array(values, dtype=columns)

        return np.array(self)

    List.to_numpy_array = to_numpy_array

    @classmethod
    def from_numpy_array(list_cls: type, numpy_array: np.array, list_type: type = None) -> List:
        """
        Populate the list from a numpy array.

        Parameters:
        - a (numpy.array): The array to load data from.

        Notes:
        Only supports loading from an array if the list's type is a JsonObject or a simple type.
        """
        if not issubclass(list_cls, List):
            raise TypeError("list_cls must inherit from List")

        new_list = list_cls()

        if list_type is not None:
            new_list.list_type = list_type

        if new_list.list_type is None:
            raise TypeError("list must have a list_type")

        if issubclass(new_list.list_type, Object):
            columns = numpy_array.dtype.names
            for row in numpy_array:
                ni = new_list.list_type()
                for i, c in enumerate(columns):
                    ni[c] = row[i].item()
                new_list.append(ni)
        else:
            for row in numpy_array:
                new_list.append(row[0].item())
        return new_list

    List.from_numpy_array = from_numpy_array

