# rm_except.py

import os
import shutil

exceptions_list = [
    'templates',
    'app_respond.py',
    'gen_prompt.py',
    'clean_db.sh',
    'models.py',
    'README.md',
    'rm_except.py',
    'requirements.txt',
    'print_database_contents_app.py',
    'populate_database_app.py',
    'posting',
    'recruiters',
    'resume',
    'user_emails',
    '.git'
]

def main():
    root_dir = os.getcwd()

    for item in os.listdir(root_dir):
        if item in exceptions_list:
            continue  # Skip items in the exceptions list
        item_path = os.path.join(root_dir, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
        except Exception as e:
            print(f"Failed to remove {item_path}. Reason: {e}")

if __name__ == "__main__":
    main()
