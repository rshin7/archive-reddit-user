import argparse

from archive_reddit_user.authenticator import RedditAuthenticator
from archive_reddit_user.config_manager import ConfigManager
from archive_reddit_user.reddit_archiver import RedditArchiver

def main():
    parser = argparse.ArgumentParser(description='Archive a specific Reddit users comments.')
    parser.add_argument('--user', type=str, help='Specify a Reddit username to archive comments of another user.')
    args = parser.parse_args()

    config_manager = ConfigManager()

    if not config_manager.config_exists():
        user_config = config_manager.interactive_config_creation()
        config_manager.create_config_file(user_config)
        return

    authenticator = RedditAuthenticator()
    reddit = authenticator.authenticate()

    if reddit is None:
        print("Authentication failed. Exiting...")
        return

    archiver = RedditArchiver(reddit)

    user_info = archiver.fetch_user_info(args.user if args.user else None)
    archiver.save_user_info_to_json(user_info, args.user if args.user else None)

    archiver.fetch_and_save_comments(args.user if args.user else None)


if __name__ == "__main__":
    main()
