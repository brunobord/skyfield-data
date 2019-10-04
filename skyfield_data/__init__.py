from os.path import dirname, join, abspath
from .expirations import check_expirations

__DATA_PATH = abspath(join(dirname(__file__), "data"))


def get_skyfield_data_path(expiration_limit=0):
    """
    Return the data path to be used along with Skyfield loader.

    Example usage::

        from skyfield_data import get_skyfield_data_path
        from skyfield.api import Loader
        load = Loader(get_skyfield_data_path())
        planets = load('de421.bsp')

    :param expiration_limit: Limit in days for expiration calculation.
                             Default is zero (only check for expired files)
    :type expiration_limit: int
    """
    check_expirations(expiration_limit)
    return __DATA_PATH


__all__ = [get_skyfield_data_path]
