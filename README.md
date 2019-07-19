# Data files for Skyfield

[Skyfield](https://rhodesmill.org/skyfield/) is a Python library for astronomical computations. It depends on various data files to accurately compute moon phases, planet positions, etc.

Several issues are raised by these data files:

* If they're not found in the path of the ``Loader``, they're **downloaded at runtime**. Depending on the archive you're requesting, some files might be very large, causing a long delay (directly related to your network bandwidth). In the case of a web server app, you'd cause a timeout on client's end.
* They come mainly from 3 sources: the USNO (US Navy), Paris (Meudon) Observatory, and NASA JPL. **If one of them is temporarily unavailable**, you couldn't perform any computation.
* In some countries, or behind some filtering proxies, the USNO is considered as a military website, and thus is **blocked**.
* These files have **an expiration date** (in a more or less distant future). As a consequence, even if the files are already downloaded in the right path, at each runtime you could possibly have to download one or more files before making any computation using them.

## Goal for this project

* Providing at least the most common of these assets in Python Package.
* Make regular releases to refresh the files before they expire.
* Provide a warning / logging mechanism when the files are about to expire (or when they are outdated) to still allow you to compute things with the loaded assets, but being informed you need to upgrade.


This way, you could **install or upgrade** this data package via ``pip``.

Once all the files are on your disk space, you can instantiate your ``skyfield`` loader pointing at their path, without having to worry about anything.
