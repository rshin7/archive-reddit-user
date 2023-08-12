import os
import re
import json
from datetime import datetime

def unix_to_rfc3339(unix_timestamp):
    dt_object = datetime.utcfromtimestamp(unix_timestamp)
    return dt_object.strftime('%Y-%m-%dT%H:%M:%S%z')

def extract_parent_comment_chain(json_data):
    """Extracts and formats a comment and its parent chain"""
    comment_chain = []

    # Extract the initial comment
    comment_chain.append({
        'body': json_data['body'],
        'id': json_data['id'],
        'upvotes': json_data['upvotes']
    })

    # Extract parent comments
    parent_data = json_data.get('parent_comment')
    while parent_data:
        comment_chain.append({
            'body': parent_data['body'],
            'id': parent_data['id'],
            'upvotes': parent_data['upvotes']
        })
        parent_data = parent_data.get('parent_comment')

    return comment_chain[::-1]  # Reverse to have oldest comment first

def sanitize_title(text):
    text = text.replace('"', '').replace("'", "")
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[Link]', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace('~~', '')
    text = text.replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)').replace('>', '\\>').replace('<', '\\<')
    text = text.strip()
    return text


def create_md_from_json(json_data):
    comment_chain = extract_parent_comment_chain(json_data)

    # Form the body of the markdown from the comment chain
    md_chain_content = ""
    for i, comment in enumerate(comment_chain):
        if i == len(comment_chain) - 1:  # This is your comment
            md_chain_content += f"{{{{< myComment >}}}}\n{comment['body']}\n{{{{< /myComment >}}}}\n\n"
        else:
            md_chain_content += f"{{{{< parentComment >}}}}\n{comment['body']}\n{{{{< /parentComment >}}}}\n\n"
    
    subreddit = json_data['subreddit']
    post_title = sanitize_title(json_data['post_title'])  # Use sanitize_title function
    timestamp = json_data['created_utc']

    # The Markdown content
    md_content = f"""---
title: '{post_title}'
date: {unix_to_rfc3339(timestamp)}
subreddit: {subreddit}
upvotes: {json_data['upvotes']}
---

{md_chain_content}
"""

    return md_content

# Make sure 'hugo-comments' directory exists
if not os.path.exists("hugo-comments"):
    os.mkdir("hugo-comments")

index_md_content = "---\ntitle: 'My Reddit Comments'\n---\n\n"

# Loop through all files in the 'comments' directory
for file_name in os.listdir("comments"):
    if file_name.endswith(".json"):
        with open(os.path.join("comments", file_name), 'r') as f:
            json_data = json.load(f)
            # Create individual Markdown content from JSON data
            md_content = create_md_from_json(json_data)
            # Save to a new .md file
            comment_md_filename = f"{json_data['id']}.md"
            with open(os.path.join("hugo-comments", comment_md_filename), 'w') as md_file:
                md_file.write(md_content)

            # Append comment and link to index_md_content
            sanitized_title = sanitize_title(json_data['body'][:50] + "..." if len(json_data['body']) > 50 else json_data['body'])
            karma = json_data['upvotes']
            comment_path = comment_md_filename.rsplit('.', 1)[0]  # This removes the '.md' extension
            index_md_content += f"* {karma} points: [{sanitized_title}]({comment_path})\n"


# Save the index.md
with open(os.path.join("hugo-comments", "index.md"), 'w') as index_md_file:
    index_md_file.write(index_md_content)

print("Conversion completed!")
