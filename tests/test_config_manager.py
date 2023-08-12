import pytest
from unittest.mock import patch, mock_open
from archive_reddit_user.config_manager import ConfigManager

def test_config_exists():
    with patch('os.path.exists', return_value=True):
        config_manager = ConfigManager()
        assert config_manager.config_exists() == True

    with patch('os.path.exists', return_value=False):
        config_manager = ConfigManager()
        assert config_manager.config_exists() == False

@patch('archive_reddit_user.config_manager.input', side_effect=['client_id_test', 'client_secret_test', 'test_username'])
@patch('archive_reddit_user.config_manager.getpass', return_value='password_test')
def test_interactive_config_creation(mocked_input, mocked_getpass):
    config_manager = ConfigManager()
    config_data = config_manager.interactive_config_creation()

    expected_data = {
        'client_id': 'client_id_test',
        'client_secret': 'client_secret_test',
        'user_agent': 'Archive_Reddit_User',
        'username': 'test_username',
        'password': 'password_test'
    }
    assert config_data == expected_data

@patch('archive_reddit_user.config_manager.os.path.abspath', return_value='/absolute/path/to/config.ini')
@patch("archive_reddit_user.config_manager.open", new_callable=mock_open)
def test_create_config_file(mocked_open_func, mocked_abspath):
    config_manager = ConfigManager()

    # Providing config data
    config_data = {
        'client_id': 'client_id_test',
        'client_secret': 'client_secret_test',
        'user_agent': 'user_agent_test',
        'username': 'username_test',
        'password': 'password_test'
    }
    config_manager.create_config_file(config_data=config_data)

    # Ensure the file was "opened" for writing
    mocked_open_func.assert_called_once_with('config.ini', 'w')

    # If no data is provided, default values should be used
    config_manager.create_config_file()
    expected_default = {
        'client_id': 'YOUR_CLIENT_ID_HERE',
        'client_secret': 'YOUR_CLIENT_SECRET_HERE',
        'user_agent': 'YOUR_USER_AGENT_HERE',
        'username': 'YOUR_USERNAME_HERE',
        'password': 'YOUR_PASSWORD_HERE'
    }

    handle = mocked_open_func()
    handle.write.assert_called()

