# Changelog for Skyfield Data

## master (unreleased)

* Removed `deltat.data` & `deltat.preds` files from the archive. They're not used by Skyfield anymore, as of v1.31 (October 2020), since they were not updated by the providers. Skyfield now uses a builtin, the `iers.npz` file, embedded into the library.
* Adapted tests for warnings to point at the `Leap_Second.dat` file.
* Removed references to the `deltat.*` files in the docs and test files.

## 1.1.0 (2020-05-20)

### Python compatibility

* Added Python 3.8 compatibility (#1).
* Added Python 2.6 compatibility + circle-ci job, documentation amended, code fixed to be compatible with Python 2.6 (#6).
* Removed tox.ini reference to Python 3.3 builds.

### Minor changes

* Revamped/Simplified Travis configuration.

## 1.0.0 (2020-05-05)

### Data updates

**Data files were downloaded on 2020-05-05.**

* Updated ``deltat.data`` data file.
* Updated ``Leap_Second.dat`` data file.
* All expiration data items are up-to-date as of 2020-05-05.

### Library Runtime Enhancements

* Added ``expiration_limit`` argument for ``get_skyfield_data_path`` function. Enables to shift the expiration date limit by "n" days.

### Downloader enhancement

* USNO file serving host has changed. Pointing now at ``ftp://cddis.nasa.gov/products/iers/`` for ``deltat.*`` files.

### Minor changes

* Changes in Python ``setup.cfg`` classifiers.

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
