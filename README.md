# archive-reddit-user

This program allows a user to export their own comments (and others) and preserve the context surrounding the comment. The comments and the context surrounding the comment (if applicable) are saved in JSON format.

You can take it a step further and and create a hostable page to easily read and search through the comments.

## Installation and Usage

1. Install using pip: `pip install archive-reddit-user`.
2. Follow the setup wizard to create a `config.ini` file.
3. Run the command: `archive-reddit-user` in your Terminal.

## Arguments
* `--user`: specify a specific user to archive their comments.
* `--limit`: returns your rate usage (does uses one call).

## Coming Soon
* Testing
* `--nuke`: edit the comment and delete them.
* `--publish`: Create a page you can upload anywhere that provides a nice front-end to navigate
through the JSON-ified comments, with search!

## Is this safe?

When you first run `archive-reddit-user`, you're prompted to enter your client id, client secret (also known as an API key in other services), and credentials to your reddit account. These credentials are stored locally so you don't have to enter them everytime you run the program. You may wonder why it is in plaintext, I wrote something in the [wiki](https://github.com/rshin7/archive-reddit-user/wiki/Plaintext-Password) for more context.