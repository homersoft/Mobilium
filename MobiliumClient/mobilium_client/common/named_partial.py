from functools import partial, update_wrapper


def named_partial(func, *args, **kwargs):
    """
    __name__ and __doc__ attributes are not created automatically for partial.
    Use that function to propagate these properties from the original function.
    """
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func
