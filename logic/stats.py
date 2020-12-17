"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""

class Stats:
    """Statistics for the status of the requests"""

    def __init__(self):
        self.success = 0
        self.fail = 0
        self.exception = 0

    def isuccess(self):
        """Increment Success number"""
        self.success += 1

    def ifail(self):
        """Increment Fail number."""
        self.fail += 1

    def iexception(self):
        """Increment Exception number."""
        self.exception += 1
