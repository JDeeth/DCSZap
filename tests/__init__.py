def arg_or_kwarg(mock_call, position=None, key=None):
    """Get mock call argument by either keyword or position"""
    func_name, args, kwargs = mock_call
    if key and key in kwargs:
        return kwargs[key]
    return args[position]
