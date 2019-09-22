import mock
from skyfield_data import get_skyfield_data_path
from skyfield.api import Loader


def test_load_no_cache(tmpdir):
    with mock.patch('jplephem.spk.SPK.open'):  # avoid naughty side-effects
        with mock.patch('skyfield.iokit.download') as download_patched:
            load = Loader(tmpdir.dirname)
            load('de421.bsp')
    assert download_patched.call_count == 1


@mock.patch('skyfield.iokit.download')
def test_load_using_cache(download_patched):
    load = Loader(get_skyfield_data_path())
    load('de421.bsp')
    assert download_patched.call_count == 0
