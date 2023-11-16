from setuptools import setup, find_packages

setup(
    name='EchoReaper',
    version='0.2.11',
    url='https://github.com/ad3002/EchoReaper',
    author='Aleksey Komissarov',
    author_email='ad3002@gmail.com',
    description='A small library for scraping websites using proxy',
    packages=find_packages(),    
    install_requires=['selenium'],
)