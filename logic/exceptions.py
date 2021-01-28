"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""

class ConfigError(Exception):
    """Bad fuzzer setup exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BuildError(Exception):
    """Problem building urls"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
