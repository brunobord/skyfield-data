# !/usr/bin/python3
import argparse
from datetime import date
from os.path import join, exists, abspath, dirname, basename
import shutil
from urllib.request import urlopen
from jplephem.spk import DAF, SPK
from colorama import init
from termcolor import colored

init()

JPL = "ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp"

__DATA_PATH = abspath(join(dirname(__file__), "skyfield_data", "data"))


def calendar_date(jd_integer):
    """Convert Julian Day `jd_integer` into a Gregorian (year, month, day)."""

    k = jd_integer + 68569
    n = 4 * k // 146097

    k = k - (146097 * n + 3) // 4
    m = 4000 * (k + 1) // 1461001
    k = k - 1461 * m // 4 + 31
    month = 80 * k // 2447
    day = k - 2447 * month // 80
    k = month // 11

    month = month + 2 - 12 * k
    year = 100 * (n - 49) + m + k

    return date(int(year), int(month), int(day))


def bsp_expiration(fileobj):
    """
    Return the expiration date for a .bsp file.
    """
    daf_object = DAF(fileobj)
    spk_object = SPK(daf_object)
    dates = [segment.end_jd for segment in spk_object.segments]
    # We take the closest end date, to expire the file as soon as it's obsolete
    end_jd = min(dates)
    return calendar_date(end_jd)


def download(url, target):
    "Download (binary) ``url`` and save it to ``target``."
    print("URL: {}".format(url))
    try:
        with urlopen(url) as response:
            with open(target, "wb") as fd:
                shutil.copyfileobj(response, fd)
        return True
    except Exception as exc:
        msg = "*** Error: {} couldn't be downloaded ({})".format(
            basename(target), exc
        )
        print(colored(msg, 'red'))
    return False


def get_expiration_date(target, params):
    """
    Return expiration date for the given ``target``.
    """
    expiration_date = None
    if exists(target):
        expiration_func = params.get("expiration_func")
        if expiration_func:
            with open(target, 'rb') as fd:
                expiration_date = expiration_func(fd)
    return expiration_date


def check_should_i_download(target, params):
    """
    Check if I should download the target file or not.
    """
    should_i_download = True
    reason = None

    if exists(target):
        # Search if the file has expired
        expiration_date = get_expiration_date(target, params)
        if expiration_date:
            if date.today() <= expiration_date:
                should_i_download = False
                reason = 'file will expire at {}'.format(expiration_date)
            else:
                reason = "expiration date: {}".format(expiration_date)
        else:
            should_i_download = False
            reason = "file already exists, no expiration function/date"
    else:
        reason = "file not here"

    return should_i_download, reason


def main(args):
    items = {
        "de421.bsp": {
            "server": JPL,
            "expiration_func": bsp_expiration,
        },
    }
    # For expiration date content
    target_expiration = abspath(
        join(__DATA_PATH, '..', 'expiration_data.py')
    )
    success = True
    expiration_dates = {}

    for filename, params in items.items():
        server = params["server"]
        url = "{}/{}".format(server, filename)
        target = join(__DATA_PATH, filename)

        expiration_date = get_expiration_date(target, params)
        expiration_dates[filename] = expiration_date

        if args.check_only:
            print(
                "File: {} => expiration: {}".format(
                    filename, expiration_date or "`unknown`"
                )
            )
            continue
        elif args.force:
            should_i_download, reason = True, "Forced download"
        else:
            should_i_download, reason = check_should_i_download(
                target, params
            )

        if should_i_download:
            print("Downloading {} ({})".format(filename, reason))
            success = download(url, target) and success
        else:
            print("Skipping {} ({})".format(filename, reason))

    # Generating the expiration date file.
    if success:  # only in case of a success
        expiration_template = """import datetime

EXPIRATIONS = {}
"""
        with open(target_expiration, 'w') as fd:
            fd.write(expiration_template.format(expiration_dates))
    else:
        print("** Skipped expiration generation: failed to download.")
    print("\nDone\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download Skyfield files")
    parser.add_argument(
        '--force', action="store_true", default=False,
        help="Force download, ignore expiration date or presence on disk."
    )
    parser.add_argument(
        "--check-only", action="store_true", default=False,
        help="Check only the expiration dates of the files on disk."
    )
    args = parser.parse_args()
    main(args)
