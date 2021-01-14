"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from timeit import default_timer

class Stats:
    """Statistics for requests."""

    def __init__(self):
        self.success = 0
        self.fail = 0
        self.exception = 0

    def isuccess(self):
        """Increment Success number."""
        self.success += 1

    def ifail(self):
        """Increment Fail number."""
        self.fail += 1

    def iexception(self):
        """Increment Exception number."""
        self.exception += 1

    def start_rpm(self):
        """Start calculating requests per minute."""
        self.start_time = default_timer()

    def get_rpm(self):
        """Get RPM."""
        time = default_timer() - self.start_time
        # ...
