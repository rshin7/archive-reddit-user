from cryptography.fernet import Fernet
import configparser
import praw

class RedditAuthenticator:
    def __init__(self):
        self.config = configparser.ConfigParser()

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_password(key, password):
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(password.encode())

    @staticmethod
    def decrypt_password(key, encrypted_password):
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_password).decode()

    def authenticate(self):
        """Authenticate to the Reddit API."""
        self.config.read('config.ini')

        username = self.config['REDDIT']['Username']
        encrypted_password = self.config['REDDIT']['EncryptedPassword']
        key = self.config['REDDIT']['EncryptionKey']

        password = self.decrypt_password(key.encode(), encrypted_password.encode())
        client_id = self.config['REDDIT']['ClientID']
        client_secret = self.config['REDDIT']['ClientSecret']
        user_agent = self.config['REDDIT']['UserAgent']

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
