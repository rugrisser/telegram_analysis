import json
import converter
import configparser

from os.path import join


class RateConverter:

    def __init__(self, frequencies, rate, raw):
        self.frequencies = frequencies
        self.rate = rate
        self.raw = raw
        self.total = {}
        self.categories = []

    def save_result(self, result, category):
        file_path = join(self.rate, category + '.json')
        with open(file_path, 'w') as file:
            json.dump(result, file)

    def get_categories(self):
        reader = converter.DirectoryReader(self.raw)
        self.categories = reader.scan()

    def count_total(self):
        self.get_categories()

        for category in self.categories:
            self.total[category] = 0
            path = join(self.frequencies, category + '.json')
            with open(path, 'r') as file:
                frequency_array = json.load(file)

            for word in frequency_array:
                self.total[category] += word[1]

    def process_rate(self):
        self.count_total()

        for category in self.categories:
            path = join(self.frequencies, category + '.json')
            with open(path, 'r') as file:
                text = file.read()
                frequencies_array = json.loads(text)

            for word in range(len(frequencies_array)):
                frequencies_array[word][1] /= self.total[category]

            self.save_result(frequencies_array, category)



def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    raw_data = config['Converter']['raw_data']
    frequencies_data = config['Analyzer']['result_data']
    rate_data = config['Rater']['result_data']

    rate_converter = RateConverter(frequencies_data, rate_data, raw_data)
    rate_converter.process_rate()


if __name__ == '__main__':
    main()
