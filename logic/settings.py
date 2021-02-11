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

# This should not be changed and must not be a positive number.
# Default value when --end is missing.
END_DEFAULT = -1

# Default timeout for each request.
TIMEOUT = 3
TOR_TIMEOUT = 10

# Default workers.
WORKERS = 50

# Injection word to look for.
# After changing this setting
# you should change the Fuzzer.get_urls docstring.
REGEX_WORD = r"\[\*\]"

# Max percentage of success responses
# (total = success + fail)
# to detect a possible Virtual DOM.
VDOM_PERCENTAGE = 60

# Request status code to save.
# Setting only the first number will
# save all the status codes with that number.
STATUS_TO_SAVE = [
    "1", "2", "3", "401", "403", "407", "410",
    "512"
]
