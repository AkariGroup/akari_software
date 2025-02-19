from setuptools import find_packages, setup

setup(
    name="akira-controller-server",
    version="0.1.0",
    packages=find_packages(),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={
        "akira_controller_server": ["py.typed"],
    },
    install_requires=[
        "akari-proto>=0.4.0,<0.5.0",
        "blobconverter==1.4.1",
        "depthai==2.19.0.0",
        "fastapi==0.115.6",
        "grpcio==1.68.1",
        "numpy==1.23.4",
        "opencv-python-headless==4.7.0.72",
        "protobuf==5.29.2",
        "uvicorn==0.19.0",
    ],
    zip_safe=False,
)
