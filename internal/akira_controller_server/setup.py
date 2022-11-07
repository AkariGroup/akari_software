from setuptools import find_packages, setup

setup(
    name="akira-controller-server",
    version="0.1.0",
    packages=find_packages(),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={
        "akira_controller_server": ["py.typed"],
        "": ["data/*.blob"],
    },
    install_requires=[
        "akari-proto>=0.1.0,<0.2.0",
        "depthai==2.19.0.0",
        "fastapi==0.86.0",
        "grpcio==1.44.0",
        "numpy==1.23.4",
        "opencv-python-headless==4.6.0.66",
        "protobuf==3.19.3",
        "uvicorn==0.19.0",
    ],
    zip_safe=False,
)
