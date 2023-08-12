from setuptools import setup, find_packages

setup(
    name="reddit_archive_user",
    version="0.1",
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
)
