class OptionsService(object):
    """
    Simple singleton class that provides application-wide
    access to some options (e.g. debugging on/off).

    @since: 2011-09-26
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    _instance = None
    def __new__(cls, *args, **kwargs): # making this a Singleton, always returns the same instance
        if not cls._instance:
            cls._instance = super(OptionsService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "debug"):   # only create on first init
            self.debug = False

    def getDebug(self):
        return self.debug

    def setDebug(self, debug):
        self.debug = debug