def singleton(cls):
    """Used as a decorator for classes that need to be a singleton

    :param **kwargs: Keyword arguments used for initialization of classes
    with decorator
    """
    instances = {}

    def get_instance(**kwargs):
        if cls not in instances:
            instances[cls] = cls(**kwargs)
        return instances[cls]
    return get_instance

    stuff = singleton.get_instance()
