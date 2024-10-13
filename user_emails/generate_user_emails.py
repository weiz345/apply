# generate_user_emails.py

import os

def generate_user_emails():
    user_emails_folder = '.'
    os.makedirs(user_emails_folder, exist_ok=True)

    user_emails_data = {
        'user_emails_resume1.txt': [
            'john.doe@example.com'
        ],
        'user_emails_resume2.txt': [
            'jane.smith@example.com'
        ],
        'user_emails_resume3.txt': [
            'michael.brown@example.com'
        ],
        'user_emails_resume4.txt': [
            'emily.johnson@example.com'
        ],
        'user_emails_resume5.txt': [
            'sarah.lee@example.com'
        ]
    }

    for filename, emails in user_emails_data.items():
        file_path = os.path.join(user_emails_folder, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            for email in emails:
                file.write(email + '\n')
    print("User email files have been generated in the 'user_emails/' folder.")

if __name__ == '__main__':
    generate_user_emails()
