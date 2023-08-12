import os
import time
import json
import datetime
from tqdm import tqdm

class RedditArchiver:
    def __init__(self, reddit_instance):
        self.reddit = reddit_instance
        self.user = self.reddit.user.me()

    def fetch_user_info(self, username=None):
        if username:
            user = self.reddit.redditor(username)
        else:
            user = self.user

        trophies = [trophy.name for trophy in user.trophies()]
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

    def save_user_info_to_json(self, user_info, username=None):
        """Saves the user's account information to a JSON file named [username].json."""
        username_for_file = username if username else user_info['name']
        with open(f"{username_for_file}.json", "w", encoding="utf-8") as file:
            json.dump(user_info, file, ensure_ascii=False, indent=4)

    def get_parent_comment(self, comment_id):
        """Recursively fetch the parent comment and its ancestors."""
        parent_comment = self.reddit.comment(id=comment_id)
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
            data["parent_comment"] = self.get_parent_comment(parent_id)
        return data

    def save_comment_to_json(self, comment, comments_dir):
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
                comment_data["parent_comment"] = self.get_parent_comment(parent_id)

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(comment_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving comment {comment.id}: {e}")

    def fetch_and_save_comments(self, username=None):
        """Fetch and save comments of a user. If no username is provided, fetches comments of authenticated user."""
        if username:
            redditor = self.reddit.redditor(username)
            comments_list = list(redditor.comments.new(limit=None))
        else:
            comments_list = list(self.user.comments.new(limit=None))
            username = self.user.name

        comments_dir = f"{username}-comments"

        if not os.path.exists(comments_dir):
            os.makedirs(comments_dir)

        for comment in tqdm(comments_list, desc=f"Processing comments for {username}"):
            self.save_comment_to_json(comment, comments_dir)
            time.sleep(1.1)
