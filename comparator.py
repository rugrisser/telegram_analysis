import json
import converter
import configparser


from os.path import join


class GlobalDictionary:

    def __init__(self):
        self.dictionary = dict()
        self.categories_count = 0

    def count_categories(self, raw):
        reader = converter.DirectoryReader(raw)
        self.categories_count = len(reader.scan())

    def put_value(self, word, category, value):
        if word not in self.dictionary.keys():
            self.dictionary[word] = dict()
        self.dictionary[word][category] = value

    def squeeze(self):
        result = dict()

        for word in self.dictionary.keys():
            if len(self.dictionary[word]) == self.categories_count:
                result[word] = self.dictionary[word]

        return result


class Comparator:

    def __init__(self, rate, result, raw):
        self.rate = rate
        self.result = result
        self.raw = raw
        self.categories = []

    def save_result(self, result):
        file_path = join(self.result, 'result.json')
        with open(file_path, 'w') as file:
            json.dump(result, file)

    def get_categories(self):
        reader = converter.DirectoryReader(self.raw)
        self.categories = reader.scan()

    def compare(self):
        self.get_categories()

        global_dictionary = GlobalDictionary()
        global_dictionary.count_categories(self.raw)

        for category in self.categories:
            path = join(self.rate, category + '.json')
            with open(path, 'r') as file:
                text = file.read()
                rate_array = json.loads(text)

            for word in rate_array:
                global_dictionary.put_value(word[0], category, word[1])

        result = global_dictionary.squeeze()
        self.save_result(result)


def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    raw_data = config['Converter']['raw_data']
    rate_data = config['Rater']['result_data']
    result_path = config['Comparator']['root']

    comparator = Comparator(rate_data, result_path, raw_data)
    comparator.compare()


if __name__ == '__main__':
    main()
