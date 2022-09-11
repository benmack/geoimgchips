import geopandas as gpd
import math
import pandas as pd
from shapely.geometry import Polygon
import utm


def s2_raster_aligned_chips_from_points(points, buffer, res):
    def utm_with_epsg_from_lat_lon(lat, lon):
        utm_info = utm.from_latlon(latitude=lat, longitude=lon)
        epsg = f"32{7 if lat < 0 else 6}{utm_info[2]}"
        return utm_info + (int(epsg),)

    utm_columns = ["easting", "northing", "zone_number", "zone_letter", "epsg"]
    assert ~points.columns.isin(utm_columns + ["minx", "miny", "maxx", "maxy"]).any()

    points = pd.concat(
        [
            points,
            points.apply(
                lambda x: pd.Series(
                    utm_with_epsg_from_lat_lon(x.latitude, x.longitude),
                    index=utm_columns,
                ),
                axis=1,
            ),
        ],
        axis=1,
    )

    chips = []
    for epsg, points_subset in points.groupby("epsg"):

        gdf = gpd.GeoDataFrame(
            points_subset,
            geometry=gpd.points_from_xy(points_subset.easting, points_subset.northing),
            crs=f"epsg:{epsg}",
        )
        polygons = gdf.buffer(buffer, cap_style=3)
        polygons_aligned = polygons.apply(
            lambda x: Polygon.from_bounds(
                *get_bbox_aligned_to_raster_res(x.bounds, res)
            )
        )

        gdf.geometry = polygons_aligned
        gdf[polygons_aligned.bounds.columns] = polygons_aligned.bounds
        gdf = gdf.to_crs("epsg:4326")

        chips.append(gdf)
    return gpd.GeoDataFrame(pd.concat(chips))


def get_bbox_aligned_to_raster_res(bbox, res=60):
    """From a bbox get a bbox aligned to the res and comprising the whole bbox.

    Assumes alignment/rounding to integers, e.g. 60m.

    Args:
        bbox (tuple): Bounding box (min x, min y, max x, max y), or in geogr. coord. terms (min lon, min lat, max lon, max lat)
        res (int, optional): Resolution to which to align to. Defaults to 60.

    Example:
        get_bbox_aligned_to_raster_res((684341.8722251394, 5335415.073570174, 686900.0993033936, 5337868.401629373), 60)
        > (684300, 5335380, 686940, 5337900)

        get_bbox_aligned_to_raster_res((684341.8722251394, 5335415.073570174, 686900.0993033936, 5337868.401629373), 20)
        > (684340, 5335400, 686920, 5337880)
    """
    # lower left => move further to lower left
    ll_x_aligned = int(
        res * math.floor(bbox[0] / res)
    )  # round to next lower int divisible by res
    ll_y_aligned = int(
        res * math.floor(bbox[1] / res)
    )  # round to next lower int divisible by res
    # upper right => move further to upper right
    ur_x_aligned = int(
        res * math.ceil(bbox[2] / res)
    )  # round to next higher int divisible by res
    ur_y_aligned = int(
        res * math.ceil(bbox[3] / res)
    )  # round to next higher int divisible by res
    return (ll_x_aligned, ll_y_aligned, ur_x_aligned, ur_y_aligned)
