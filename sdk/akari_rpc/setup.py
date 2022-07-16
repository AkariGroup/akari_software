from setuptools import find_packages, setup

setup(
    name="akari_rpc",
    version="0.1.0",
    description="gRPC client of Akari RPC service",
    packages=find_packages(exclude=["tests"]),
    author="akari",
    author_email="akari.tmc@gmail.com",
    package_data={"akari_rpc": ["py.typed"]},
)
