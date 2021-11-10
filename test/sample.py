import json
class TestData:
    def __init__(self):
        self.__data = None
    def connect(self, data_file):
        with open(data_file) as json_file:
            self.__data = json.load(json_file)
    def get_data(self, name):
        for test in self.__data['tests']:
            if test['name'] == name:
                return test
    def close(self):
        pass