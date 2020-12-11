"""
Copyright (c) 2020 Diego Moraes. MIT license, see LICENSE file.
"""
from utils import query_yes_no
from .client import Client


class Fuzzer:

    def __init__(self, url, directory, logger, stats, timeout):
        self.log = logger
        self.stats = stats
        self.timeout = timeout

        insert_word = url.find('*')
        inject = False
        if insert_word != -1:
            inject = query_yes_no('* Custom injection found - or continue ')
            if not inject:
                index = url.find('*')
                self.url = url[:index] + url[index+1:]
            else:
                self.url = url
        else:
            self.url = url

        self.directory = directory

    def get_wordlist(self, start, end):
        """Get words from dictionary."""
        with open(self.directory, 'r') as dictionary:
            words = []
            for index, word in enumerate(dictionary):
                if index >= start and index <= end:
                    words.append(word.strip())
            return words

    def get_urls(self, start, end):
        """Get urls to test."""
        urls = []
        words = self.get_wordlist(start, end)

        for word in words:
            url = self.build_url(word)
            urls.append(url)
        self.log.linfo(f'Number of urls to test: {len(urls)}')
        return urls

    def build_url(self, word):
        """Build urls using dictionary words."""
        index = self.url.find('*')
        if index != -1:
            url = self.url[:index] + word + self.url[index+1:]
        else:
            url = self.url + word
        return url


    async def fuzz(self, urls, workers):
        data = await self.get_results(urls, workers)
        return data


    async def get_results(self, urls, workers):
        client = Client(self.log, self.stats)
        data = await client.get_data(urls, workers, self.timeout)
        return data
