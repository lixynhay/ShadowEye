from setuptools import setup, find_packages

setup(
    name="shadoweye",
    version="3.1.0",
    description="Multi-Tool OSINT Framework for Termux",
    author="lixynhay",
    url="https://github.com/lixynhay/ShadowEye",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "httpx>=0.27.0",
        "requests>=2.31.0",
        "holehe>=1.0.0",
        "maigret>=0.4.0",
        "phonenumbers>=8.13.0",
        "python-whois>=0.9.0",
        "dnspython>=2.6.0",
        "exifread>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "shadoweye=cli:main",
        ],
    },
    python_requires=">=3.10",
)
