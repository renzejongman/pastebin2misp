import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pastebin2misp",
    version="1.0.0",
    author="Renze Jongman",
    author_email="info@renzejongman.nl",
    description="Pastebin2misp monitors for new pastes by your preferred authors, and automatically scrapes the IOCs, to add and publish them as an event in MISP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renzejongman/pastebin2misp",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
