"""
This file is just to ensure local package installation.
"""

from setuptools import setup, find_packages

setup(
    name = 'Optimiser',  # Replace with your package name
    version = '0.1',
    packages =find_packages(),  # Automatically includes all folders with __init__.py
    install_requires = []  # Add any dependencies required by your local modules
)
