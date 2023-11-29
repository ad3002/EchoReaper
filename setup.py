from setuptools import setup, find_packages
import re

version = None
for line in open("./EchoReaper/__init__.py"):
    m = re.search("__version__\s*=\s*(.*)", line)
    if m:
        version = m.group(1).strip()[1:-1]  # quotes
        break
assert version

setup(
    name='EchoReaper',
    version=version,
    packages=["EchoReaper"],
    package_data={"": ["README.md"]},
    python_requires='>=3.6',
    include_package_data=True,
    scripts=[],
    license="BSD",
    url='https://github.com/ad3002/EchoReaper',
    author='Aleksey Komissarov',
    author_email='ad3002@gmail.com',
    description='A small library for scraping websites with or without proxy',
    install_requires=[
        'seleniumbase == 4.21.1', 
        'webdriver-manager == 4.0.1'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
