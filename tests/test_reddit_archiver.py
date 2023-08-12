import pytest
from unittest.mock import MagicMock, patch
from archive_reddit_user.reddit_archiver import RedditArchiver

# Mocks for reddit objects
@pytest.fixture
def mock_redditor():
    redditor = MagicMock()
    redditor.name = 'test_redditor'
    redditor.comments.new.return_value = []
    return redditor

@pytest.fixture
def mock_reddit(mock_redditor):
    reddit = MagicMock()
    reddit.redditor.return_value = mock_redditor
    reddit.user.me.return_value = mock_redditor
    return reddit

@pytest.fixture
def archiver(mock_reddit):
    return RedditArchiver(mock_reddit)

def test_fetch_user_info(archiver):
    info = archiver.fetch_user_info()
    assert 'name' in info
    assert info['name'] == 'test_redditor'

def test_save_user_info_to_json(archiver):
    user_info = {'name': 'test_user'}
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        archiver.save_user_info_to_json(user_info)
        mock_open.assert_called_with('test_user.json', 'w', encoding='utf-8')

def test_get_parent_comment(archiver):
    mock_comment = MagicMock()
    mock_comment.id = "test_id"
    mock_comment.body = "test_body"
    mock_comment.created_utc = 12345
    mock_comment.permalink = "/r/test/test_id"
    mock_comment.ups = 100
    mock_comment.parent_id = "t3_test_parent"

    archiver.reddit.comment.return_value = mock_comment

    parent_data = archiver.get_parent_comment("test_id")
    assert 'id' in parent_data
    assert parent_data['id'] == 'test_id'

def test_save_comment_to_json(archiver):
    mock_comment = MagicMock()
    mock_comment.id = "test_comment_id"
    mock_comment.body = "test_body"
    mock_comment.created_utc = 12345
    mock_comment.permalink = "/r/test/test_comment_id"
    mock_comment.ups = 100
    mock_comment.parent_id = "t3_test_parent"
    mock_comment.subreddit.display_name = "test"
    mock_comment.submission.title = "test_title"
    mock_comment.all_awarded = [{"name": "award1", "description": "desc1"}]

    with patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('os.path.exists', return_value=False):
        archiver.save_comment_to_json(mock_comment, "./")
        mock_open.assert_called_with('./test_comment_id.json', 'w', encoding='utf-8')

def test_fetch_and_save_comments(archiver, mock_redditor):
    with patch('archive_reddit_user.reddit_archiver.RedditArchiver.save_comment_to_json') as mock_save:
        archiver.fetch_and_save_comments()
        mock_save.assert_not_called()  # In this mock setup, the user has no comments.

def test_fetch_and_save_comments_with_username(archiver, mock_redditor):
    with patch('archive_reddit_user.reddit_archiver.RedditArchiver.save_comment_to_json') as mock_save:
        archiver.fetch_and_save_comments(username="another_user")
        mock_save.assert_not_called()  # In this mock setup, the user has no comments.
