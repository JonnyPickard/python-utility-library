"""
Minimal setup.py for development installs.
"""

from setuptools import setup, find_packages

setup(
    name="python-utility-library",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "marker-pdf",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility library for PDF to Markdown conversion",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)