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

    def __init__(self, path):
        self.path = path

    def parse(self):
        result = []
        iterator = 1
        parse_over = False

        while not parse_over:
            if iterator == 1:
                path = join(self.path, 'messages.html')
            else:
                path = join(self.path, 'messages' + str(iterator) + '.html')

            with open(path, 'r') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')

                elements = soup.select('div.body')

                for element in elements:
                    for child in element.contents:
                        try:
                            if 'text' in child['class']:
                                result.append(child.get_text().replace('\n', ' '))
                        except TypeError:
                            pass
                        except KeyError:
                            pass

                next_root = join(self.path, 'messages' + str(iterator + 1) + '.html')

                if len(soup.find_all('a', 'pagination', href=next_root)) == 0:
                    parse_over = True
                else:
                    iterator += 1

        return result


class Category:

    def __init__(self, root):
        self.root = root
        self.array = []

    def scan(self):
        self.array = []

        reader = DirectoryReader(self.root)
        for item in reader.scan():
            parser = Parser(join(self.root, item))
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

    def compile(self, path):
        for key in self.array.keys():
            root = join(path, key)

            try:
                os.mkdir(root)
            except OSError:
                pass

            array = self.array[key].get_array()
            for index in range(len(array)):
                with open(join(root, str(index + 1) + '.json'), 'w') as file:
                    json.dump(array[index], file)


def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    root = config['Converter']['root']
    raw_data = config['Converter']['raw_data']

    library = Library(root)
    library.scan_categories()
    library.parse_files()
    library.compile(raw_data)


if __name__ == '__main__':
    main()
