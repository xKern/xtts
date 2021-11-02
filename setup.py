from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = ('Simple python package to consume google TTS'
               ' and offers basic caching')
LONG_DESCRIPTION = Path('readme.md').read_text()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="xtts",
    version=VERSION,
    author="Haider Ali",
    author_email="neo@xkern.net",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['tts', 'google', 'caching', 'xkern'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ])
