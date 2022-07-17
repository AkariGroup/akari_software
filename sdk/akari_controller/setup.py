from setuptools import find_packages, setup

setup(
    name="akari_controller",
    version="0.2.2",
    packages=find_packages(exclude=["tests"]),
    description="Akari controller by dynamixel_sdk. python package",
    long_description=open("README.md").read(),
    author="akari",
    author_email="akari.tmc@gmail.com",
    install_requires=["dynamixel_sdk"],
    package_data={"akari_controller": ["py.typed"]},
)
