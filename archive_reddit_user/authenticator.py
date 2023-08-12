import hashlib
import configparser
import praw

class RedditAuthenticator:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def authenticate(self):
        """Authenticate to the Reddit API."""
        self.config.read('config.ini')

        username = self.config['REDDIT_AUTH']['username']
        password = self.config['REDDIT_AUTH']['password']
        client_id = self.config['REDDIT_AUTH']['client_id']
        client_secret = self.config['REDDIT_AUTH']['client_secret']
        user_agent = self.config['REDDIT_AUTH']['user_agent']

        reddit_instance = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )

        try:
            # Checking if authenticated by fetching the username
            user = reddit_instance.user.me()
            print(f"Authenticated as {user.name}")
            return reddit_instance
        except Exception as e:
            print("Authentication failed. Please check your credentials.")
            print(f"Error: {e}")
            return None
