import os
import json
from jinja2 import Environment, FileSystemLoader

class HTMLPublisher:
    def __init__(self, directory, template_path=None):
        self.directory = directory
        self.username = directory.split("-")[0] if "-" in directory else None
        
        if not template_path:
            # If no template_path is provided, default to the current directory joined with "template"
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template")
    
        print(f"Using template path: {template_path}")
        self.env = Environment(loader=FileSystemLoader(template_path))

    def get_user_data(self):
        if not self.username:
            return None

        user_file = os.path.join(f"{self.username}.json")
        
        if not os.path.exists(user_file):
            print(f"User data for {self.username} not found!")
            return None

        with open(user_file, 'r') as f:
            return json.load(f)
        
    def generate_html(self):
        template = self.env.get_template('user_comments_template.html')
        user_data = self.get_user_data()
        comments = self.process_directory()

        rendered_html = template.render(user=user_data, comments=comments)
        
        with open('view-comments.html', 'w') as html_file:
            html_file.write(rendered_html)
            
        print("HTML generated at 'view-comments.html'")

    def process_directory(self):
        comments_data = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.json') and not filename == f"{self.username}.json":
                with open(os.path.join(self.directory, filename), 'r') as f:
                    data = json.load(f)
                    comments_data.append(data)
        return comments_data
