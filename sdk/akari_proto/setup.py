from setuptools import find_packages, setup

setup(
    name="akari-proto",
    version="0.3.1",
    description="Python package of akari protobuf definitions and utility functions",
    packages=find_packages(exclude=["tests"]),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akari_proto": ["py.typed"]},
    license="Apache License 2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
    url="https://github.com/AkariGroup/akari_software",
    install_requires=[
        "grpcio==1.44.0",
        "protobuf==3.19.3",
    ],
)
