from isodata import *
import isodata
from isodata.base import FuelMix, ISOBase, GridStatus
import pandas as pd
import pytest

all_isos = [MISO(), CAISO(), PJM(), Ercot(), SPP(), NYISO(), ISONE()]


@pytest.mark.parametrize('iso', all_isos)
def test_get_latest_fuel_mix(iso):
    print(iso)
    mix = iso.get_latest_fuel_mix()
    assert isinstance(mix, FuelMix)
    assert isinstance(mix.time, pd.Timestamp)
    assert isinstance(mix.mix, pd.DataFrame)
    assert len(mix.mix) > 0
    assert mix.iso == iso.name
    assert isinstance(repr(mix), str)


def test_list_isos():
    assert len(isodata.list_isos()) == 7


def test_get_iso():
    for iso in isodata.list_isos()["Id"].values:
        assert issubclass(isodata.get_iso(iso), ISOBase)


def test_get_iso_invalid():
    with pytest.raises(Exception) as e_info:
        isodata.get_iso("ISO DOESNT EXIST")


@pytest.mark.parametrize('iso', [CAISO(), Ercot()])
def test_get_latest_status(iso):
    status = iso.get_latest_status()
    assert isinstance(status, GridStatus)


@pytest.mark.parametrize('iso', [CAISO(), Ercot(), ISONE()])
def test_latest_demand(iso):
    demand = iso.get_latest_demand()
    assert set(["time", "demand"]) == demand.keys()
    # todo check that there date is right


def test_latest_supply():
    iso = CAISO()
    demand = iso.get_latest_supply()

    assert set(["time", "supply"]) == demand.keys()

# @pytest.mark.parametrize('iso', all_isos)


def test_get_historical_fuel_mix():
    iso = CAISO()

    # date string works
    date_str = "20220322"
    df = iso.get_historical_fuel_mix(date_str)
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_str

    # timestamp object works
    date_obj = pd.to_datetime("2019/11/19")
    df = iso.get_historical_fuel_mix(date_obj)
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_obj.strftime('%Y%m%d')

    # datetime object works
    date_obj = pd.to_datetime("2021/05/09").date()
    df = iso.get_historical_fuel_mix(date_obj)
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_obj.strftime('%Y%m%d')


@pytest.mark.parametrize('iso', [CAISO(), ISONE()])
def test_get_historical_demand(iso):

    # date string works
    date_str = "20220322"
    df = iso.get_historical_demand(date_str)
    assert isinstance(df, pd.DataFrame)
    assert set(["Time", "Demand"]) == set(df.columns)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_str

    # timestamp object works
    date_obj = pd.to_datetime("2021/11/19")
    df = iso.get_historical_demand(date_obj)
    assert isinstance(df, pd.DataFrame)
    assert set(["Time", "Demand"]) == set(df.columns)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_obj.strftime('%Y%m%d')

    # datetime object works
    date_obj = pd.to_datetime("2021/05/09").date()
    df = iso.get_historical_demand(date_obj)
    assert isinstance(df, pd.DataFrame)
    assert set(["Time", "Demand"]) == set(df.columns)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_obj.strftime('%Y%m%d')


def test_get_historical_supply():
    iso = CAISO()

    # date string works
    # todo abstract the testing of all way to add dates
    date_str = "20220322"
    df = iso.get_historical_supply(date_str)
    assert isinstance(df, pd.DataFrame)
    assert set(["Time", "Supply"]) == set(df.columns)
    assert df.loc[0]["Time"].strftime('%Y%m%d') == date_str


@pytest.mark.parametrize('iso', [Ercot(), ISONE()])
def test_get_demand(iso):
    df = iso.get_demand_today()
    assert isinstance(df, pd.DataFrame)

    df = iso.get_demand_yesterday()
    assert isinstance(df, pd.DataFrame)

    demand = iso.get_latest_demand()
    set(["time", "demand"]) == demand.keys()