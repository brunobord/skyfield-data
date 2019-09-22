import mock
from datetime import date
from datetime import timedelta
from skyfield_data import get_skyfield_data_path


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
