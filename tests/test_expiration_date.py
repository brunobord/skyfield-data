import mock
from datetime import date, timedelta
from skyfield_data import get_skyfield_data_path
from skyfield_data.expiration_data import EXPIRATIONS


@mock.patch('skyfield_data.expirations.get_all')
def test_no_expiration(mocked_exp):
    mocked_exp.return_value = {}
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 0


@mock.patch('skyfield_data.expirations.get_all')
def test_expiration_deltat_distant_future(mocked_exp):
    mocked_exp.return_value = {
        'deltat.data': date.today() + timedelta(days=10000)
    }
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 0


@mock.patch('skyfield_data.expirations.get_all')
def test_expiration_deltat_yesterday(mocked_exp):
    mocked_exp.return_value = {
        'deltat.data': date.today() - timedelta(days=1)
    }
    with mock.patch('warnings.warn') as mocked_warn:
        get_skyfield_data_path()
    assert mocked_warn.call_count == 1


def test_current_expiration_date():
    # Filter all files that would expire in 45 days
    expired = {
        k: v for k, v in EXPIRATIONS.items()
        if date.today() >= v - timedelta(days=45)
    }
    assert not expired, \
        "{} files(s) are about to expire: {}".format(len(expired), expired)
