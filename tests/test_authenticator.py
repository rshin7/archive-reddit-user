import pytest
from unittest.mock import patch, Mock
from archive_reddit_user.authenticator import RedditAuthenticator
from io import StringIO
import sys

@pytest.fixture
def mock_config():
    with patch('archive_reddit_user.authenticator.configparser.ConfigParser') as MockConfig:
        mock = MockConfig.return_value
        mock.__getitem__.return_value = {
            'username': 'test_user',
            'password': 'test_password',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'user_agent': 'test_user_agent'
        }
        yield mock

@pytest.fixture
def mock_praw(mock_config):
    with patch('archive_reddit_user.authenticator.praw.Reddit') as MockReddit:
        mock_instance = MockReddit.return_value
        yield mock_instance

def test_successful_authentication(mock_praw):
    mock_user = Mock()
    mock_user.name = "test_user"
    mock_praw.user.me.return_value = mock_user

    authenticator = RedditAuthenticator()
    captured_output = StringIO()
    sys.stdout = captured_output
    reddit_instance = authenticator.authenticate()
    sys.stdout = sys.__stdout__

    assert reddit_instance == mock_praw
    assert "Authenticated as test_user" in captured_output.getvalue()

def test_failed_authentication(mock_praw):
    mock_praw.user.me.side_effect = Exception("Some error")

    authenticator = RedditAuthenticator()
    captured_output = StringIO()
    sys.stdout = captured_output
    reddit_instance = authenticator.authenticate()
    sys.stdout = sys.__stdout__

    assert reddit_instance is None
    assert "Authentication failed. Please check your credentials." in captured_output.getvalue()
