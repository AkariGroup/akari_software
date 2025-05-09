from setuptools import find_packages, setup

setup(
    name="akari-client",
    version="0.4.2",
    packages=find_packages(exclude=["tests"]),
    description="Akari Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="akari",
    author_email="akari.tmc@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
    url="https://github.com/AkariGroup/akari_software",
    install_requires=[
        "feetech-servo-sdk",
        "dynamixel_sdk",
        "pydantic>=2.0,<3.0",
        "pydantic-settings>=2.0,<3.0",
        "numpy==1.26.4",
    ],
    package_data={"akari_client": ["py.typed"]},
    extras_require={
        "grpc": [
            "akari-proto>=0.4.0,<0.5.0",
            "grpcio==1.68.1",
            "protobuf==5.29.2",
        ],
        "depthai": [
            "matplotlib",
            "depthai",
            "opencv-python",
            "blobconverter",
        ],
    },
)
