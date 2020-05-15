import re
import json
import pymorphy2
import converter
import configparser

from collections import Counter
from os.path import join, exists
from nltk.tokenize import word_tokenize


class Analyzer:

    def __init__(self, raw, result):
        self.raw = raw
        self.result = result
        self.categories = []
        self.stops = ['PREP', 'CONJ', 'PRCL', 'INTJ', 'NUMR', 'COMP', 'NPRO']
        self.stop_words = []

    def read_stop_words(self, path):
        with open(path, 'r') as file:
            text = file.read()
            self.stop_words = text.split('\n')

    def get_categories(self):
        reader = converter.DirectoryReader(self.raw)
        self.categories = reader.scan()

    def save_result(self, result, category):
        file_path = join(self.result, category + '.json')
        with open(file_path, 'w') as file:
            json.dump(result, file)

    def analyze(self):
        self.get_categories()

        morph = pymorphy2.MorphAnalyzer()

        for category in self.categories:

            category_path = join(self.raw, category)
            iterator = 1
            analyze_over = False
            lemmas = []

            while not analyze_over:

                file_path = join(category_path, str(iterator) + '.json')

                if not exists(file_path):
                    analyze_over = True
                    break

                with open(file_path, 'r') as file:
                    text = file.read()
                    array = json.loads(text)

                for element in array:
                    element = re.sub('\W', ' ', element)
                    words = word_tokenize(element)

                    for word in words:
                        parse = morph.parse(word)
                        if parse[0].tag.POS not in self.stops:
                            normal_form = parse[0].normal_form
                            if normal_form not in self.stop_words:
                                lemmas.append(normal_form)

                iterator += 1

            self.save_result(Counter(lemmas).most_common(), category)


def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    raw_data = config['Converter']['raw_data']
    result_data = config['Analyzer']['result_data']
    stop_words = config['Analyzer']['stop_words']

    analyzer = Analyzer(raw_data, result_data)
    analyzer.read_stop_words(stop_words)
    analyzer.analyze()


if __name__ == '__main__':
    main()
