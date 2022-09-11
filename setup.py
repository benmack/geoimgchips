from setuptools import setup, find_packages

setup(
    name="geoimgchips",
    version="0.1.1",
    packages=find_packages(
        include=["geoimgchips", "geoimgchips.datasets", "geoimgchips.utils"]
    ),
    install_requires=[
        "geopandas",
        "pandas",
        "shapely",
        "utm",
    ],
    package_data={
        "geoimgchips": ["data/*.geojson"],
    },
)
