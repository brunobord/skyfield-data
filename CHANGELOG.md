# Changelog for Skyfield Data

## 0.0.1 (2019-07-29)

Initial release

* This project includes minimal data files required by the [Python Skyfield library](https://rhodesmill.org/skyfield/): `de421.bsp`, `deltat.data`, `deltat.preds` and `Leap_Second.dat`,
* It provides a small Python script to download the files from their respective source,
* This script eventually checks if some of the files are expired and skips them (by default),
* Usage documentation is included in the `README.md` file.
* This project code is released under the terms of the MIT License.
