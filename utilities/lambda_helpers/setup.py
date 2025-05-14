from setuptools import setup, find_packages
from os import getcwd, path

utils = path.dirname(getcwd())

setup(
    name="tpds_lambda_helpers",
    version="1.1.6",
    packages=find_packages(),
    install_requires=[
        f"tpds_logger @ file://localhost{utils}/logger",
        f"tpds_config @ file://localhost{utils}/config",
        f"tpds_env_var @ file://localhost{utils}/env_var",
    ]
)