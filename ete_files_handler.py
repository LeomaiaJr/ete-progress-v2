import json


class ETEFilesHandler:
    def __init__(self):
        pass

    @staticmethod
    def read_file_data(path):
        with open(mode='r', file=path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def write_file_data(path, data):
        with open(mode='w', file=path) as json_file:
            json_file.write(json.dumps(data, indent=2, ensure_ascii=False))
