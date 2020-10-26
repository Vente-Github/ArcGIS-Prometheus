import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="src-prometheus",
    version="0.0.1",
    author="Ignacio Lorenzo García",
    author_email="ilorgar@gesplan.es",
    description="Export metrics ArcGIS Rest Services to prometheus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cabildo-tf/vente/monitoring/arcgis-promtheus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)