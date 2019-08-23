# Changelog for Skyfield Data

## master (unreleased)

Nothing here yet.

## 0.0.2 (2019-08-23)

* Document the "Advanced" usage, with the ``expire`` option for the Loader.
* Ensure it's Python 2 compatible, since ``skyfield`` is compatible with Python 2.6/2.7.

## 0.0.1 (2019-07-29)

Initial release

* This project includes minimal data files required by the [Python Skyfield library](https://rhodesmill.org/skyfield/): `de421.bsp`, `deltat.data`, `deltat.preds` and `Leap_Second.dat`,
* It provides a small Python script to download the files from their respective source,
* This script eventually checks if some of the files are expired and skips them (by default),
* Usage documentation is included in the `README.md` file.
* This project code is released under the terms of the MIT License.
