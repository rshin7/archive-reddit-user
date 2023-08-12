import os
import time
import json
import praw
import datetime
import argparse
from tqdm import tqdm
from decouple import config

def authenticate_reddit_client():
    """Authenticate to the Reddit API."""

    client_id = config('REDDIT_CLIENT_ID')
    client_secret = config('REDDIT_SECRET_KEY')
    user_agent = config('REDDIT_USER_AGENT')
    username = config('REDDIT_USERNAME')
    password = config('REDDIT_PASSWORD')

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
    
def fetch_user_info(reddit_instance):
    user = reddit_instance.user.me()

    trophies = [trophy.name for trophy in reddit_instance.user.me().trophies()]
    user_info = {
        "name": user.name,
        "trophies": trophies,
        "post_karma": user.link_karma,
        "comment_karma": user.comment_karma,
        "cake_day": datetime.datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        "is_mod": user.is_mod,
        "is_gold": user.is_gold,
        "verified": user.verified,
        "has_verified_email": user.has_verified_email,
        "is_friend": user.is_friend,
        "subreddit": {
            "display_name": user.subreddit.display_name if user.subreddit else None,
            "title": user.subreddit.title if user.subreddit else None,
            "description": user.subreddit.public_description if user.subreddit else None,
            "subscribers": user.subreddit.subscribers if user.subreddit else None
        }
    }

    return user_info

def save_user_info_to_json(user_info, username=None):
    """Saves the user's account information to a JSON file named [username].json."""
    username_for_file = username if username else user_info['name']
    with open(f"{username_for_file}.json", "w", encoding="utf-8") as file:
        json.dump(user_info, file, ensure_ascii=False, indent=4)


    
def get_parent_comment(reddit_instance, comment_id):
    """Recursively fetch the parent comment and its ancestors."""
    parent_comment = reddit_instance.comment(id=comment_id)
    parent_comment.refresh()  # Ensure the comment data is fetched

    data = {
        "id": parent_comment.id,
        "body": parent_comment.body,
        "created_utc": parent_comment.created_utc,
        "permalink": parent_comment.permalink,
        "upvotes": parent_comment.ups
    }

    if parent_comment.parent_id.startswith('t1_'):
        parent_id = parent_comment.parent_id.split('_')[1]
        data["parent_comment"] = get_parent_comment(reddit_instance, parent_id)
    return data

def save_comment_to_json(reddit_instance, comment, comments_dir):
    """
    Save a comment to a JSON file named by its ID, maintaining comment hierarchy.
    """
    # Construct the file path
    file_path = os.path.join(comments_dir, f"{comment.id}.json")
    
    # If the comment's JSON file already exists, return (skip saving)
    if os.path.exists(file_path):
        return

    try:
        comment_data = {
            "id": comment.id,
            "body": comment.body,
            "created_utc": comment.created_utc,
            "subreddit": comment.subreddit.display_name,
            "permalink": comment.permalink,
            "post_title": comment.submission.title,
            "upvotes": comment.ups,
            "awards": [{"name": award['name'], "description": award['description']} for award in getattr(comment, 'all_awarded', [])]
        }

        if comment.parent_id.startswith('t1_'):
            parent_id = comment.parent_id.split('_')[1]
            comment_data["parent_comment"] = get_parent_comment(reddit_instance, parent_id)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(comment_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving comment {comment.id}: {e}")


def fetch_and_save_comments(reddit_instance, username=None):
    """Fetch and save comments of a user. If no username is provided, fetches comments of authenticated user."""
    if username:
        redditor = reddit_instance.redditor(username)
        comments_list = list(redditor.comments.new(limit=None))
    else:
        comments_list = list(reddit_instance.user.me().comments.new(limit=None))

    username_for_dir = username if username else reddit_instance.user.me().name
    comments_dir = f"{username_for_dir}-comments"

    if not os.path.exists(comments_dir):
        os.makedirs(comments_dir)

    for comment in tqdm(comments_list, desc=f"Processing comments for {username_for_dir}"):
        save_comment_to_json(reddit_instance, comment, comments_dir)
        # Introduce delay to respect Reddit's rate limits
        time.sleep(1.1)

def main():
    parser = argparse.ArgumentParser(description='Archive Reddit user comments.')
    parser.add_argument('--user', type=str, help='Specify a Reddit username to archive comments of another user.')
    args = parser.parse_args()

    reddit = authenticate_reddit_client()

    if reddit:
        if args.user:
            user_info = fetch_user_info(reddit)
            save_user_info_to_json(user_info)
            fetch_and_save_comments(reddit, args.user)
        else:
            user_info = fetch_user_info(reddit)
            save_user_info_to_json(user_info)
            fetch_and_save_comments(reddit)

if __name__ == "__main__":
    main()