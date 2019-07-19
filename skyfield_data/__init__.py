from os.path import dirname, join, abspath

__DATA_PATH = abspath(join(dirname(__file__), "data"))


def get_skyfield_data_path():
    """
    Return the data path to be used along with Skyfield loader.

    Example usage::

        from skyfield_data import get_skyfield_data_path
        from skyfield.api import Loader
        load = Loader(get_skyfield_data_path())
        planets = load('de421.bsp')
    """
    return __DATA_PATH


__all__ = [get_skyfield_data_path]
