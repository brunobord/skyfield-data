#!/usr/bin/python3
import shutil
from os.path import join, exists
from urllib.request import urlopen

from skyfield_data import get_skyfield_data_path

JPL = "ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp"
USNO = "http://maia.usno.navy.mil/ser7"
IERS = "https://hpiers.obspm.fr/iers/bul/bulc"

items = (
    ("de421.bsp", JPL),
    ("deltat.data", USNO),
    ("deltat.preds", USNO),
    ("Leap_Second.dat", IERS),
)


def download(url, target):
    "Download (binary) ``url`` and save it to ``target``."
    print("URL: {}".format(url))
    with urlopen(url) as response:
        with open(target, "wb") as fd:
            shutil.copyfileobj(response, fd)


if __name__ == '__main__':
    for filename, server in items:
        url = "{}/{}".format(server, filename)
        target = join(get_skyfield_data_path(), filename)

        if not exists(target):
            print("Downloading {}".format(filename))
            download(url, target)
        else:
            print("Skipping {}".format(filename))

    print("OK")
