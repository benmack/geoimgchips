import os
import geopandas as gpd

__all__ = ["available", "get_path"]

_module_path = os.path.dirname(__file__)

available = ["five_points.geojson"]


def get_path(dataset):
    """
    Get the path to a data file.

    Parameters
    ----------
    dataset : str
        The name of the dataset. See ``geopandas.datasets.available`` for
        all options.

    Examples
    --------
    >>> geoimgchips.datasets.get_path("five_points.geojson")
    '.../python3.8/site-packages/geopandas/datasets/five_points.geojson'
    """
    if dataset in available:

        path = os.path.abspath(os.path.join(_module_path, "data", dataset))
        assert os.path.exists(path), f"Path does not exist: {path}"
        return path
    else:
        msg = f"The dataset '{data}' is not available. "
        msg += f"Available datasets are {', '.join(available)}"
        raise ValueError(msg)


def get_dataset(dataset):
    return gpd.read_file(filename=get_path(dataset))
