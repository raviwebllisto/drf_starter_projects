import logging

class SpecialFilter(logging.Filter):

    def filter(self, record):
        try:
            if record.name == 'root':
                return True
            else:
                return False
        except:
            pass
class WarningFilter(logging.Filter):

    def filter(self, record):
        try:
            if record.levelname == 'WARNING':
                # import pdb;pdb.set_trace()
                return True
            else:
                return False
        except:
            pass
class ErrorFilter(logging.Filter):

    def filter(self, record):
        try:
            if record.levelname == 'ERROR':
                return True
            else:
                return False
        except:
            pass


class InfoFilter(logging.Filter):

    def filter(self, record):
        try:
            if record.levelname == 'INFO':
                return True
            else:
                return False
        except:
            pass