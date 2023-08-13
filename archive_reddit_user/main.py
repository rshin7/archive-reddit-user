import argparse
from archive_reddit_user.authenticator import RedditAuthenticator
from archive_reddit_user.config_manager import ConfigManager
from archive_reddit_user.rate_limits import RateLimits
from archive_reddit_user.reddit_archiver import RedditArchiver
from archive_reddit_user.html_publisher import HTMLPublisher

def initialize_argparse():
    parser = argparse.ArgumentParser(description='Archive a specific Reddit users comments.')
    parser.add_argument('--user', type=str, help='Specify a Reddit username to archive comments of another user.')
    parser.add_argument('--usage', action='store_true', help='Just fetch rate limit info without archiving.')
    parser.add_argument('--html', type=str, help='Create a local user interface to view and search through a directory containing archived comments.')
    return parser.parse_args()

def manage_configuration():
    config_manager = ConfigManager()
    if not config_manager.config_exists():
        user_config = config_manager.interactive_config_creation()
        config_manager.create_config_file(user_config)
        return False
    return True

def authenticate():
    authenticator = RedditAuthenticator()
    reddit = authenticator.authenticate()
    if reddit is None:
        print("Authentication failed. Exiting...")
        return None
    return reddit

def archive_user_data(reddit, user=None):
    archiver = RedditArchiver(reddit)
    user_info = archiver.fetch_user_info(user)
    archiver.save_user_info_to_json(user_info, user)
    archiver.fetch_and_save_comments(user)

def publish_html(directory):
    publisher = HTMLPublisher(directory)
    publisher.generate_html()

def main():
    args = initialize_argparse()

    if args.html:
        publish_html(args.publish)
        return

    if not manage_configuration():
        return

    reddit = authenticate()
    if reddit is None:
        return

    if args.usage:
        rate_limiter = RateLimits(reddit)
        rate_limiter.display_rate_limits()
        return

    archive_user_data(reddit, args.user)

if __name__ == "__main__":
    main()
