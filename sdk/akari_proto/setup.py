from setuptools import find_packages, setup

setup(
    name="akari-proto",
    version="0.1.0",
    description="Python package of akari protobuf definitions and utility functions",
    packages=find_packages(exclude=["tests"]),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akari_proto": ["py.typed"]},
    install_requires=[
        "grpcio==1.44.0",
        "protobuf==3.19.3",
    ],
)
