import glob
import os
import subprocess
import sys

class SortBySize:

    def __init__(self, indir):

        self._indir = indir

    def __call__(self):

        self._file_list = glob.glob(os.path.join(self._indir, '*.pdb'))
        self._nres = self._get_num_resids()
        self._create_links()

    def _get_num_resids(self):

        nres = []
        for file in self._file_list:
            str_in = "tail -2 " + file + " | head -1"
            line = subprocess.check_output(str_in, shell=True).decode().split()
            if line[3] == 'GUAIL':
                nres.append(int(line[4]))
            else:
                nres.append(int(line[5]))

        return nres

    def _create_links(self):

        for ifile, file in enumerate(self._file_list):

            nres = str(self._nres[ifile])

            directory = os.path.join(self._indir, nres)
            if not os.path.exists(directory):
                os.mkdir(directory)

            for file1 in [file, file.replace('.pdb', '.psf')]:
                file_name = os.path.split(file1)[1]
                str_in = 'ln -s -n ' + os.path.join('..', file_name) + ' ' + directory
                subprocess.call(str_in.split())

if __name__ == '__main__':

    INDIR = sys.argv[1]
    sorter = SortBySize(INDIR)
    sorter()
