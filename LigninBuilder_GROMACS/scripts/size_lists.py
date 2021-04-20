import glob
import json
import os
import subprocess
import sys

class WriteSizeLists:

    # def __init__(self, species, directory):


    def __call__(self, species, directory):

        self._species = species
        self._directory = directory

        dir_list = glob.glob(os.path.join(directory, '[0-9]*', ''))
        self._size_list = [dir.split(os.sep)[-2] for dir in dir_list]
        self._size_list = sorted(self._size_list, key=int)

        self._size_dict = self._get_size_dict()
        self._write_json()

    def _get_size_dict(self):

        size_dict = {}

        for size in self._size_list:
            file_list = glob.glob(os.path.join(self._directory, size, 'L*.pdb'))
            n_list = [os.path.split(file)[-1].replace('L', '').replace('.pdb', '') \
                      for file in file_list]
            n_list = sorted(n_list, key=int)
            size_dict[size] = n_list

        return size_dict

    def _write_json(self):

        with open(os.path.join(self._directory, 'size_lists.json'), 'w') as jf:
            json.dump(self._size_dict, jf, indent=4)

        with open('config.json', 'r') as jf:
            json_data = json.load(jf)

        if 'SIZE_LISTS' not in json_data:
            json_data['SIZE_LISTS'] = {}

        json_data['SIZE_LISTS'][self._species] = self._size_dict

        with open('config.json', 'w') as jf:
            json.dump(json_data, jf, indent=4)


if __name__ == '__main__':

    SPECIES = sys.argv[1]
    DIRECTORY = sys.argv[2]
    writer = WriteSizeLists()
    writer(SPECIES, DIRECTORY)
