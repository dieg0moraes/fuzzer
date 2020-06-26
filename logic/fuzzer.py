import argparse
import asyncio
from .client import Client
from utils import query_yes_no

class Fuzzer:


    def __init__(self, url, directory):
        insert_word = url.find('*')
        inject = False
        if insert_word != -1:
            inject = query_yes_no('* Custom injection found - or continue ')
            if not inject:
                index = url.find('*')
                self.url = url[:index] + url[index+1 :]
            else:
                self.url = url
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

    def get_urls(self, start, end):
        urls = []
        words = self.get_wordlist()

        for word in words[start:end]:
            url = self.build_url(word)
            urls.append(url)

        return urls

    def build_url(self, word):
        index = self.url.find('*')
        if index != -1:
            url = self.url[:index] + word + self.url[index+1:]
        else:
            url = self.url + word
        print(url)
        return url



    async def fuzz(self, urls, workers):
        data = await self.get_results(urls, workers)
        return data

    async def get_results(self, urls, workers):
        client = Client()
        data = await client.get_data(urls, workers)
        return data
