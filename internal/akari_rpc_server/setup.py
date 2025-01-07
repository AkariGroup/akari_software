from setuptools import find_packages, setup

setup(
    name="akari-rpc-server",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akari_rpc_server": ["py.typed"]},
    install_requires=[
        "akari-proto>=0.4.0,<0.5.0",
        "grpcio==1.68.1",
        "protobuf==5.29.2",
    ],
)
