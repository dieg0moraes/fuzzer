"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from re import sub, search
from utils import query_yes_no
from .settings import REGEX_WORD
from .exceptions import BuildError


class UrlBuilder:
    """Url building class"""
    def __init__(self, target_url, directory, word_range, ask, inject):
        self.target_url = target_url
        self.directory = directory
        self.start = word_range[0]
        self.end = word_range[1]
        self.ask = ask
        self.inject_by_default = inject
        self.urls = self.builder()


    def builder(self):
        self.main_url = self.find_inject()
        words = self.get_wordlist()
        urls = self.get_urls(words)
        if not urls:
            raise BuildError("No urls to build, check start and end parameters.")
        return urls


    def find_inject(self):
        """Look for injection."""
        insert_found = search(REGEX_WORD, self.target_url)
        if self.inject_by_default and not self.ask:
            url = self.target_url
        elif insert_found and self.ask:
            inject = query_yes_no('Custom injection found, continue? ', default=None)
            if not inject:
                url = sub(REGEX_WORD, "", self.target_url)
            else:
                url = self.target_url
        else:
            url = sub(REGEX_WORD, "", self.target_url)

        return url


    def get_wordlist(self):
        """Get words from dictionary."""
        with open(self.directory, 'r') as dictionary:
            words = []
            for index, word in enumerate(dictionary):
                if self.start <= index <= self.end:
                    words.append(word.strip())
                if index == self.end:
                    break
            return words


    def get_urls(self, words):
        """Get urls to test."""
        urls = []
        for word in words:
            url = self.build_url(word)
            urls.append(url)
        return urls


    def build_url(self, word):
        """Build urls using dictionary words."""
        if search(REGEX_WORD, self.main_url):
            url = sub(REGEX_WORD, word, self.main_url)
        else:
            url = self.main_url + word
        return url
