from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="archive_reddit_user",
    version="0.14",
    packages=find_packages(),
    install_requires=[
        "praw",
        "tqdm",
    ],
    author="Richard Shin",
    author_email="webmaster@moogra.com",
    description="A tool to archive Reddit user comments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="reddit, archiver, comments, backup",
    url="https://github.com/rshin7/archive-reddit-user",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'console_scripts': [
            'archive-reddit-user=archive_reddit_user.main:main',
        ],
    },
    project_urls={  
        "Bug Reports": "https://github.com/rshin7/archive-reddit-user/issues",
        "Source": "https://github.com/rshin7/archive-reddit-user/",
    },
)
