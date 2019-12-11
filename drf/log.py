import logging

class SpecialFilter(logging.Filter):
    def filter(self, record):
        return True