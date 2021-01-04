"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""

class ConfigError(Exception):
    """Bad fuzzer setup exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
