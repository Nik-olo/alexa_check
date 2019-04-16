# rootVIII
# Check a domain's Alexa rank via command line
# Pass a domain as an argument with the -d option
# Usage: python alexa_check.py -d example.com
#
from argparse import ArgumentParser
from re import search
from sys import version_info, exit
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import Request, urlopen


class AlexaCheck:
    def __init__(self, domain):
        self.url = "https://www.alexa.com/siteinfo/" + domain
        self.page = []

    @staticmethod
    def search_regex(regex, phrase):
        match = search(regex, phrase)
        if match:
            return match.group(1)
        return None

    def get(self):
        if version_info[0] != 2:
            r = urlopen(self.url)
            self.page = r.read().decode('utf-8').split("\n")
        else:
            req = Request(self.url)
            request = urlopen(req)
            self.page = request.read().split("\n")

    def check(self):
        try:
            self.get()
        except Exception as error:
            print(error)
            exit(1)
        found_global = False
        for line in self.page:
            if "</strong>" in line and any(char.isdigit() for char in line):
                perspective = line.replace(',', '')
                found = self.search_regex(r"(\d+)\s+<", perspective)
                if found and found[:1] != "0":
                    if not found_global:
                        found_global = True
                        yield ("global_rank", found)
            if "Flag" in line and "nbsp" in line:
                perspective = line.replace(',', '')
                country = self.search_regex(r".*\w+;(.*)</a>", perspective)
                country_rank = self.search_regex(r".*>(\d+)<", perspective)
                yield (country, country_rank)


if __name__ == "__main__":
    message = 'Usage: python alexa_check.py -d <domain.com>'
    h = '-d domain.com argument'
    parser = ArgumentParser(description=message)
    parser.add_argument('-d', '--domain', required=True, help=h)
    d = parser.parse_args()
    for rank_tuple in AlexaCheck(d.domain).check():
        print(rank_tuple)
