# Data files for Skyfield

[![Tests](https://github.com/brunobord/skyfield-data/actions/workflows/tests.yml/badge.svg)](https://github.com/brunobord/skyfield-data/actions/workflows/tests.yml)

## Rationale

[Skyfield](https://rhodesmill.org/skyfield/) is a Python library for astronomical computations. It depends on various data files to accurately compute moon phases, planet positions, etc.

Several issues are raised by these data files:

* If they're not found in the path of the ``Loader``, they're **downloaded at runtime**. Depending on the archive you're requesting, some files might be very large, causing a long delay (directly related to your network bandwidth). In the case of a web server app, you'd cause a timeout on client's end.
* They come mainly from 2 sources: NASA's JPL, and the IERS. **If one of them is temporarily unavailable**, you couldn't perform any computation.
* In some countries, or behind some filtering proxies, some hosts may be **blocked**.
* These files have **an expiration date** (in a more or less distant future). As a consequence, even if the files are already downloaded in the right path, at each runtime you could possibly have to download one or more files before making any computation using them.

### Currently known expiration dates

|      File       |    Date    |
|:---------------:|:----------:|
| finals2000A.all | 2024-06-16 |
|    de421.bsp    | 2053-10-08 |


**Deprecation warning**: As of ``python-skyfield>=1.31``, `Leap_Second.dat`, `deltat.data` and `deltat.preds` files are not used anymore. They were not maintained anymore, and Brandon Rhodes switched to other source files for ∆T computations.

## Goal for this project

* Providing at least the most common of these assets in Python Package.
* Make regular releases to refresh the files before they expire.
* Provide a warning / logging mechanism when the files are about to expire (or when they are outdated) to still allow you to compute things with the loaded assets, but being informed you need to upgrade.

This way, you could **install or upgrade** this data package via ``pip``.

Once all the files are on your disk space, you can instantiate your ``skyfield`` loader pointing at their path, without having to worry about anything.

## Usage

Install the packages using:

```sh
pip install skyfield skyfield-data
```

To create a custom Skyfield loader, use the following code:

```python
from skyfield_data import get_skyfield_data_path
from skyfield.api import Loader
load = Loader(get_skyfield_data_path())
planets = load('de421.bsp')  # this command won't download this file
ts = load.timescale(builtin=False)  # this command won't download the IERS file
```

For the record, using `buitin=True` as an argument to load the timescale data won't trigger the download of the file, because python-skyfield embeds its own data files as a built-in data source.

If you want to make sure that the data files would **never** be downloaded, you can also use the ``expire`` option like this:

```python
load = Loader(get_skyfield_data_path(), expire=False)
```

Whenever a file contained in the catalog has expired, you're going to receive a warning when loading the `skyfield-data` path:

```python
>>> from skyfield_data import get_skyfield_data_path
>>> from skyfield.api import Loader
>>> load = Loader(get_skyfield_data_path())
/home/[redacted]/skyfield_data/expirations.py:25: RuntimeWarning: The file de421.bsp has expired. Please upgrade your version of `skyfield-data` or expect computation errors
  RuntimeWarning
```

By default, the loading isn't blocked, but it's strongly recommended to upgrade to a more recent version, to make sure you're not going to make wrong astronomical computations.

### Custom limit

By default, the ``RuntimeWarning`` is raised when the file **has** expired. You may want to be aware of this warning **in advance**, that is to say a few days or weeks before, in order to eventually upgrade your version of ``skyfield-data``.

In order to trigger this warning, you can use the ``expiration_limit`` argument, like this:

```python
>>> from skyfield_data import get_skyfield_data_path
>>> from skyfield.api import Loader
>>> load = Loader(get_skyfield_data_path(expiration_limit=30))
/home/[redacted]/skyfield_data/expirations.py:25: RuntimeWarning: The file de421.bsp would expire in less than 30 days. Please upgrade your version of `skyfield-data` or expect computation errors
  RuntimeWarning
```

**Note:** The ``expiration_limit`` argument should be a positive integer (or zero).

## Developers

We assume that you'll be using a Python3.7+ version for all regular operations.

We're providing a ``Makefile`` with basic targets to play around with the toolkit. use ``make help`` to get more details.

In order to be able to run the `download.py` script, we recommend to run it **from a virtualenv** where you'd have installed the "dev" dependencies, using:

```sh
make install-dev
```

### Python compatibility

*Important:* This project is, and should stay compatible with Python 2.6, 2.7 and Python 3.7+ up to 3.11, to keep the same Python compatibility that `skyfield` has.

### Hacking

Improving or fixing `skyfield-data` will require you to have at least a virtualenv with `tox` installed on it.

We'll ask you to add tests along your patch, to make sure that no regression or bug would be introduced by your patch or further ones.

To make a quick'n'dirty test, inside your "tox-ready" virtualenv, run:

```sh
make test
```

to launch the Python 2.7 and Python 3.7+ test jobs.

If you want to test your branch against Python 2.6, you'll have to setup a Python 2.6-ready tox environment, by doing something similar to:

```sh
sudo apt install python2.6 python2.6-dev  # dev headers to compile numpy
mkvirtualenv TOX26 --python=`which python2.6`  # You will activate this venv with `workon TOX26`
pip install tox
tox -c tox-py26.ini
```

**Known issues**: on Ubuntu, you may be unable to build numpy at this point, due to misplaced C header files in your system. I've had hard times on Ubuntu, but your mileage may vary.

Note: At the moment, we can't prove that skyfield-data is 100% compatible with Python 2.6, because of a defunct CI. Although, we're pretty confident it is. Fingers crossed!

### Online CI with Travis & Circle-CI

The online CI relies on Github Actions:

[![Tests](https://github.com/brunobord/skyfield-data/actions/workflows/tests.yml/badge.svg)](https://github.com/brunobord/skyfield-data/actions/workflows/tests.yml)

## Copyright

### Data files

* `de421.bsp` is provided by the *Jet Propulsion Laboratory*,
* `finals2000A.all` is provided by the *International Earth Rotation and Reference Systems Service*.

### Software

This Python Package code is published under the terms of the MIT license. See the ``COPYING`` file for more details.
