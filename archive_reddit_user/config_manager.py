import os
import configparser
from getpass import getpass
from archive_reddit_user.authenticator import RedditAuthenticator

class ConfigManager:

    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.authenticator = RedditAuthenticator()

    def config_exists(self):
        """Check if the config.ini file exists."""
        return os.path.exists(self.config_file)

    def interactive_config_creation(self):
        """Guide the user through creating the config.ini file interactively."""
        client_id = input("Enter your Reddit client_id: ")
        client_secret = input("Enter your Reddit client_secret: ")
        user_agent = "Archive_Reddit_User"
        username = input("Enter your Reddit username: ")
        password = getpass("Enter your Reddit password: ")

        return {
            'client_id': client_id,
            'client_secret': client_secret,
            'user_agent': user_agent,
            'username': username,
            'password': password
        }

    def create_config_file(self, config_data=None):
        """Create a config.ini file with provided or default values."""
        config = configparser.ConfigParser()

        if not config_data:
            config_data = {
                'client_id': 'YOUR_CLIENT_ID_HERE',
                'client_secret': 'YOUR_CLIENT_SECRET_HERE',
                'user_agent': 'YOUR_USER_AGENT_HERE',
                'username': 'YOUR_USERNAME_HERE',
                'password': 'YOUR_PASSWORD_HERE',
            }

        config['REDDIT_AUTH'] = config_data

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

        # Inform the user about the path of the created file
        config_path = os.path.abspath(self.config_file)
        print(f"\nThe {self.config_file} file has been created at: {config_path}\n")
