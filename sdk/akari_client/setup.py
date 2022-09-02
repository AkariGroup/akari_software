from setuptools import find_packages, setup

setup(
    name="akari-client",
    version="0.2.3",
    packages=find_packages(exclude=["tests"]),
    description="Akari Python package",
    long_description=open("README.md").read(),
    author="akari",
    author_email="akari.tmc@gmail.com",
    install_requires=[
        "dynamixel_sdk",
        "pydantic>=1.5,<2.0",
    ],
    package_data={"akari_client": ["py.typed"]},
    extras_require={
        "grpc": [
            "akari-proto>=0.1.0,<0.2.0",
            "grpcio==1.44.0",
            "protobuf==3.19.3",
        ],
    },
)
