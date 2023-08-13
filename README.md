# archive-reddit-user
<p align="center">
  <a href="https://github.com/rshin7/archive-reddit-user/actions/workflows/python-publish.yml"><img src="https://github.com/rshin7/archive-reddit-user/actions/workflows/python-publish.yml/badge.svg"></a>
</p>

This program allows a user to export their own (and others) comments and preserve the context surrounding the comment in JSON format for archiving purposes.

## Installation and Usage

1. Install using pip: `pip install archive-reddit-user`.
2. Follow the setup wizard to create a `config.ini` file.
3. Run the command: `archive-reddit-user` in your Terminal.

For a more detailed guide checkout this blog post.

## Arguments
* `--user <reddit_user>`: specify a specific user to archive their comments, no /u/ required.
    * `archive-reddit-user --user testusername`
* `--html <directory>`: create a page you can upload anywhere and evne run locally to look through comments.
    * `archive-reddit-user --html testusername-comments`
* `--usage`: returns your rate usage (does use one call).


## Is this safe?

When you first run `archive-reddit-user`, you're prompted to enter your client id, client secret (also known as an API key in other services), and credentials to your reddit account. These credentials are stored locally so you don't have to enter them everytime you run the program. You may wonder why it is in plaintext, I wrote something in the [wiki](https://github.com/rshin7/archive-reddit-user/wiki/Plaintext-Password) for more context.