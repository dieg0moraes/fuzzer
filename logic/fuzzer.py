import argparse
import asyncio
from .client import Client


class Fuzzer:


    def __init__(self, url, directory):
        if not url.endswith('/'):
            self.url = url + '/'
        else:
            self.url = url

        self.directory = directory

    def get_wordlist(self):
        f = open(self.directory, 'r')
        words = []
        for word in f:
            words.append(word.strip())


        print('Number of words in documents', len(words))
        return words

    def get_urls(self, sub):
        urls = []
        words = self.get_wordlist()
        if not sub:
            for word in words:
                urls.append(self.url + word)

        else:
            for word in words:
                if self.url.startswith('http://www.'):
                    url = self.url.replace('http://www.', 'http://' + word + '.')
                elif self.url.startswith('https://www.'):
                    url = self.url.replace('https://www.', 'https://' + word + '.')
                elif self.url.startswith('http://'):
                    url = self.url.replace('http://','http://' + word + '.')
                elif self.url.startswith('https://'):
                    url = self.url.replace('https://', 'https://' + word + '.')

                urls.append(url)

        return urls

    async def fuzz(self, sub, words, workers):
        urls = self.get_urls(sub)
        data = await self.get_results(urls, words, workers)
        return data



    async def get_results(self, urls, words, workers):
        client = Client()
        data = await client.get_data(urls, words, workers)
        return data
