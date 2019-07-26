# !/usr/bin/python3
import argparse
from datetime import date
from datetime import datetime, timedelta
from os.path import join, exists
import shutil
from urllib.request import urlopen

from skyfield_data import get_skyfield_data_path

JPL = "ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp"
USNO = "http://maia.usno.navy.mil/ser7"
IERS = "https://hpiers.obspm.fr/iers/bul/bulc"


def deltat_data_expiration(fileobj):
    """Return the expiration date for the USNO ``deltat.data`` file.

    Each line file gives the date and the value of Delta T::

        2016  2  1  68.1577
    """
    line = None
    for line in fileobj.readlines():
        pass
    # `line` is the last line
    if not line:  # No line, error...
        return
    array = line.strip().split()
    # We'll only keep the year / month / day
    array = array[:3]
    array = map(int, array)
    year, month, day = array
    # By convention, the file expires at year+1
    return date(year + 1, month, day)


def deltat_preds_expiration(fileobj):
    """
    Return the expiration date for the USNO ``deltat.preds`` file.

    The old format supplies a floating point year, the value of Delta T,
    and one or two other fields::

    2015.75      67.97               0.210         0.02

    The new format adds a modified Julian day as the first field:

    58484.000  2019.00   69.34      -0.152       0.117

    """
    lines = iter(fileobj)
    header = next(lines)

    if header.startswith(b'YEAR'):
        # Format in use until 2019 February
        next(lines)  # discard blank line
        line = next(lines)
        year_float = float(line.strip().split().pop())
    else:
        # Format in use since 2019 February
        line = next(lines)
        array = line.strip().split()
        year_float = float(array[1])

    year = int(year_float)
    month = 1 + int(year_float * 12.0) % 12
    expiration_date = date(year + 2, month, 1)
    return expiration_date


def leap_seconds_expiration(fileobj):
    """
    Return the expiration date for the IERS file ``Leap_Second.dat``.
    """
    lines = iter(fileobj)
    for line in lines:
        if line.startswith(b'#  File expires on'):
            break
    else:
        raise ValueError('Leap_Second.dat is missing its expiration date')
    line = line.decode('ascii')

    dt = datetime.strptime(line, '#  File expires on %d %B %Y\n')

    # The file went out of date at the beginning of July 2016, and kept
    # downloading every time a user ran a Skyfield program.  So we now
    # build in a grace period:
    grace_period = timedelta(days=30)
    expiration_date = dt.date() + grace_period
    return expiration_date


def download(url, target):
    "Download (binary) ``url`` and save it to ``target``."
    print("URL: {}".format(url))
    with urlopen(url) as response:
        with open(target, "wb") as fd:
            shutil.copyfileobj(response, fd)


def check_should_i_download(target, params):
    """
    Check if I should download the target file or not.
    """
    should_i_download = True
    reason = None

    if exists(target):
        # Search if the file has expired
        expiration_func = params.get("expiration_func")
        if expiration_func:
            with open(target, 'rb') as fd:
                expiration_date = expiration_func(fd)
            if date.today() <= expiration_date:
                should_i_download = False
                reason = 'file will expire at {}'.format(expiration_date)
            else:
                reason = "expiration date: {}".format(expiration_date)
        else:
            should_i_download = False
            reason = "file already exists, no expiration function"
    else:
        reason = "file not here"

    return should_i_download, reason


def main(args):
    items = {
        "de421.bsp": {"server": JPL},
        "deltat.data": {
            "server": USNO,
            "expiration_func": deltat_data_expiration
        },
        "deltat.preds": {
            "server": USNO,
            "expiration_func": deltat_preds_expiration
        },
        "Leap_Second.dat": {
            "server": IERS,
            "expiration_func": leap_seconds_expiration
        },
    }

    for filename, params in items.items():
        server = params["server"]
        url = "{}/{}".format(server, filename)
        target = join(get_skyfield_data_path(), filename)

        if args.force:
            should_i_download, reason = True, "Forced download"
        else:
            should_i_download, reason = check_should_i_download(
                target, params
            )

        if should_i_download:
            print("Downloading {} ({})".format(filename, reason))
            download(url, target)
        else:
            print("Skipping {} ({})".format(filename, reason))
    print("\nDone\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download Skyfield files")
    parser.add_argument(
        '--force', action="store_true", default=False,
        help="Force download, ignore expiration date or presence on disk."
    )
    args = parser.parse_args()
    main(args)
