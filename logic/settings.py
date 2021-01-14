"""
Copyright (c) 2021 Diego Moraes. MIT license, see LICENSE file.
"""

# Logging success level number.
SUCCESS_LEVEL_NUM = 15

# Log file name.
LOG_FILE_NAME = "fuzzer.log"

# Log config defaults
LOG_DEFAULTS = {
    "info": True,
    "exceptions": True,
    "status": True,
    "debug": False,
    "file": False,
    "colors": True
}

# sys.exit() when logging a critical exception.
EXIT_ON_CRITICAL = True

# Default timeout for each request.
TIMEOUT = 3

# Default workers.
WORKERS = 50

# Injection word to look for.
# After changing this setting
# you should change the Fuzzer.get_urls.__doc__
REGEX_WORD = r"\[\*\]"

# Max percentage of success responses
# (total = success + fail)
# to detect a possible Virtual DOM.
VDOM_PERCENTAGE = 60
