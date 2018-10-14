#! /usr/bin/python3
# check a domain's Alexa rank via command line
# pass domain as argument with -d option
# usage:
# python alexa_check.py -d example_domain.com
import requests
import argparse
import re


class AlexaCheck:
    def __init__(self, domain):
        self.url = "https://www.alexa.com/siteinfo/"
        self.url += domain

    def __search_regex(self, regex, phrase):
        match = re.search(regex, phrase)
        if match:
            return match.group(1)

    def check(self):
        r = requests.get(self.url)
        page = str(r.text).split("\n")
        found_global = False
        for line in page:
            if "</strong>" in line and any(char.isdigit() for char in line):
                perspective = line.replace(',', '')
                found = self.__search_regex("(\d+)\s+<", perspective)
                if found and found[:1] != "0":
                    if not found_global:
                        found_global = True
                        yield ("global_rank", found)

            if "Flag" in line and "nbsp" in line:
                perspective = line.replace(',', '')
                country = self.__search_regex(".*\w+;(.*)</a>", perspective)
                country_rank = self.__search_regex(".*>(\d+)<", perspective)
                yield (country, country_rank)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter -d domain.com as argument')
    parser.add_argument('-d', '--domain', metavar='', required=True, help='Enter a domain: example.com')
    domain = vars(parser.parse_args())
    for rank_tuple in AlexaCheck(domain['domain']).check():
        print(rank_tuple)
