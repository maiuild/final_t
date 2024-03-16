import csv

class Model:
    def __init__(self):
        self.__filename = None
        self.__line = 0
        self.__header = []
        self.__data = []

    @property
    def filename(self):
        return self.__filename

    @property
    def header(self):
        return self.__header

    @property
    def data(self):
        return self.__data

    @filename.setter
    def filename(self, value):
        self.__filename = value

    def read_data(self):
        self.__header = []
        self.__data = []
        with open(self.__filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                self.__header = next(reader)
                for row in reader:
                    self.__data.append(row)
            except StopIteration:
                pass
            file.seek(0)
        return self.__header, self.__data

    # def close_file(self, file):
    #   if self.filename in locals() and not file.closed:
    #      file.close()
    # print("File closed.")

    @staticmethod
    def search_data(insert, data):
        search_results = []
        insert = insert.split(' ')
        # print(insert)
        for row in data:
            if all(any(word in value.lower() for value in row) for word in insert):
                search_results.append(row)
        return search_results
