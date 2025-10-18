from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
requirements = fh.read().splitlines()

setup(
name="netspeed-cli",
version="0.1.0",
author="Elton John Kellum",
description="Cross-platform CLI Internet Speed Test Tool",
long_description=long_description,
long_description_content_type="text/markdown",
packages=find_packages(where="src"),
package_dir={"": "src"},
python_requires=">=3.8",
install_requires=requirements,
entry_points={
"console_scripts": [
"netspeed=netspeed.cli:main",
],
},
)
