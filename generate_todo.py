import os
import re

# Define the array of files
files_array = [
    {"name": "JwtAuthorizer", "path": "./authorizers/jwt", "description": "A jwt authorizer for private lambda functions"},
    {"name": "Hello", "path": "./functions/hello", "description": "protected function", "method": "GET", "endpoint": "/users"},
    {"name": "Signin", "path": "./functions/auth/signin", "description": "Signin function", "method": "POST", "endpoint": "/signin"},
    {"name": "CreateUser", "path": "./functions/auth/signup", "description": "Create a user with name and age on Dynamo DB", "method": "POST", "endpoint": "/signup"},
    {"name": "SendConnectionId", "path": "./functions/chat/send_connection_id", "description": "Return the connection id on connect"},
    {"name": "Connect", "path": "./functions/chat/connect", "description": "real time chat"},
    {"name": "SendMessage", "path": "./functions/chat/send_message", "description": "real time chat"},
    {"name": "Disconnect", "path": "./functions/chat/disconnect", "description": "real time chat"}
]

# Define the function to check for keywords and capture subsequent comments until a blank line
def check_for_keywords_with_comments(file_path):
    keywords_with_comments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        keyword = None
        comment_lines = []
        for line in lines:
            if keyword is not None:
                if line.strip() == '':
                    if comment_lines:
                        if keyword not in keywords_with_comments:
                            keywords_with_comments[keyword] = []
                        keywords_with_comments[keyword].append(' '.join(comment_lines))
                        comment_lines = []
                else:
                    comment_lines.append(line.strip())
            else:
                for kw in ['help', 'improve', 'waiting', 'todo', 'fixme']:
                    if f'# {kw.upper()}' in line:
                        keyword = kw
    return keywords_with_comments

# Define the function to generate HTML with different background colors for each keyword
def generate_html(keywords_with_comments):
    html = '<html><head><title>TODO Log</title></head><body>'
    for keyword, comments in keywords_with_comments.items():
        if keyword == 'help':
            color = '#FFD700'  # Gold
        elif keyword == 'improve':
            color = '#90EE90'  # Light Green
        elif keyword == 'waiting':
            color = '#87CEEB'  # Sky Blue
        elif keyword == 'todo':
            color = '#FFA07A'  # Light Salmon
        elif keyword == 'fixme':
            color = '#FF6347'  # Tomato
        else:
            color = '#FFFFFF'  # White (default)
        for comment in comments:
            html += f'<div style="background-color: {color};">{keyword.upper()}: {comment}</div>'
    html += '</body></html>'
    return html

# Define the function to iterate through files and generate HTML with keywords and comments
def iterate_files_and_generate_html(files):
    all_keywords_with_comments = {}
    for file_data in files:
        file_path = os.path.join(file_data['path'], f"main.py")
        if os.path.exists(file_path):
            keywords_with_comments = check_for_keywords_with_comments(file_path)
            for keyword, comments in keywords_with_comments.items():
                if keyword not in all_keywords_with_comments:
                    all_keywords_with_comments[keyword] = []
                all_keywords_with_comments[keyword].extend(comments)
    html = generate_html(all_keywords_with_comments)
    with open('todo_log.html', 'w') as html_file:
        html_file.write(html)

# Call the function to iterate through files and generate HTML with keywords and comments
iterate_files_and_generate_html(files_array)
