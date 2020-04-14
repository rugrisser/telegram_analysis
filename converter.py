import os
import json
import configparser

from os.path import join, isdir
from bs4 import BeautifulSoup


class DirectoryReader:

    def __init__(self, root):
        self.root = root

    def scan(self):
        return [tag for tag in os.listdir(self.root) if isdir(join(self.root, tag))]

    def count(self):
        return len(self.scan())


class Parser:

    def __init__(self, link):
        self.link = link

    def parse(self):
        result = []

        with open(self.link, 'r') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            elements = soup.select('div.text')
            elements.pop(0)

            for element in elements:
                result.append(element.text)

        return result


class Category:

    def __init__(self, root):
        self.root = root
        self.array = []

    def scan(self):
        self.array = []

        reader = DirectoryReader(self.root)
        for item in reader.scan():
            parser = Parser(join(self.root, item, 'messages.html'))
            self.array.append(parser.parse())

    def get_array(self):
        return self.array


class Library:

    def __init__(self, root):
        self.root = root
        self.array = dict()

    def create_category(self, name):
        self.array[name] = Category(join(self.root, name))

    def scan_categories(self):
        reader = DirectoryReader(self.root)
        for category in reader.scan():
            self.create_category(category)

    def parse_files(self):
        for name in self.array.keys():
            self.array[name].scan()

    def compile(self, filename):
        with open(filename, 'x') as file:
            file.write(json.dumps(self.array))


def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    root = config['Converter']['root']

    library = Library(root)
    library.scan_categories()
    library.parse_files()


if __name__ == '__main__':
    main()
