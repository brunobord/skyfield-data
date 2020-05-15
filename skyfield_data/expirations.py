import warnings
from datetime import date, timedelta
from os.path import dirname, join, abspath
from os import listdir
from .expiration_data import EXPIRATIONS


__DATA_PATH = abspath(join(dirname(__file__), "data"))

# IMPORTANT NOTE: This module has to keep compatibility with Python 2.6
# That's the reason why it doesn't use ``format()`` to format strings, but the
# old ``%`` formatting.


def get_all():
    return EXPIRATIONS


def check_expirations(expiration_limit=0):
    """
    Check for expiration dates on each file in the catalog.

    :param expiration_limit: Limit in days for expiration calculation.
                             Default is zero (only check for expired files)
    :type expiration_limit: int
    """
    if not isinstance(expiration_limit, int) or expiration_limit < 0:
        raise ValueError(
            "Argument `expiration_limit` should be a positive integer"
        )

    expirations = get_all()
    files = listdir(__DATA_PATH)
    for filename in files:
        expiration_date = expirations.get(filename)
        if expiration_date:
            message = (
                "The file %s has expired."
                " Please upgrade your version of `skyfield-data` or expect"
                " computation errors") % filename
            if expiration_limit:
                expiration_date -= timedelta(days=expiration_limit)
                message = (
                    "The file %s would expire in less than %d days."
                    " Please upgrade your version of `skyfield-data` or expect"
                    " computation errors") % (filename, expiration_limit)

            if date.today() >= expiration_date:
                warnings.warn(message, RuntimeWarning)
