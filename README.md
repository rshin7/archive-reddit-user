# reddit-archive-user

This program allows a user to export their own comments and preserve the context surrounding the comment. The comments and the context surrounding the comment (if applicable) are saved in JSON format.

You can use these JSON comments however you wish, if you'd like, you can host them on your Hugo blog to closely resemble your Reddit user page.


## Archiving Instructions

1. Install the pre-requisite packages: `pip install -r requirements.txt`
2. Create an .env file (see below)
3. Run the script: `python archive-comments.py`

## Host on Hugo Blog

1. Run the script: `python comments-to-hugo.py`

## Arguments
* `--nuke`: edit the comment and delete them.
* `--publish`: Create a page you can upload anywhere that provides a nice front-end to navigate
through the JSON-ified comments, with search!

## .env File

```
REDDIT_CLIENT_ID=
REDDIT_SECRET_KEY=
REDDIT_USER_AGENT=Reddit Comment Fetcher
REDDIT_USERNAME=
REDDIT_PASSWORD=
```