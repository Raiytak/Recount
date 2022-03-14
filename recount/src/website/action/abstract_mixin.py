import abc

import logs


class AbstractAction:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCallbacks()
        logs.formatAndDisplay(f"The callback of {self} has been set")

    @abc.abstractmethod
    def setCallbacks(self):
        """Set the callbacks to the components of the vue"""
