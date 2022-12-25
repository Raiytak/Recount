import abc


class AbstractVue:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractproperty
    def vue(self):
        """Returns the complete vue"""
