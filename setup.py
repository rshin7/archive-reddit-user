from setuptools import setup, find_packages

setup(
    name="archive_reddit_user",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "praw",
        "tqdm",
        "cryptography"
    ],
    author="Richard Shin",
    author_email="webmaster@moogra.com",
    description="A tool to archive Reddit user comments",
    keywords="reddit archiver comments backup",
    url="https://github.com/rshin7/archive-reddit-user",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'console_scripts': [
            'archive-reddit-user=archive_reddit_user.main:main',
        ],
    },
)
