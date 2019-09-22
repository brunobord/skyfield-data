import warnings
from datetime import date
from os.path import dirname, join, abspath
from os import listdir
from .expiration_data import EXPIRATIONS


__DATA_PATH = abspath(join(dirname(__file__), "data"))


def get_all():
    return EXPIRATIONS


def check_expirations():
    expirations = get_all()
    files = listdir(__DATA_PATH)
    for filename in files:
        expiration_date = expirations.get(filename)
        if expiration_date and date.today() >= expiration_date:
            warnings.warn(
                ("The file {} has expired."
                 " Please upgrade your version of `skyfield-data` or expect"
                 " computation errors").format(filename),
                RuntimeWarning
            )
