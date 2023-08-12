# archive-reddit-user

This program allows a user to export their own comments (and others) and preserve the context surrounding the comment. The comments and the context surrounding the comment (if applicable) are saved in JSON format.

You can take it a step further and and create a hostable page to easily read and search through the comments.


## Installation and Usage

1. Install the pre-requisite packages: `pip install -r requirements.txt`
2. Follow the setup wizard to create a `config.ini` file
3. Run the command: `archive-reddit-user` in your Terminal.

## Arguments
* `--user`: specify a specific user to archive their comments.
* `--nuke`: edit the comment and delete them.
* `--publish`: Create a page you can upload anywhere that provides a nice front-end to navigate
through the JSON-ified comments, with search!