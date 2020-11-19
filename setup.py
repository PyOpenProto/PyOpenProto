# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import pyaudio_protocol

long_description = """
PyAudio_protocol is a simple module to read audio files and send triggers
(via parallel port for now) based on a pandas list of stimulation.
The aim is to be used in research experiments.
"""

setup(
    name = "pyaudio_protocol",
    version = pyaudio_protocol.__version__,
    packages = [pkg for pkg in find_packages() if pkg.startswith('pyaudio_protocol')],
    install_requires=[
                    'numpy',
                    'pandas',
                    'sounddevice',
                    'pyparallel',
                    'pandas'
                    #'portaudio',
                    #'QtCore', #For core_gui.py - recular computer
                    #Rpi.GPIO # For core_rpi_nogui - Stimulation box
                    ],
    author = "Anonymous", #for review
    author_email = "Anonymous", #for review
    description = "Simple module for playing audio research protocol.",
    long_description = long_description,
    license = "BSD",
    #url=' ', #for review
    classifiers = [
        'Development Status :: 1 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering']
)
