import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acrome-smd-python",
    version="0.1.0",
    author="Mehmet Bener",
    author_email="mehmet.bener@hisarschool.k12.tr",
    description="Python library for interfacing with the Acrome SMD Red hardware platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MehmetBener/acrome-lib",
    py_modules=["smd_gateway"],
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "pyserial>=3.0",
        "acrome-smd>=1.0",
        "tkinter"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
