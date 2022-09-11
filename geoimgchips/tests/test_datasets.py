import geoimgchips
import pytest


def test_import_dataset_five_points():
    assert "five_points.geojson" in geoimgchips.datasets.available


def test_import_dataset_five_points():
    gdf = geoimgchips.datasets.get_dataset("five_points.geojson")
    assert gdf.shape == (5, 3)
