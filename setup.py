from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="hai",
    version="0.2",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "hai=hai.__main__:cli",
        ],
    },
)
