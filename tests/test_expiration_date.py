import pytest
import mock
from datetime import date, timedelta
from skyfield_data import get_skyfield_data_path
from skyfield_data.expiration_data import EXPIRATIONS
from skyfield_data.expirations import check_expirations


@mock.patch('skyfield_data.expirations.get_all')
def test_no_expiration(mocked_exp):
    mocked_exp.return_value = {}
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 0


def test_wrong_custom_expiration_limit_get_path():
    with pytest.raises(ValueError):
        get_skyfield_data_path(expiration_limit=-1)

    with pytest.raises(ValueError):
        get_skyfield_data_path(expiration_limit=None)

    with pytest.raises(ValueError):
        get_skyfield_data_path(expiration_limit="bad")


def test_wrong_custom_expiration_limit_check_expirations():
    with pytest.raises(ValueError):
        check_expirations(expiration_limit=-1)

    with pytest.raises(ValueError):
        check_expirations(expiration_limit=None)

    with pytest.raises(ValueError):
        check_expirations(expiration_limit="bad")


@mock.patch('skyfield_data.expirations.get_all')
def test_expiration_distant_future(mocked_exp):
    mocked_exp.return_value = {
        'de421.bsp': date.today() + timedelta(days=10000)
    }
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 0


@mock.patch('skyfield_data.expirations.get_all')
def test_expiration_yesterday(mocked_exp):
    mocked_exp.return_value = {
        'de421.bsp': date.today() - timedelta(days=1)
    }
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 1
    message = mocked_warn.call_args[0][0]
    assert "The file de421.bsp has expired." in message


@mock.patch('skyfield_data.expirations.get_all')
def test_expiration_custom_limit(mocked_exp):
    # It expires in 20 days
    mocked_exp.return_value = {
        'de421.bsp': date.today() + timedelta(days=20)
    }
    with mock.patch('warnings.warn') as mocked_warn:
        # Limit is 40 days, the limit is reached
        get_skyfield_data_path(expiration_limit=40)
    assert mocked_warn.call_count == 1
    message = mocked_warn.call_args[0][0]
    assert "The file de421.bsp would expire in less than 40 days." in message

    with mock.patch('warnings.warn') as mocked_warn:
        # Limit is 15 days, the limit is not reached
        get_skyfield_data_path(expiration_limit=15)
    assert mocked_warn.call_count == 0


@pytest.mark.skip("Momentary skip, because I need to fix the CI first")
def test_current_expiration_date():
    # Filter all files that would expire in 45 days
    # NOTE: this could be done using a dict comprehension, but this code has
    # to be kept Python 2.6-compatible.
    today = date.today()
    expired = EXPIRATIONS.items()
    expired = filter(lambda x: today >= x[1] - timedelta(days=45), expired)
    expired = list(expired)
    assert not expired, \
        "%d files(s) are about to expire: %s" % (len(expired), expired)
