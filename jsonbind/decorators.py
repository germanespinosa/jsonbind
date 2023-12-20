from .core import Bindings, Serialization


def parse_parameters(funct):
    import inspect
    sig = inspect.signature(funct)
    params_bindings = dict()

    var_keyword = is_method = is_class = False
    for parameter_name, parameter in sig.parameters.items():
        if parameter_name == "self":
            is_method = True
            continue
        if parameter_name == "cls":
            is_class = True
            continue
        if parameter.kind == parameter.VAR_KEYWORD:
            var_keyword = True
            continue
        if parameter.annotation:
            params_bindings[parameter_name] = Bindings.find_binding(parameter.annotation)
        else:
            params_bindings[parameter_name] = None

    def get_parsed_parameters(json_string:str) -> dict:
        params_dict = Serialization.deserialize(json_string=json_string, python_type=dict)
        parsed_params = dict()
        for parameter_name, parameter_value in params_dict.items():
            print(parameter_name, parameter_value)
            if parameter_name in params_bindings:
                binding = params_bindings[parameter_name]
                if binding:
                    parsed_params[parameter_name] = binding.to_python_value(parameter_value)
                else:
                    parsed_params[parameter_name] = parameter_value
            elif var_keyword:
                parsed_params[parameter_name] = parameter_value
        return parsed_params

    if is_method:
        def parsed_parameters(self, json_string: str):
            parsed_params = get_parsed_parameters(json_string=json_string)
            return funct(self, **parsed_params)
    elif is_class:
        def parsed_parameters(cls, json_string: str):
            parsed_params = get_parsed_parameters(json_string=json_string)
            return funct(cls, **parsed_params)
    else:
        def parsed_parameters(json_string: str):
            parsed_params = get_parsed_parameters(json_string=json_string)
            return funct(**parsed_params)

    parsed_parameters.__name__ = funct.__name__
    return parsed_parameters