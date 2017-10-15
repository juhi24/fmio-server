import threading
from os import path, remove, listdir, makedirs
from urllib import urlretrieve
from fmio import fmi


class DataMiner:
    def __init__(self, key, tempdir, stored_count=6):
        self.key = key
        self.stored_count = stored_count
        self.tempdir = tempdir
        self.counter = 0
        self.lock = threading.RLock()
        with self.lock:
            if not path.exists(self.tempdir):
                makedirs(self.tempdir)
            self.remove_all_files()

    def remove_all_files(self):
        with self.lock:
            for filename in self.filenames():
                remove(path.join(self.tempdir, filename))

    @property
    def radar_url(self):
        return fmi.gen_url(key=self.key)

    def generate_filename(self):
        with self.lock:
            self.counter += 1
            return "{}.tif".format(self.counter)

    def erase_extra_files(self):
        with self.lock:
            filenames = listdir(self.tempdir)
            filenames.sort(reverse=True)
            for filename in filenames[self.stored_count:]:
                remove(path.join(self.tempdir, filename))

    def fetch_radar_data(self):
        with self.lock:
            filepath = path.join(self.tempdir, self.generate_filename())
            urlretrieve(self.radar_url, filename=filepath)
            self.erase_extra_files()

    def filenames(self):
        """Returns names of the stored files sorted as newest to oldest"""
        with self.lock:
            filenames = listdir(self.tempdir)
            filenames.sort(reverse=True)
            return filenames
