"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from utils import query_yes_no


class UrlBuilder:
    """Url building class"""
    def __init__(self, target_url, directory, start, end):
        self.target_url = target_url
        self.directory = directory
        # self.log = logger
        self.start = start
        self.end = end
        self.urls = self.builder()


    def builder(self):
        self.main_url = self.find_inject()
        words = self.get_wordlist()
        urls = self.get_urls(words)
        return urls


    def find_inject(self):
        """Look for injection."""
        insert_word = self.target_url.find('*')
        inject = False
        if insert_word != -1:
            inject = query_yes_no('* Custom injection found, continue? ')
            if not inject:
                index = self.target_url.find('*')
                url = self.target_url[:index] + self.target_url[index+1:]
            else:
                url = self.target_url
        else:
            url = self.target_url
        
        return url


    def get_wordlist(self):
        """Get words from dictionary."""
        with open(self.directory, 'r') as dictionary:
            words = []
            for index, word in enumerate(dictionary):
                if index >= self.start and index <= self.end:
                    words.append(word.strip())
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
        index = self.main_url.find('*')
        if index != -1:
            url = self.main_url[:index] + word + self.main_url[index+1:]
        else:
            url = self.main_url + word
        return url
