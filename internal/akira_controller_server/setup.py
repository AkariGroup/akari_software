from setuptools import find_packages, setup

setup(
    name="akira-controller-server",
    version="0.1.0",
    packages=find_packages(),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akira_controller_server": ["py.typed"]},
    install_requires=[
        "akari-proto>=0.1.0,<0.2.0",
        "fastapi>=0.60.0",
        "grpcio==1.44.0",
        "protobuf==3.19.3",
    ],
)
