import os

def generate_recruiter_files():
    recruiters_folder = '.'
    os.makedirs(recruiters_folder, exist_ok=True)

    recruiters_data = {
        'recruiters_posting1.txt': [
            'alice.johnson@recruiters.com',
            'michael.smith@recruiters.com',
            'sarah.brown@recruiters.com',
            'david.wilson@recruiters.com',
            'emma.davis@recruiters.com'
        ],
        'recruiters_posting2.txt': [
            'james.miller@recruiters.com',
            'olivia.garcia@recruiters.com',
            'daniel.martinez@recruiters.com',
            'sophia.rodriguez@recruiters.com',
            'liam.hernandez@recruiters.com'
        ],
        'recruiters_posting3.txt': [
            'noah.lopez@recruiters.com',
            'isabella.gonzalez@recruiters.com',
            'logan.wilson@recruiters.com',
            'mia.anderson@recruiters.com',
            'lucas.thomas@recruiters.com'
        ],
        'recruiters_posting4.txt': [
            'elijah.taylor@recruiters.com',
            'amelia.moore@recruiters.com',
            'mason.jackson@recruiters.com',
            'harper.martin@recruiters.com',
            'ethan.lee@recruiters.com'
        ],
        'recruiters_posting5.txt': [
            'benjamin.perez@recruiters.com',
            'evelyn.thompson@recruiters.com',
            'alexander.white@recruiters.com',
            'abigail.harris@recruiters.com',
            'jackson.sanchez@recruiters.com'
        ]
    }

    for filename, emails in recruiters_data.items():
        file_path = os.path.join(recruiters_folder, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            for email in emails:
                file.write(email + '\n')
    print("Recruiter files have been generated in the 'recruiters/' folder.")

if __name__ == '__main__':
    generate_recruiter_files()
