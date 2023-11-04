from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Read requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

VERSION = "1.5.0"
DESCRIPTION = "Personality Types"
LONG_DESCRIPTION = "Standard python package for personality types"

setup(
    name="ptypes",
    version=VERSION,
    author="Fib",
    author_email="<Noah@psight.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license_files="LICENSE",
    packages=find_packages(),
    install_requires=requirements,
    url="https://github.com/Psight-Limited/ptypes",
    keywords=["python"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
