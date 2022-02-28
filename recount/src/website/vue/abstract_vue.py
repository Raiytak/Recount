import abc


class AbstractVue:
    @abc.abstractproperty
    def vue(self):
        """Returns the complete vue"""

