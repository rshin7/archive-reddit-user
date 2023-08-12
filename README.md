# archive-reddit-user-comments

This script allows a user to export their own comments and preserve the context surrounding the comment. The comments and the context surrounding the comment (if applicable) are saved in JSON format.

You can use these JSON comments however you wish, if you'd like, you can host them on your Hugo blog to closely resemble your Reddit user page.


## Archiving Instructions

1. Install the pre-requisite packages: `pip install -r requirements.txt`
2. Create an .env file (see below)
3. Run the script: `python archive-comments.py`

## Host on Hugo Blog

1. Run the script: `python comments-to-hugo.py`

## Nuke (Optional)

You can pass in the `--nuke` flag to edit your comment and delete them with this script. 

## .env File

```
REDDIT_CLIENT_ID=
REDDIT_SECRET_KEY=
REDDIT_USER_AGENT=Reddit Comment Fetcher
REDDIT_USERNAME=
REDDIT_PASSWORD=
```