# Changelog for Skyfield Data

## 6.0.0 (2024-06-23)

* Upgraded `finals2002A.all` file, which has expired, thanks @matrss for the bug report (#36).

## 5.0.0 (2023-04-23)

* Upgraded `finals2002A.all` file, which has expired. Thanks a lot to @ReimarBauer for the PR, and @thierry-FreeBSD for the bug report.
* Dropped support for Python 3.6.
* Confirm support for Python 3.11.

## 4.0.0 (2022-02-17)

* Switching from Travis/CircleCI for tests and CI to Github Actions (inspired by #24, thank you a lot, @Deuchnord).
* Dropped support for Python 3.5.
* Confirmed support for Python 3.10.
* **NOTE**: Temporarily skipped Python 2.6 tests. Since version 3.0.0, the runtime code hasn't been modified, so this means that it should still be compatible, although... We can't prove it.

### Data updates

**Data files were downloaded on 2022-12-15.**

* Upgrade `finals2000A.all` file, which has expired, thanks @6ruff for the bug report (#20).

## 3.0.0 (2020-12-18)

### Important changes

* Using `finals2000A.all` file for timescale computations (#14).
* Removed `Leap_Second.dat` file from the archive. They're not used by Skyfield anymore (#14).
* Adapted tests for warnings to point at the `de421.bsp` file (#14).
* Removed references to `Leap_Second.dat` from doc and test files (#14).
* Confirmed support of Python 3.9 (#15).

### Data updates

**Data files were downloaded on 2020-12-18.**

* Downloaded the `finals2000A.all` data file.


## 2.0.0 (2020-12-11)

### Important changes

* Removed `deltat.data` & `deltat.preds` files from the archive. They're not used by Skyfield anymore, as of v1.31 (October 2020), since they were not updated by the providers. Skyfield now uses a builtin, the `iers.npz` file, embedded into the library.
* Adapted tests for warnings to point at the `Leap_Second.dat` file.
* Removed references to the `deltat.*` files in the docs and test files.

### Data updates

**Data files were downloaded on 2020-12-11.**

* Updated the `Leap_Second.dat` data file.

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
