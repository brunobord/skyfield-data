# Changelog for Skyfield Data

## master (unreleased)

* Added ``expiration_limit`` argument for ``get_skyfield_data_path`` function. Enables to shift the expiration date limit by "n" days.

## 0.1.0 (2019-10-04)

### Library Runtime Enhancements

* Dropped compatibility with Python 3.3 and 3.4, as skyfield did.
* Generate a catalog of the expiration dates for files.
* Detect when a file has expired and raise a ``UserWarning``.

### Downloader Enhancements

* Added a ``--check-only`` argument to ``download.py`` to display the expiration dates of the files currently on disk.
* Enable computation of the expiration date of the BSP file(s) on disk (requires to install the local repository using the [dev] option / See README for more information).
* Warn user when there's a download error. Expiration date file won't be modified if at least one of the downloads has failed.

### Other Improvements

* Added basic tests for the ``get_skyfield_data_path`` function using `tox`.
* Added automated tests through Travis CI.
* Add Travis CI badge on README.
* Added a test to check if the current files are about to expire (45 days from now). Travis CI would run a monthly job and eventually report when it has failed, so actions can be done to refresh the files and "unbreak" the library.

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
