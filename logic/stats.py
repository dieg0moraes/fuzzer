"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from datetime import datetime

class Stats:
    """Statistics for fuzzer requests."""

    def __init__(self):
        self.success = 0
        self.fail = 0
        self.exception = 0
        self.start_time = None
        self.end_time = None

    def isuccess(self):
        """Increment Success number."""
        self.success += 1

    def ifail(self):
        """Increment Fail number."""
        self.fail += 1

    def iexception(self):
        """Increment Exception number."""
        self.exception += 1

    def get_start_time(self):
        self.start_time = datetime.now()

    def get_end_time(self):
        self.end_time = datetime.now()
