from setuptools import setup, find_packages

setup(
    name="tasker",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "tasker = tasker.cli:run",
        ],
    },
)
