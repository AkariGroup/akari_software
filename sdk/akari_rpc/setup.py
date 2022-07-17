from setuptools import find_packages, setup

setup(
    name="akari-rpc",
    version="0.1.0",
    description="protobuf definitions and utility functions of Akari gRPC service",
    packages=find_packages(exclude=["tests"]),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akari_rpc": ["py.typed"]},
    install_requires=[
        "grpcio==1.44.0",
        "protobuf==3.19.3",
    ],
)
