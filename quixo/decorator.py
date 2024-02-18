class classproperty(property):
    """
    Custom decorator that define a class level property
    """
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
