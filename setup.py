
from setuptools import find_packages, setup


setup(
    name='twtitter_rumor_spreader',
    version='0.0.1',
    description='Collection of utilities to help with graph coloring problems',
    author='Didericis',
    author_email='eric@dideric.is',
    python_requires='>3.4',
    classifier=[
        'Intended Audience :: Mathematicians',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'tweepy==3.7.0',
        "Flask>=0.10.0"
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'twitter-rumors=twitter_rumor_spreader.cli:main',
        ]
    },
)
