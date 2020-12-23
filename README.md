# Fuzzer

Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.

### Set up

- cd to Fuzzer directory.

- python3 -m pip install -r requirements.txt

### Usage

```
Usage: python3 main.py [args]

Arguments

(*) = Required

-h (--help)           Show help message and exit.

Basic arguments:

-u (--url) -> Url like http://www.example.com/ (*)
You may add an asterisk to inject the word in a specific place, like http://*.example.com/
By default it is http://www.example.com/*
Notice you should add the "/" at the end, or it will be http://www.example.com*

-d (--dir)            Path to dictionary wordlist. (*)

Performance options:

-w (--workers)        Number of workers (50 by default).
-s (--start)          Index of word to start in the dictionary (defaults to 0, the first word of the dictionary).
-e (--end)            Index of the last word of the dictionary to test (defaults to the last word of the dictionary).
-i (--interval)       Number of intervals to execute all the requests (*)
-t (--timeout)        Timeout for each request (Defaults to 3)

Connection options:
--tor                 Perform requests over the Tor network
--proxy               Custom proxy url

Log options:

--exceptions          Show exception and error messages
--rstatus             Show response http status code messages (200 status code is always logged)
--noinfo              Do not show info messages
--debug               Show debug messages
--logall              Log everything
--logfile             Log Output to app.log
--nocolors            Disable colored logs
```