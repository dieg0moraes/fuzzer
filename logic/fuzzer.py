"""
LICENCIA
"""
import asyncio  # FIXME: Pylint: unused-import
from utils import query_yes_no
from .client import Client


class Fuzzer:
    # TODO: Agregar docstring.

    def __init__(self, url, directory, logger):
        self.log = logger
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

    def get_wordlist(self):
        """Get words from dictionary."""
        dictionary = open(self.directory, 'r')
        words = []
        for word in dictionary:
            words.append(word.strip())
        dictionary.close()
        self.log.linfo(f'Number of words to test: {len(words)}')
        return words

    def get_urls(self, start, end):
        """Get urls to test."""
        urls = []
        words = self.get_wordlist()

        for word in words[start:end]:
            url = self.build_url(word)
            urls.append(url)

        return urls

    def build_url(self, word):
        """Build urls using dictionary words."""
        index = self.url.find('*')
        if index != -1:
            url = self.url[:index] + word + self.url[index+1:]
        else:
            url = self.url + word
        return url

    # TODO: ¿Para qué sirve esta función? Agregar docstring.
    async def fuzz(self, urls, workers):
        data = await self.get_results(urls, workers)
        return data

    # TODO: Agregar Docstring.
    async def get_results(self, urls, workers):
        client = Client(self.log)
        data = await client.get_data(urls, workers)
        return data
