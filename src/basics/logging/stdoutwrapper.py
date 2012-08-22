import logging
import sys

class StdOutWrapper(object):
    """
        Call wrapper for stdout
    """
    def __init__(self):
        super(StdOutWrapper, self).__init__()
        self.line = ""
        self.logy = logging.getLogger()
        self.stdout = sys.stdout
        sys.stdout = self

    def close(self):
        if self.stdout is not None:
            sys.stdout = self.stdout
            self.stdout = None

    def write(self, msg):
        self.line += msg
        if '\n' in msg:
            self.line = self.line.rstrip('\n').lstrip('\n')
            if self.line:
                self.logy.info(self.line)
            self.line = ""

    def flush(self):
        self.line = self.line.rstrip('\n').lstrip('\n')
        if self.line:
            self.logy.info(self.line)
        self.line = ""

